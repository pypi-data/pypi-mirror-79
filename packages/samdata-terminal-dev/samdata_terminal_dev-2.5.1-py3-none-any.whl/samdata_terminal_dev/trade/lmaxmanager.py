# coding=utf-8
"""
    仿真交易订单模块
"""

from datetime import datetime
import requests
import json
import random
import string
import traceback

from ..core.storage import context, Holding
from ..helper.loghelper import LogHelper
from ..model.order import PaperOrder
from ..core.producer import OrderProduce

fill_time_cache = []
diverse_dict = {"Buy": "Sell", "Sell": "Buy"}
fee_ratio = 0  # 手续费率

class LmaxTradeEngine(object):
    """Lmax仿真交易引擎类"""

    def __init__(self):
        self.order_id_dict = {}    # 保存samdata 订单id与lmax订单查询id(clOrId)的映射
        self.waorking_order_dict = {}    #  保存没有完成的订单信息，便于查询该订单信息
        self.order_url = ""

    def set_order_conn(self):
        self.order_url = "http://{ip}:{port}/Lmax/CreateOrder".format(ip=context.orderserver.server_url, port = context.orderserver.port)
        self.check_order_url = "http://{ip}:{port}/Lmax/GetOrderStatus".format(ip=context.orderserver.server_url, port = context.orderserver.port)

    def __get_order_id(self):
        """
        生成唯一的下单id
        """
        value = "SO" + datetime.strftime(datetime.utcnow(), "%Y%m%d") + ''.join(random.sample(string.ascii_letters + string.digits, 8))
        return value

    def create_order_into_mysql(self, order):
        """
        往数据库中插入订单数据
        :params order: 订单, Order对象
        """
        data = (context.strategyid, order.symbol, order.order_type, order.order_time, order.fill_time, datetime.now(),
                round(order.quantity, 4), order.open_or_close, order.order_id, order.fillprice, order.direction,
                context.paperid, order.status, order.nav,
                order.cach, order.close_profit, order.close_profit_ratio, order.fee, datetime.now(),
                datetime.now(), order.positionid, order.order_result, order.limit_price, order.exchange_orderid, order.fill_quantity, order.volume_multiple)
        print(data)
        OrderProduce(data)
        log = 'orderid : ' + str(order.order_id) + ', 状态： ' + order.status
        LogHelper.info(log)

    def create_order(self, order):
        self.create_order_into_mysql(order)

    def fit_order(self, order):
        """
        成交订单
        :params order: 订单, Order对象
        :params order: 订单
        :returns status: 成交状态
        """
        lmaxorderid = ""
        status = ""
        if order.order_id is None:
            order.order_id = self.__get_order_id()

        LogHelper.info("************ orderid : %s " % (order.order_id))

        if isinstance(order, PaperOrder):
            LogHelper.info("用户发送的订单信息 : %s  " % order.to_string())
            is_operate, order = self.check_order_operate(order)

            if is_operate:
                if order.order_type == 0:
                    status, order, lmaxorderid = self.fit_market_order(order)
                else:
                    status, order, lmaxorderid = self.fit_limit_order(order)

                LogHelper.info("从lmax返回的订单状态: %s "% (status))
                if status == "Filled" or status == "Partially filled":
                    self.handle_position(order)
                self.create_order(order)
        return status, order, lmaxorderid

    def fit_limit_order(self, order):
        """
        按限价成交订单
        :params order: 订单, Order对象
        :returns status: 订单状态,
        :returns order: 订单
        """
        status = ""
        side = order.direction.upper()

        # 如果为平仓操作，则反向操作仓位
        if order.direction == "Buy":
            side = 0
        else:
            side = 1
        headers = {'Content-Type':'application/json'}

        try:
            order.symbol = order.symbol
        except Exception as str_ex:
            print("将品种名转换成指定格式时出错")
            print(str_ex)
            traceback.print_exc()

        data = {
            "Symbol": order.symbol,  # "XAU/USDm"
            "Direction": side,
            "Qty": order.quantity,
            "Price":order.limit_price,
            "Type": 1   # 限价下单
        }

        LogHelper.info("向lmax 发送订单数据: "+ str(data))
        req = requests.post(url= self.order_url, headers = headers, data = json.dumps(data), timeout=10)

        try:
            if req.status_code == 200:
                response_data = req.json()
                LogHelper.info("订单返回信息: "+ str(response_data))
                if response_data["order"] and "Symbol" in response_data["order"].keys():
                    response_order = response_data["order"]
                    order.status = response_order.get("Status")
                    order.fillprice = response_order.get("AvgPrice")
                    order.fill_quantity = response_order.get("CumQty")
                    order.fill_time = response_order.get("Time")
                    order.order_result = response_order.get("Detail")
                    order.exchange_orderid = response_order.get("LmaxOrderId")
                    order.volume_multiple = response_order.get("VolumeMultiple")

                    if order.status == "New":
                        self.waorking_order_dict[order.order_id] = response_order["ClOrdID"]
                    status = order.status
                else:
                    LogHelper.warn("没有下单数据返回")
                    order.status = "UnKnow"
                    order.fill_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H:%M:%S")
            else:
                status = "fail"
                LogHelper.error("下单失败, code: %s" % str(req.status_code))
        except Exception as ex:
            LogHelper.error("处理订单信息时出现异常: %s" % str(ex))
            traceback.print_exc()
        return status, order, order.exchange_orderid

    def fit_market_order(self, order):
        """
        按市价成交订单
        :params order: 订单, Order对象
        :returns status: 订单状态,
        :returns order: 订单
        """
        status = ""
        side = order.direction.upper()

        # 如果为平仓操作，则反向操作仓位
        if order.direction == "Buy":
            side = 0
        else:
            side = 1

        headers = {'Content-Type':'application/json'}

        try:
            order.symbol = order.symbol
        except Exception as str_ex:
            print("将品种名转换成指定格式时出错")
            print(str_ex)
            traceback.print_exc()

        data = {
            "Symbol": order.symbol,  # "XAU/USDm"
            "Direction": side,
            "Qty": order.quantity,
            "Price":order.limit_price,
            "Type": 0    # 市价下单
        }

        LogHelper.info("向lmax 发送订单数据: "+ str(data))
        req = requests.post(url=self.order_url, headers = headers, data = json.dumps(data), timeout=10)

        try:
            if req.status_code == 200:
                response_data = req.json()
                LogHelper.info("订单返回信息: "+ str(response_data))
                if response_data["order"] and "Symbol" in response_data["order"].keys():
                    response_order = response_data["order"]
                    order.status = response_order.get("Status")
                    order.fillprice = float(response_order.get("AvgPrice"))
                    order.fill_quantity = float(response_order.get("CumQty"))
                    order.fill_time = response_order.get("Time")
                    order.order_result = response_order.get("Detail")
                    order.exchange_orderid = response_order.get("LmaxOrderId")
                    order.volume_multiple = response_order.get("VolumeMultiple")

                    status = order.status
                else:
                    LogHelper.warn("没有下单数据返回")
                    order.status = "fail"
                    order.fill_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H:%M:%S")
            else:
                status = "fail"
                LogHelper.error("下单失败, code: %s" % (str(req.status_code)))
        except Exception as ex:
            LogHelper.error("处理订单信息时出现异常: %s " % (str(ex)))
            traceback.print_exc()
        return status, order, order.exchange_orderid

    def check_order_operate(self,order):
        """
        判断该订单是否可以进行操作：
        """
        result = order
        is_operate = True
        if isinstance(result, PaperOrder):
            if result.open_or_close == "Close":  # 平仓
                holds = context.holdings.get(result.symbol)
                diverse_direction = diverse_dict[result.direction]

                if holds:  # 有持仓
                    diverse_hold = holds.get(diverse_direction)

                    if diverse_hold:
                        total_quantity = sum([item.quantity for item in diverse_hold])
                        spread = total_quantity - result.quantity

                        # 当前仓位不足以平仓，则先平仓再进行开仓
                        if spread < 0 :
                            # 是否可以进行反手开仓
                            if context.is_reverse_operate:
                                open_order = result
                                import math
                                open_order.quantity = math.fabs(spread)
                                open_order.open_or_close = "Open"
                                result.quantity = total_quantity
                                self.fit_order(result)
                                msg = "没有" + diverse_direction + "方向持仓，无法进行平仓，但可以进行反手开仓！！！"
                                LogHelper.error(msg)
                            else:
                                msg = "没有足够" + diverse_direction + "方向持仓，无法进行平仓"
                                LogHelper.error(msg)
                                is_operate = False
                    else:
                        if context.is_reverse_operate:
                            open_order = result
                            open_order.open_or_close = "Open"
                            result.quantity = order.quantity
                            self.fit_order(result)
                            msg = "没有" + diverse_direction + "方向持仓，无法进行平仓，但可以进行反手开仓！！！"
                            LogHelper.error(msg)
                            is_operate = False
                        else:
                            msg = "没有足够" + diverse_direction + "方向持仓，无法进行平仓"
                            LogHelper.error(msg)
                            is_operate = False
                else:
                    if context.is_reverse_operate:
                        result.open_or_close = "Open"
                        msg = "没有" + diverse_direction + "方向持仓，无法进行平仓，但可以进行反手开仓！！！"
                        LogHelper.error(msg)
                    else:
                        msg = "没有" + diverse_direction + "方向持仓，无法进行平仓！！！"
                        LogHelper.error(msg)
                        is_operate = False

            return is_operate, result

    def handle_position(self, order):
        """
        仓位处理、资金计算
        :params order: 订单, Order对象
        :return
        """
        global  fee

        if isinstance(order, PaperOrder):
            if order.open_or_close == "Open":  # 开仓
                holds = context.holdings.get(order.symbol)
                hold_id = ""
                hold = None

                if holds:  # 是否持有相同方向的仓库, 有则加仓， 否则建仓
                    same_hold = holds.get(order.direction)

                    """
                    if same_hold:
                        sum_price = same_hold.quantity * same_hold.averageprice   # 使用平均成本价计算
                        same_hold.quantity = same_hold.quantity + order.quantity
                        same_hold.averageprice = (sum_price + order.quantity * order.fillprice) / same_hold.quantity
                    else:
                        hold = Holding(order.symbol, order.direction, order.quantity, order.fillprice, order.fill_time)
                        holds[order.direction] = []
                        holds[order.direction].append(hold)
                    """
                    if not same_hold:
                        holds[order.direction] = []
                    hold = Holding(order.symbol, order.direction, order.quantity, order.fillprice, order.fill_time)
                    holds[order.direction].append(hold)
                else:
                    msg = "当前没有任何仓位，创建仓位!!!"
                    LogHelper.info(msg)
                    hold = Holding(order.symbol, order.direction, order.quantity, order.fillprice, order.fill_time)
                    holds = {}
                    holds[order.direction] = []
                    holds[order.direction].append(hold)

                context.holdings[order.symbol] = holds
                fee = order.quantity * order.fillprice * fee_ratio
                context.cash = context.cash - order.quantity * order.fillprice - fee
                hold_cash = 0
                for key in holds.keys():
                    for item in holds[key]:
                        hold_cash = hold_cash + item.quantity * item.averageprice
                context.total_cash = context.cash + hold_cash
                # order.positionid = hold.positionid
                order.fee = fee
                order.nav = context.total_cash
                order.cach = context.cash
                
                if order.direction == "Buy":
                    msg = "开仓成功, 开仓价: " + str(order.fillprice) + ', 开仓量: ' + str(
                        order.quantity) + ', 开仓方向: 多, 手续费: ' + str(fee) + ',成交时间: '+ order.fill_time
                elif order.direction == "Sell":
                    msg = "开仓成功, 开仓价: " + str(order.fillprice) + ', 开仓量: ' + str(
                        order.quantity) + ', 开仓方向: 空, 手续费: ' + str(fee) + '成交时间: ' + order.fill_time

                LogHelper.fatal(msg)
            else:  # 平仓
                holds = context.holdings.get(order.symbol)
                diverse_direction = diverse_dict[order.direction]

                if holds:  # 有持仓
                    diverse_holds = holds.get(diverse_direction)

                    if diverse_holds:
                        diverse_holds = sorted(diverse_holds, key=lambda x: x.creat_time, reverse=True)
                        close_profit = 0.0
                        cost = 0.0

                        for diverse_hold in diverse_holds:
                            diverse_hold.quantity = diverse_hold.quantity - order.quantity
                            open_price = diverse_hold.averageprice

                            # 平仓收益 = （平仓价 - 平掉的当前仓位的开仓价） * 方向系数
                            close_profit = close_profit + ((order.fillprice - open_price) * (1 if diverse_direction == "Buy" else -1))
                            cost = cost + order.quantity * open_price

                            if diverse_hold.quantity > 0 or diverse_hold.quantity == 0:
                                if diverse_hold.quantity == 0:
                                    diverse_holds.remove(diverse_hold) 
                                break
                        
                        if len(diverse_holds) ==0:
                            holds.pop(diverse_direction)

                        hold_cash = 0
                        for item in diverse_holds:
                            hold_cash = hold_cash + item.quantity * item.averageprice

                        fee = order.fillprice * order.quantity * fee_ratio
                        context.holdings[order.symbol] = holds
                        context.cash = context.cash + cost + close_profit - fee
                        context.total_cash = context.cash + hold_cash
                        order.nav = context.total_cash
                        order.cach = context.cash

                        order.fee = round(fee, 4)

                        if diverse_direction == "Sell":
                            msg = "平仓成功, 平仓价: " + str(order.fillprice) + ', 平仓量: ' + str(
                                order.quantity) + ', 平仓方向: 空, 开仓价： ' + str(open_price) + ', 手续费: ' + str(
                                fee) + ', 时间: '+ order.order_time  #  + order.fill_time
                        elif diverse_direction == "Buy":
                            msg = "平仓成功, 平仓价: " + str(order.fillprice) + ', 平仓量: ' + str(
                                order.quantity) + ', 平仓方向: 多, 开仓价： ' + str(open_price) + ', 手续费: ' + str(
                                fee) + ', 时间: '+ order.order_time  #  + order.fill_time
                        LogHelper.debug(msg)

            msg = '总资产为' + str(context.total_cash)
            LogHelper.warn(msg)

            msg = '可用资金为' + str(context.cash)
            if context.cash < 0 :
                LogHelper.warn(msg)
            else:
                LogHelper.info(msg)

            holds = context.holdings
            if len(holds.keys()) != 0:
                for symbol in holds:
                    LogHelper.warn("当前持仓情况: " + symbol)
                    for key in holds[symbol]:
                        for item in holds[symbol][key]:
                            msg = ("direction: {} , quantity: {} , price: {}, create_time: {} " ).format(item.direction, str(
                                item.quantity),  str(item.averageprice), item.creat_time)
                            LogHelper.warn(msg)
        return order

    def check_order_status(self,order_id):
        """
        查询订单状态，对于没有立即完成的订单，定时查询订单状态，获取订单的成交信息
        """
        clOrId = self.order_id_dict.get(order_id)
        order= self.waorking_order_dict.get(order_id)
        
        headers = {'Content-Type':'application/json'}
        data = {
            "clOrId": clOrId,  # Lmax查询id
        }

        while True:
            import time
            time.sleep(5)
            LogHelper.info("向lmax 查询订单数据: "+ str(data))
            req = requests.post(url=self.check_order_url, headers = headers, data = json.dumps(data), timeout=10)

            try:
                if req.status_code == 200:
                    response_data = req.json()
                    LogHelper.info("订单返回信息: "+ str(response_data))
                    if response_data["order"] and "Symbol" in response_data["order"].keys():
                        response_order = response_data["order"]
                        order.status = response_order["Status"]
                        order.fillprice = float(response_order["AvgPrice"])
                        order.fill_quantity = float(response_order["CumQty"])
                        order.fill_time = response_order["Time"]
                        order.order_result = response_order["Detail"]
                        order.exchange_orderid = response_order["LmaxOrderId"]
                        order.volume_multiple = response_order["VolumeMultiple"]
                        break
                    else:
                        LogHelper.warn("没有下单数据返回")
                        order.status = "fail"
                        order.fill_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H:%M:%S")
                else:
                    status = "fail"
                    LogHelper.error("下单失败, code: %s" % (str(req.status_code)))
            except Exception as ex: 
                LogHelper.error("处理订单信息时出现异常: %s " % (str(ex)))
                traceback.print_exc()


# 下单引擎实例
lmaxtradeengine =LmaxTradeEngine()


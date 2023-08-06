# -*- encoding:utf-8 -*-

class Order(object):
    """
        订单类
    """
    def __init__(self, symbol, direction, order_time, quantity, 
            open_or_close, order_type, fillprice, limit_price=0, order_id = 0):
        """
        初始化
        :params symbol: 品种名, str
        :params direction: 方向("Buy":多，"Sell":空), str
        :params order_time: 下单时间, str
        :params quantity: 数量, int
        :params open_or_close：开仓("Open")/平仓("Close"), str
        :params order_type: 
        :params fillprice: 成交价, float
        :params limitprice: 限价，float
        """
        self.order_id = None   # 订单id
        self.symbol = symbol # 品种名
        self.direction = direction   # 方向
        self.order_time = order_time  # 下单时间
        self.fill_time = None   # 成交时间
        self.quantity = quantity  # 下单数量
        self.open_or_close = open_or_close  # 开/平仓
        self.fillprice = fillprice    # 最终成交价
        self.limit_price = limit_price   # 限价
        self.order_type = order_type  # 订单类型, 市价/限价单
        self.positionid = None   # 仓位id
        self.close_profit = None   # 平仓收益
        self.close_profit_ratio = None  # 平仓收益率
        self.status = ""    # 订单状态
        self.cach = 0   # 余额
        self.fee = 0    # 手续费
        self.nav = 0    # 资产总价值
        self.order_result = None  # 订单信息

class PaperOrder(object):
    """
        订单类
    """
    def __init__(self, symbol, direction, order_time, quantity,
            open_or_close, order_type, fillprice, limit_price=0, order_id = None):
        """
        初始化
        :params symbol: 品种名, str
        :params direction: 方向("Buy":多，"Sell":空), str
        :params order_time: 下单时间, str
        :params quantity: 数量, int
        :params open_or_close：开仓("Open")/平仓("Close"), str
        :params order_type:
        :params fillprice: 成交价, float
        :params limitprice: 限价，float
        """
        self.order_id = order_id   # 订单id
        self.symbol = symbol      # 品种名
        self.direction = direction    # 方向
        self.order_time = order_time   # 下单时间
        self.fill_time = None     # 成交时间
        self.quantity = quantity   # 下单数量
        self.fill_quantity = None   # 最终成交数量
        self.open_or_close = open_or_close    # 开/平仓
        self.fillprice = fillprice    # 最终成交价
        self.limit_price = limit_price  # 限价
        self.order_type = order_type    # 订单类型, 市价/限价单
        self.positionid = None    # 仓位id
        self.close_profit = None   # 平仓收益
        self.close_profit_ratio = None    # 平仓收益率
        self.status = ""    # 订单状态
        self.cach = 0     # 余额
        self.fee = 0      # 手续费
        self.nav = 0     # 资产总价值
        self.order_result = None    # 订单信息
        self.exchange_orderid = None    # 平台订单id
        self.volume_multiple = None    # 合约乘数

    def to_string(self):
        order_type = ""
        if self.order_type == 0:
            order_type = "market"
        elif self.order_type == 1:
            order_type = "limit"

        result = ("symbol: {}, quantity: {}, order_type: {}, direction: {}, open_or_close: {}, limit_price: {}").format(self.symbol, self.quantity, order_type, self.direction, self.open_or_close, self.limit_price)
        return result

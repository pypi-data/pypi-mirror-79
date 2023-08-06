from ..core.storage import context

class DataSourceExcetion(Exception):
    """
    数据源无效异常
    """
    def __init__(self):
        context.trader.stop()
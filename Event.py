class Event(object):
    """
    作为事件的基本 class 为所有子事件提供一个界面，以触发交易
    """
    
    pass
    
class MarketEvent(Event):
    """
    根据 bars 触发更新并接收新数据
    """
    
    def __init__(self):
        self.type = 'MARKET'
        
class SignalEvent(Event):
    """
    从 Strategy 得到交易信号，传递给 Portfolio
    """
    
    def __init__(self, strategy_id, symbol, datetime, signal_type, strength):
        """
        初始化 SignalEvent
        
        
        参数:
        strategy_id - 每个策略的唯一标识符
        symbol - 证券的编号
        datetime - signal 生成时的时间 timestamp
        signal_type - 'LONG' or 'SHORT' 多头或者空头
        strength - 调整策略因子，用于调整 portfolio 的数量
        """
        
        self.type = 'SIGNAL'
        self.strategy_id = strategy_id
        self.symbol = symbol
        self.datetime = datetime
        self.signal_type = signal_type
        self.strength = strength
        
class OrderEvent(Event):
    """
    将交易（order）指令传递给执行系统，order 包括 标的(如：ETF50), 
    交易的类型、交易的数量和交易方向
    """
    
    def __init__(self, symbol, order_type, quantity, direction):
        """
        初始化交易类型，设置为市价指令（'MKT'）或者限价指令('LMT'）
        并设定交易数量（整数）和交易方向（买、卖）
        
        参数：
        symbol -  交易的标的
        order_type - 'MKT' or 'LMT' 市价指令或者限价指令
        quantity - 非负整数
        direction - 'BUY' or 'SELL' 多头或者空头
        """
        
        
        self.type = 'ORDER'
        self.symbol = symbol
        self.order_type = order_type
        self.quantity = quantity
        self.direction = direction
    
    def print_order(self):
        """
        输出交易的价值
        """
        print('Order: Symbol=%s, Type%s, Quantity=%s, Direction%s' %(
        self.symbol, self.order_type, self.quantity, self.direction))
        
class FillEvent(Event):
    """
    当接收到交易指令时，封装交易指令。存储要交易标的的数量和价格，
    并存储委托交易信息。
    """
    
    def __init__(self, timeindex, symbol, exchange, quantity,
                direction, fill_cost, commission=None):
        """
        初始化 FillEvent, 设置 标的symbol, exchange, quantity, direction,
        cost, and an optional commission
        
        如果 commission 没有被提供， Fill 会基于交易数量和交易费用计算
        
        参数：
        timeindex - bars-resolution bar的转换
        symbol - 标的资产
        exchange - 交易所
        quantity - 交易数量
        direction - 交易方向
        fill_cost - 交易费用
        commission - 可选佣金

        """
        
        self.type = 'FILL'
        self.timeindex = timeindex
        self.symbol = symbol
        self.exchange = exchange
        self.quantity = quantity
        self.direction = direction
        self.fill_cost = fill_cost
        
        # 计算佣金
        if commission is None:
            self.commission = self.calculate_ib_commission()
        else:
            self.commission = commission
    
    def calculate_ib_commission(self):
        """
        计算交易费用
        
        此处以美国为例
        """
        full_cost = 1.3
        if self.quantity <=500：
            full_cost = max(1.3, 0.013 * self.quantity)
        else:
            full_cost = max(1.3, 0.008 * self.quantity)
        return full_cost
        
        
        
        
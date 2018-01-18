
from abc import ABCMeta, absractmethod
import datetime
import os
import numpy as np
import pandas as pd

from Event import MarketEvent

class DataHandler(object):
	"""
	DataHandler 是一个抽象类，用于给所有子类提供一个交互界面
	
	DataHandler 主要是根据需求返回所需的数据
	"""
	
	__metaclass__ = ABCMeta
	
	@absractmethod
	def get_latest_bar(self, symbol):
		"""
		返回一个最新bar的信息
		"""
		
		raise NotImplementedError("Should implement get_latest_bar()")
		
	@absractmethod
	def get_latest_bars(self, symbol, N=1):
		"""
		返回前N个最新bar的信息
		"""
		
		raise NotImplementedError("Should implement get_latest_bars()")
	
	@absractmethod
	def get_latest_datetime(self, symbol):
		"""
		返回最新 bar 的 python datetime 格式的时间
		"""
		
		raise NotImplementedError("Should implement get_latest_datetime()")
		
	@absractmethod
	def get_latest_bar_value(self, symbol, val_type):
		"""
		返回最新 bar 的数据
		"""
		
		raise NotImplementedError("Should implement get_latest_bar_value()")
	
	@absractmethod
	def et_latest_bar_values(self, symbol, val_type, N=1):
		"""
		返回最新 N 个 bar 的数据
		"""
		
		raise NotImplementedError("Should implement et_latest_bar_values()")
		
	@absractmethod
	def update_bars(self):
		"""
		更新当前 bar 并将最近的bars 放进 bar_queue 队列中，存储所有symbol的数据
		"""
		
		raise NotImplementedError("Should implement update_bars()")
		

class HistoricMysqlDataHandler(DataHandler):
	"""
	HistoricMysqlDataHandler 提供一个接口，用于从 Mysql  数据库中读取需要的数据
	"""
	
	def __init__(self, events, mysql_dir, symbol_list):
		"""
		初始化 historic data handler
		
		参数：
		events - The Event Queue 事件队列
		mysql_dir - Mysql 的地址
		symbol_list - 股票池
		"""
		
		self.events = events
		self.mysql_dir = mysql_dir
		self.symbol_list = symbol_list
		
		self.symbol_data = {}
		self.latest_symbol_data = {}
		self.continue_backtest = True
		
	def _open_convert_mysql(self):
	
		"""
		将 Mysql 数据读入，根据 symbol 以字典形式
		将数据存成 DataFrame 格式
		"""
		
		for s in self.symbol_list:
			self.symbol_data[s] = self.get_data_from_mysql(s)
			
			# 设置 最新的 symbol_data 为 空
			self.latest_symbol_data[s] = []
			
		
	def get_data_from_mysql(s):
		"""
		从 mysql 中读取数据，输出 DataFrame 格式的时间
		"""
		pass
	
	def _get_new_bar(self, symbol):
		"""
		返回最新的数据
		"""
		
		for b in self.symbol_data[symbol]:
			yield b
			
	def get_latest_bar(self, symbol):
		"""
		从 latest_symbol 列表中返回一个最新的 bar
		"""
		
		try:
			bars_list = self.latest_symbol_data[symbol]
		except KeyError:
			print("这个 symbol 在历史数据库中不可用")
			raise
		else:
			return bars_list[-1]
	
	def get_latest_datetime(self, symbol):
		"""
		返回最新 bar 的 datetime 时间 
		"""
		
		try:
			bars_list = self.latest_symbol_data[symbol]
		except:
			print("这个 symbol 在历史数据库中不可用")
			raise
		else:
			return bars_list[-1][0] ## 第一个为时间
			
			
	def get_latest_bar_value(self, symbol, val_type):
		"""
		返回最新 bar 的一条信息
		"""
		
		try:
			bars_list = self.get_latest_bar[symbol]
		except:
			print("这个 symbol 在历史数据库中不可用")
			raise
		else:
			return bars_list[-1][val_type]
			
	def get_latest_bar_values(self, symbol, val_type, N=1):
		"""
		返回最新 bar 的 N 条信息
		"""
		
		try:
			bars_list = self.get_latest_bars(symbol, N)
		except:
			print("这个 symbol 在历史数据库中不可用")
			raise
		else:
			return bars_list[-N:][val_type]
			
	def update_bars(self):
		"""
		将所有 symbol_list 证券池中的所有 symbol 证券的
		最新 bar 的数据放入 latest_symbol_data 中
		"""
		
		for s in self.symbol_list:
			try:
				bar = next(self._get_new_bar(s))
			except StopIteration:
				## 已经遍历了所有选取的时间的数据
				self.continue_backtest = False
			else:
				if bar is not None:
					self.latest_symbol_data[s].append(bar)
		
		self.events.put(MarketEvent()) ## 发送 MarketEvent 信号
		
		
		
		
		
		
		
		
		
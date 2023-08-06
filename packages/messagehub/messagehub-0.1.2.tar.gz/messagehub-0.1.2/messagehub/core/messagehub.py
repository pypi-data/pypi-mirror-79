# -*- coding:utf-8 -*-
"""
message hub project
Created on 2020/08/07
@author: Xinqi Yang
@group : https://chaininout.com
@contact: xinqiyang@gmail.com
"""
from __future__ import division
import datetime
import traceback
import sys
import pandas as pd
import json
from messagehub.core import client
from messagehub.util import upass
from messagehub.util.formula import MA
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

PRICE_COLS = ['o', 'c', 'h', 'l', 'pre_c']

# define type
ASSET_STOCK = "stock"
ASSET_INDEX = "index"
ASSET_SPOT = "spot"

# Derivatives 衍生品
ASSET_DELIVERY = "delivery"     # 交割
ASSET_PERPETUAL = "perpetual"   # 永续

ASSET_OPTION = "option"
ASSET_ETF = "etf"

FORMAT = lambda x: '%.4f' % x

TIMEFRAMES = {
                '1m': '1m',
                '5m': '5m',
                '30m': '30m',
                '1h': '1h',
                '4h': '4h',
                '1d': '1d',
                '1w': '1w',
                '1M': '1M',
            }

FACT_LIST = {
    'tor': 'turnover_rate',
    'turnover_rate': 'turnover_rate',
    'vr': 'volume_ratio',
    'volume_ratio': 'volume_ratio',
    'pe': 'pe',
    'pe_ttm': 'pe_ttm',
}


def api(token='', timeout=10):
    """
    初始化pro API,第一次可以通过ts.set_token('your token')来记录自己的token凭证，临时token可以通过本参数传入
    """
    if token == '' or token is None:
        token = upass.get_token()
    else:
        upass.set_token(token)
    if token is not None and token != '':
        api_instance = client.DataApi(token=token, timeout=timeout)
        return api_instance
    else:
        raise Exception('api_instance init error.')


def bar(code='', api_instance=None, start_date='', end_date='', freq='1d', asset=ASSET_PERPETUAL,
            exchange='binance',
            ma=[],
            offset=0,
            limit=200,
            retry_count=3):

    """
    BAR数据
    Parameters:
    ------------
    code: 代码，支持 数字金融相关领域的：  数字货币 现货, 期货, 永续合约, 期权, ETF, 股票, 指数
    start_date: 开始日期  YYYYMMDD
    end_date: 结束日期 YYYYMMDD

    asset: stock: 美股,港股,上证股,日股   index:指数, spot:数字货币 现货,   delivery 交割, perpetual 永续,  option: 期权,  etf: ETF

    exchange: 市场代码，数字货币为交易所代码
    freq: 支持 1/5/15/30min, 1h, 4h, 1d, 1w, 1M

    ma:均线,支持自定义均线频度， 如：ma5/ma10/ma20/ma60/maN   # crypto 7，25，99
    offset:开始行数（分页功能，从第几行开始取数据）
    limit: 本次提取数据行数

    retry_count: 网络重试次数

    Return
    ----------
    DataFrame
    timestamp   o         h         l         c         v
    """
    data = pd.DataFrame()
    if code == '' or code is None:
        logger.warning('必须输入代码')
        return

    if freq not in TIMEFRAMES.keys():
        logger.warning("输入的间隔参数freq出错，请检查")
        return

    freq = freq.strip()

    if 'm' not in freq:
        today = datetime.datetime.today().date()
        today = str(today)[0:10]
        start_date = '' if start_date is None else start_date
        end_date = today if end_date == '' or end_date is None else end_date
        start_date = start_date.replace('-', '')
        end_date = end_date.replace('-', '')

    code = code.lower()
    asset = asset.strip().lower()

    if api_instance is None:
        api_instance = api()

    if limit > 500:
        limit = 500

    for _ in range(retry_count):
        try:
            api_name = "{}".format(asset).lower()
            logger.info(api_name)
            data = getattr(api_instance, api_name)(exchange=exchange, code=code, interval=freq, start_date=start_date, end_date=end_date, offset=offset,
                                     limit=limit)

            if 'm' in freq and data is not None and len(data.index) > 0 and "c" in data.columns:
                data['pre_c'] = data['c'].shift(-1)
            # update ma info
            if ma is not None and len(ma) > 0:
                for a in ma:
                    if isinstance(a, int):
                        data['ma%s' % a] = MA(data['c'], a).map(FORMAT).shift(-(a - 1))
                        data['ma%s' % a] = data['ma%s' % a].astype(float)
                        # value ma
                        data['ma_v_%s' % a] = MA(data['v'], a).map(FORMAT).shift(-(a - 1))
                        data['ma_v_%s' % a] = data['ma_v_%s' % a].astype(float)

            # reset index
            if data is not None and len(data.index) > 0 and "timestamp" in data.columns:
                data['date'] = pd.to_datetime(data['timestamp'], unit='ms', utc=True, infer_datetime_format=True)
                data = data.reset_index(drop=True)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            # error = "{}".format(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
            # print("------no  auth---------")
            # print(error)
            exc_value = str(exc_value).replace('Exception: ', '')
            error = json.loads(exc_value)
            if error.get('code') == '401':
                logger.error(error.get('message'))
                break
        else:
            return data


def flash(query='', source_name='jinse', api_instance=None, start_date='', end_date='',
            offset=0,
            limit=100,
            retry_count=3):

    """
    flash快讯数据
    Parameters:
    ------------
    query: 查询关键词，默认空为显示全部
    source_name: 默认 金色财经   jinse, huoxing, bishijie, 海外版本支持:  twitter （判断用户ip在海外）
    start_date: 开始日期  YYYYMMDD
    end_date: 结束日期 YYYYMMDD
    offset:开始行数（分页功能，从第几行开始取数据）
    limit: 本次提取数据行数
    retry_count: 网络重试次数
    Return
    ----------
    DataFrame
    timestamp   title         body
    """
    data = pd.DataFrame()
    if api_instance is None:
        api_instance = api()

    if limit > 500:
        limit = 500

    for _ in range(retry_count):
        try:
            api_name = "flash"
            data = getattr(api_instance, api_name)(query=query, source_name=source_name, start_date=start_date, end_date=end_date, offset=offset,
                                     limit=limit)
            # reset index
            if data is not None and len(data.index) > 0 and "timestamp" in data.columns:
                # add to date
                data['date'] = pd.to_datetime(data['timestamp'], unit='s', utc=True, infer_datetime_format=True)
                data = data.reset_index(drop=True)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            # error = "{}".format(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
            # print("------no  auth---------")
            # print(error)
            exc_value = str(exc_value).replace('Exception: ', '')
            error = json.loads(exc_value)
            if error.get('code') == '401':
                logger.error(error.get('message'))
                break
        else:
            return data


def wallet(owner='', blockchain='bitcoin', symbol='btc', api_instance=None,
            offset=0,
            limit=500,
            retry_count=3):

    """
    获取标记钱包信息
    Parameters:
    ------------
    owner: 查询关键词，默认空为显示全部
    blockchain: 默认 bitcoin  显示公链数据
    symbol: 默认 btc ,        显示token数据
    offset:开始行数（分页功能，从第几行开始取数据）
    limit: 本次提取数据行数
    retry_count: 网络重试次数
    Return
    ----------
    DataFrame
    timestamp   title         body
    """
    data = pd.DataFrame()
    if api_instance is None:
        api_instance = api()

    if limit > 500:
        limit = 500

    for _ in range(retry_count):
        try:
            api_name = "wallet"
            data = getattr(api_instance, api_name)(owner=owner, blockchain=blockchain, symbol=symbol, offset=offset,
                                     limit=limit)
            # reset index
            if data is not None and len(data.index) > 0 and "timestamp" in data.columns:
                # add to date
                data['date'] = pd.to_datetime(data['timestamp'], unit='s', utc=True, infer_datetime_format=True)
                data = data.reset_index(drop=True)

        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            # error = "{}".format(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
            # print("------no  auth---------")
            # print(error)
            exc_value = str(exc_value).replace('Exception: ', '')
            error = json.loads(exc_value)
            if error.get('code') == '401':
                logger.error(error.get('message'))
                break
        else:
            return data


def transaction(owner='', blockchain='bitcoin', symbol='btc', api_instance=None,
            offset=0,
            limit=500,
            retry_count=3):

    """
    获取大
    Parameters:
    ------------
    owner: 查询关键词，默认空为显示全部
    blockchain: 默认 bitcoin  显示公链数据
    symbol: 默认 btc ,        显示token数据
    offset:开始行数（分页功能，从第几行开始取数据）
    limit: 本次提取数据行数
    retry_count: 网络重试次数
    Return
    ----------
    DataFrame
    timestamp   title         body
    """
    data = pd.DataFrame()
    if api_instance is None:
        api_instance = api()

    if limit > 500:
        limit = 500

    for _ in range(retry_count):
        try:
            api_name = "transaction"
            data = getattr(api_instance, api_name)(owner=owner, blockchain=blockchain, symbol=symbol, offset=offset,
                                     limit=limit)
            # reset index
            if data is not None and len(data.index) > 0 and "timestamp" in data.columns:
                # add to date
                data['date'] = pd.to_datetime(data['timestamp'], unit='s', utc=True, infer_datetime_format=True)
                data = data.reset_index(drop=True)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            error = "{}".format(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
            logger.error(error)
        else:
            return data


def defi(constract_address='', api_instance=None,
            offset=0,
            limit=500,
            retry_count=3):

    """
    defi 获取uniswap的交易记录
    Parameters:
    ------------
    constract_address: uniswap 合约地址
    offset:开始行数（分页功能，从第几行开始取数据）
    limit: 本次提取数据行数
    retry_count: 网络重试次数
    Return
    ----------
    DataFrame

    """
    data = pd.DataFrame()
    if api_instance is None:
        api_instance = api()

    if limit > 500:
        limit = 500

    for _ in range(retry_count):
        try:
            api_name = "defi"
            data = getattr(api_instance, api_name)(constract_address=constract_address, offset=offset, limit=limit)
            # reset index
            if data is not None and len(data.index) > 0:
                data = data.reset_index(drop=True)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            # error = "{}".format(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
            # print("------no  auth---------")
            # print(error)
            exc_value = str(exc_value).replace('Exception: ', '')
            error = json.loads(exc_value)
            if error.get('code') == '401':
                logger.error(error.get('message'))
                break
        else:
            return data


def info(api_instance=None, retry_count=3):

    """
    info 获取api支持信息
    Parameters:
    ------------
    retry_count: 网络重试次数
    Return
    ----------
    DataFrame
    timestamp   title         body
    """
    data = pd.DataFrame()
    if api_instance is None:
        api_instance = api()

    for _ in range(retry_count):
        try:
            api_name = "info"
            data = getattr(api_instance, api_name)()
            # reset index
            if data is not None:
                # add to date
                data['date'] = pd.to_datetime(data['timestamp'], unit='s', utc=True, infer_datetime_format=True)
                data = data.reset_index(drop=True)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            error = "{}".format(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
            logger.error(error)
        else:
            return data


if __name__ == '__main__':
    api_instance = api()

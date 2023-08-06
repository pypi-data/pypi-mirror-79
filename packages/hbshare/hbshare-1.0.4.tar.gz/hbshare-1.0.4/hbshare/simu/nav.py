#!/usr/bin/python
#coding:utf-8
from __future__ import division
import time
import pandas as pd
from hbshare.simu import cons as ct
import hbshare as hbs

"""
@author: Meng.lv
@contact: meng.lv@howbuy.com
@software: PyCharm
@file: nav.py.py
@time: 2020/9/18 9:18
"""

def get_simu_nav_by_code(code, start_date, end_date, retry_count=3, pause=0.01, timeout=10):
    """
        根据基金代码查询历史净值、累计净值、复权单位净值(分页需要单独处理)
    :param code:
    :return:
    """
    api = hbs.hb_api()
    for _ in range(retry_count):
        time.sleep(pause)
        ct._write_console()
        # 分页需要单独处理！！！！！！！！！！！！！
        url = ct.HOWBUY_SIMU_CORP_SEARCH % (ct.P_TYPE['https'], ct.DOMAINS['s'], code, start_date, end_date)
        org_js = api.query(url)
        total_count = int(org_js['totalCount'])

        if 'smgsContent' not in org_js or total_count <= 0:
            status = "未查询到数据"
            raise ValueError(status)

        data = org_js['smgsContent']
        corp_df = pd.DataFrame(data, columns=ct.HOWBUY_SIMU_CORP)
        corp_df['name'] = corp_df['tsname'].astype(basestring)
        corp_df['short_name'] = corp_df['tsshortName'].astype(basestring)
        corp_df['code'] = corp_df['tscode'].astype(basestring)
        return corp_df
    raise IOError(ct.NETWORK_URL_ERROR_MSG)
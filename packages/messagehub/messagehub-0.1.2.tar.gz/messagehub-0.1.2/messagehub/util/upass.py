# -*- coding:utf-8 -*-

"""
Created on 2020/08/07
@author: Xinqi Yang
@group : https://chaininout.com
@contact: xinqiyang@gmail.com
"""

import pandas as pd
import os

token_name = 'chaininout_token.csv'


def set_token(token):
    df = pd.DataFrame([token], columns=['token'])
    user_home = os.path.expanduser('~')
    fp = os.path.join(user_home, token_name)
    df.to_csv(fp, index=False)


def get_token():
    user_home = os.path.expanduser('~')
    fp = os.path.join(user_home, token_name)
    if os.path.exists(fp):
        df = pd.read_csv(fp)
        return str(df.loc[0]['token'])
    else:
        print("fetch token error")
        return None

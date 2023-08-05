#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : reverse_metrics
# @Time         : 2020/9/8 4:46 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


def get_num_pos_neg(num_sample, online_metric, metric='auc'):
    if metric == 'auc':
        num_pos = 1 / (2 * online_metric - 1)

    elif metric == 'f1':
        """f1
        提交一个正确的正样本(确保f1不为0)得到线上f1
        猜一个1其他全为0: 正样本数 = 2 / f1 - 1
        猜一个0其他全为1: 正样本数 = (总样本数 - 1) / (2 / f1 - 1)  # 概率更大
        """
        # 猜 0
        num_pos = (num_sample - 1) / (2 / online_metric - 1)

    num_neg = num_sample - num_pos
    print(f"num_pos/num_neg = 1 / {num_neg / num_pos}")
    print(f"{num_sample} = {num_pos} + {num_neg}")

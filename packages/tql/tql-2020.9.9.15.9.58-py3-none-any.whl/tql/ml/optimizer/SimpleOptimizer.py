#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : SimpleOptimizer
# @Time         : 2020/9/8 8:14 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import json
import optuna
import numpy as np

from optuna.samplers import TPESampler
from sklearn.metrics import f1_score


class SimpleOptimizer(object):

    def __init__(self, y_true, y_pred, trials=1):
        self.y_true = y_true
        self.y_pred = y_pred
        self.trials = trials
        self.sampler = TPESampler(seed=777)

    def objective(self, trial: optuna.trial.Trial):
        threshold = trial.suggest_discrete_uniform('threshold', 0.001, 1, 0.001)
        y_pred_ = np.where(self.y_pred > threshold, 1, 0)
        score = f1_score(self.y_true, y_pred_)
        return score


    def run(self, gc_after_trial=False, show_progress_bar=False):
        self.study = optuna.create_study(direction='maximize', sampler=self.sampler)
        self.study.optimize(
            self.objective,
            n_trials=self.trials,
            gc_after_trial=gc_after_trial,
            show_progress_bar=show_progress_bar
        )
        print(f"best_params:\n{json.dumps(self.study.best_params, indent=4)}")
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : Features
# @Time         : 2019-07-26 10:04
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : featuretools

import featuretools
import featuretools as ft
import featuretools.variable_types as vt

from featuretools.selection import remove_low_information_features
from tqdm.auto import tqdm
from tql.pipe import reduce_mem_usage


class AutoFeat(object):

    def __init__(self, df, entity_id, type2features, index=None, time_index=None, secondary_time_index=None):
        self.entity_id = entity_id  # 表名
        self.type2features = type2features

        self.es = ft.EntitySet(id='MAIN')
        self.es.entity_from_dataframe(
            entity_id=entity_id,
            dataframe=df.copy(),
            index='__id' if index is None else index,
            variable_types=self.variable_types,
            time_index=time_index,
            secondary_time_index=secondary_time_index
        )
        print(self.es)

    def dfs(self, target_entity, max_depth=1, features_only=True, n_jobs=1, chunk_size=None, ignore_variables=['uid']):
        """Deep Feature Synthesis"""

        for col in tqdm(self.normalize_entity_cols, desc='Normalize Entity'):
            self.es.normalize_entity(self.entity_id, col, col)

        return self.run_dfs(self.es, target_entity, max_depth, chunk_size, n_jobs, features_only, ignore_variables)

    def run_dfs(self, es, target_entity, max_depth, chunk_size, n_jobs, features_only, ignore_variables):
        _ = ft.dfs(
            entityset=es,
            target_entity=target_entity,
            max_depth=max_depth,
            verbose=1,
            chunk_size=chunk_size,
            n_jobs=n_jobs,
            ignore_variables={self.entity_id: ignore_variables},
            features_only=features_only,
        )

        if features_only:
            return _
        else:
            df_ = _[0].add_prefix(f'{self.entity_id}_').reset_index()
            df_ = reduce_mem_usage(df_)
            df_ = remove_low_information_features(df_)

            return df_

    @property
    def normalize_entity_cols(self):
        types = [vt.Id, vt.Categorical, vt.Boolean]
        cols = sum([self.type2features.get(type_, []) for type_ in types], [])
        return cols

    @property
    def variable_types(self):
        dic = {}
        for type_, features in self.type2features.items():
            dic.update(zip(features, len(features) * [type_]))
        return dic

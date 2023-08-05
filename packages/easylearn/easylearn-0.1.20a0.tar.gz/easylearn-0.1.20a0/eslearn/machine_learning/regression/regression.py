#!/usr/bin/env python 
# -*- coding: utf-8 -*-
"""
Author: Mengshi Dong <dongmengshi1990@163.com>
"""

import time
from sklearn import datasets
from sklearn.datasets import load_digits
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import make_scorer, mean_squared_error, mean_absolute_error, max_error

from eslearn.base import BaseMachineLearning
from eslearn.machine_learning.regression._base_regression import PipelineSearch_


x, y = datasets.make_regression(n_samples=200, n_informative=50, n_features=100, random_state=1)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.30, random_state=42)


class Regression(BaseMachineLearning, PipelineSearch_):
    
    def __init__(self):
        super(BaseMachineLearning, self).__init__()
        super(PipelineSearch_, self).__init__()
        self.search_strategy = 'grid'
        self.n_jobs = 2
        self.metric = mean_absolute_error

    def regression(self, 
                       x=None, 
                       y=None,
                       method_feature_preprocessing=None, 
                       param_feature_preprocessing=None,
                       method_dim_reduction=None,
                       param_dim_reduction=None,
                       method_feature_selection=None,
                       param_feature_selection=None,
                       method_machine_learning=None,
                       param_machine_learning=None,
    ):
        
        self.make_pipeline_(
            method_feature_preprocessing=method_feature_preprocessing, 
            param_feature_preprocessing=param_feature_preprocessing, 
            method_dim_reduction=method_dim_reduction, 
            param_dim_reduction=param_dim_reduction, 
            method_feature_selection=method_feature_selection,
            param_feature_selection=param_feature_selection,
            method_machine_learning=method_machine_learning, 
            param_machine_learning=param_machine_learning
        )
        
        self.fit_pipeline_(x_train, y_train)
        self.get_weights_(x_train, y_train)
        yhat = self.predict(x_test)
        score = self.metric(yhat, y_test)
        return yhat, score

    def run(self):
        self.get_configuration_(configuration_file=r'F:\Python378\Lib\site-packages\eslearn\GUI\test\configuration_file.json')
        self.get_preprocessing_parameters()
        self.get_dimension_reduction_parameters()
        self.get_feature_selection_parameters()
        self.get_unbalance_treatment_parameters()
        self.get_machine_learning_parameters()
        self.get_model_evaluation_parameters()
        
        method_feature_preprocessing = self.method_feature_preprocessing
        param_feature_preprocessing= self.param_feature_preprocessing

        method_dim_reduction = self.method_dim_reduction
        param_dim_reduction = self.param_dim_reduction

        method_feature_selection = self.method_feature_selection
        param_feature_selection = self.param_feature_selection

        method_machine_learning = self.method_machine_learning
        param_machine_learning = self.param_machine_learning
        
        yhat, score = self.regression(
            method_feature_preprocessing=method_feature_preprocessing, 
            param_feature_preprocessing=param_feature_preprocessing,
            method_dim_reduction=method_dim_reduction,
            param_dim_reduction=param_dim_reduction,
            method_feature_selection=method_feature_selection,
            param_feature_selection=param_feature_selection, 
            method_machine_learning=method_machine_learning, 
            param_machine_learning=param_machine_learning,
            x=x, 
            y=y
        )
        
        print(clf.param_search_)
        # print(clf.pipeline_)
        print(f"score = {score}")
        

if __name__ == "__main__":
    time_start = time.time()
    clf = Regression()
    clf.run()
    time_end = time.time()
    print(f"Running time = {time_end-time_start}\n")
    print("="*50)
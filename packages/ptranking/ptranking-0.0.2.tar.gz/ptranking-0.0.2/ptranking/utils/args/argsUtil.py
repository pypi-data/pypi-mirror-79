#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Description

"""

import argparse

class ArgsUtil(object):
    def __init__(self, given_root=None):
        self.args_parser = argparse.ArgumentParser('Run pt_ranking.')
        self.ini_l2r_args(given_root=given_root)

    def ini_l2r_args(self, given_root=None):
        self.given_root = given_root

        self.args_parser.add_argument('-gpu', action='store_true', help='using gpu device.')
        self.args_parser.set_defaults(apply_tl_af=True)

        #''' framework '''
        #self.args_parser.add_argument('-framework', default='adhoc', help='the specific learning-to-rank framework: adhoc | adversarial | gbdt')

        ''' data '''
        self.args_parser.add_argument('-data_id', help='the data collection upon which you will perform learning-to-rank.')
        self.args_parser.add_argument('-dir_data', help='the path where the data locates.')

        ''' output '''
        self.args_parser.add_argument('-dir_output', help='the output path of the results.')

        '''model-specific'''
        self.args_parser.add_argument('-model', help='specify the learning-to-rank method')

        self.args_parser.add_argument('-engine', help='specify the driving engine for LambdaMART, either XGBoost or LightGBM')

        """
        ''' train '''
        self.args_parser.add_argument('-num_epochs', type=int, default=100, help='the number of training epoches.')
        self.args_parser.add_argument('-validation', action='store_false', help='perform validation.')
        self.args_parser.set_defaults(validation=True)
        self.args_parser.add_argument('-validation_k', type=int, default=10, help='the cutoff value for validation.')
        self.args_parser.add_argument('-min_docs', type=int, default=10, help='the minimum size of a ltr_adhoc.')
        self.args_parser.add_argument('-min_rele', type=int, default=1, help='the minimum number of relevant documents per ltr_adhoc.')
        self.args_parser.add_argument('-binary', action='store_true', help='using binary standard relevance judgments.')
        self.args_parser.set_defaults(apply_tl_af=False)

        ''' score function '''
        self.args_parser.add_argument('-num_layers', type=int, default=1, help='the number of layers.')
        self.args_parser.add_argument('-hd_hn_af', default='S', help='the type of activation function for head & hidden layers.')
        self.args_parser.add_argument('-tl_af', default='S', help='the type of activation function for the final layer.')
        self.args_parser.add_argument('-apply_tl_af', action='store_false', help='perform activation for the final layer.')
        self.args_parser.set_defaults(apply_tl_af=True)

        

        ''' ApproxNDCG '''
        self.args_parser.add_argument('-approxNDCG_alpha', type=int, default=100, help='the alpha parameter of ApproxNDCG.')

        ''' WassRank '''
        """


    def update_if_required(self, args):
        #if args.root_output != self.given_root:
        #    args.dir_output = args

        return args

    def get_l2r_args(self):
        l2r_args = self.args_parser.parse_args()
        l2r_args = self.update_if_required(l2r_args)
        return l2r_args


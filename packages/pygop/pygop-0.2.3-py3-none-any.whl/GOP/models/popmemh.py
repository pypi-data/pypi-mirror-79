#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Fast Progressive Operational Perceptron with memory
https://arxiv.org/abs/1808.06377


Author: Dat Tran
Email: dat.tranthanh@tut.fi, viebboy@gmail.com
github: https://github.com/viebboy
"""

from __future__ import print_function

from ..utility import misc, gop_utils, gop_operators
from ._model import _Model
import shutil
import os
import copy
import pickle

CUDA_FLAG = 'CUDA_VISIBLE_DEVICES'


class POPmemH(_Model):
    """Progressive Operational Perceptron with Memory scheme H

    This class implements the POPmemH algorithm to learn a multilayer
    network of Generalized Operational Perceptron (GOP) in a progressive manner
    augmented by memory scheme H. The operator set search procedure is similar
    to POPfast. Difference between POPmemH and POPmemO is described in the
    original paper in the reference.

    reference: https://arxiv.org/abs/1808.06377

    Note:
        The model basically uses a python data generator mechanism to feed the data
        Thus, the data should be prepared with the following format:
            train_func: a function that returns (data_generator, number of steps)
                        the user specifies how data is loaded and preprocess by giving
                        the definition of the data generator and the number of steps (number of mini-batches)
            train_data: the input to 'train_func'
                        this can be filepath to the data on disk

        When the model generates the data, the generator and #steps are retrieved by
        calling:
            gen, steps = train_func(train_data)

        And next(gen) should produce a mini-batch of (x,y) in case of fit()/evaluate()
        or only x in case of predict()

        See documentation page for example how to define such train_func and train_data


    Examples:
        >>> from GOP import models
        >>> model = models.POPmemH() # create a model instance
        >>> params = model.get_default_parameters() # get default parameters (PCA as memory path)

        # fit the model with data using train_func, train_data (see above in Note)
        >>> performance, progressive_history, finetune_history = model.fit(params, train_func, train_data)

        # evaluate model with test data (test_func, test_data) using a list of metrics
        # and special_metrics (those require full batch evaluation such as F1, Precision, Recall...)
        # using either CPU or GPU as computation environment,
        # e.g. computation=('cpu',) -> using cpu
        # e.g. computation=('gpu', [0,1]) -> using gpu with GPU0, GPU1

        >>> model.evaluate(test_func, test_data, metrics, special_metrics, computation)

        # generate prediction with (test_func, test_data)
        >>> model.predict(test_func, test_data, computation)

        # save model to 'popmemh.pickle'
        >>> model.save('popmemh.pickle')

        # load model from 'popmemh.pickle' and finetune with another data and
        # (possibly different) parameter settings
        >>> model.load('popmemh.pickle')
        >>> history, performance = model.finetune(params, another_train_func, another_train_data)

        See documentation page for detail usage and explanation


    """

    def __init__(self, *args, **kargs):
        self.model_data = None
        self.model_data_attributes = ['model',
                                      'topology',
                                      'op_sets',
                                      'weights',
                                      'output_activation',
                                      'use_bias']

        self.model_name = 'POPmemH'

        return

    def get_default_parameters(self,):

        params = {'memory_regularizer': 1e-1,
                  'memory_type': 'PCA',
                  'min_energy_percentage': 0.98,
                  'layer_threshold': 1e-4,
                  'metrics': ['mse', ],
                  'convergence_measure': 'mse',
                  'direction': 'lower',
                  'output_activation': None,
                  'loss': 'mse',
                  'max_topology': [40, 40, 40, 40],
                  'weight_regularizer': None,
                  'weight_regularizer_finetune': None,
                  'weight_constraint': 2.0,
                  'weight_constraint_finetune': 2.0,
                  'lr_train': (1e-3, 1e-4, 1e-5),
                  'epoch_train': (2, 2, 2),
                  'lr_finetune': (1e-3, 1e-4, 1e-5),
                  'epoch_finetune': (2, 2, 2),
                  'input_dropout': None,
                  'dropout': 0.2,
                  'dropout_finetune': 0.2,
                  'optimizer': 'adam',
                  'optimizer_parameters': None,
                  'nodal_set': gop_operators.get_default_nodal_set(),
                  'pool_set': gop_operators.get_default_pool_set(),
                  'activation_set': gop_operators.get_default_activation_set(),
                  'direct_computation': False,
                  'cluster': False,
                  'special_metrics': None,
                  'search_computation': ('cpu', 8),
                  'finetune_computation': ('cpu', 8),
                  'use_bias': True,
                  'class_weight': None}

        return params

    def check_parameters(self, params):

        if 'memory_type' in params.keys():
            assert params['memory_type'] in [
                'PCA', 'LDA'], 'Only support 2 memory types "PCA" and "LDA", given %s' % params['memory_type']

        if params['memory_type'] == 'PCA':
            if 'min_energy_percentage' in params.keys():
                msg = 'Minimum energy to keep in PCA must be nonzero and less than 1, given '
                msg += str(params['min_energy_percentage'])
                assert params['min_energy_percentage'] > 0 and params['min_energy_percentage'] < 1.0, msg

        params = misc.check_model_parameters(params, self.get_default_parameters())

        return params

    def fit(self,
            params,
            train_func,
            train_data,
            val_func=None,
            val_data=None,
            test_func=None,
            test_data=None,
            verbose=False):

        if verbose:
            print('Start progressive learning')

        p_history = self.progressive_learn(params,
                                           train_func,
                                           train_data,
                                           val_func,
                                           val_data,
                                           test_func,
                                           test_data,
                                           verbose)

        if verbose:
            print('Start finetuning')

        f_history, performance = self.finetune(params,
                                               train_func,
                                               train_data,
                                               val_func,
                                               val_data,
                                               test_func,
                                               test_data,
                                               verbose)

        if os.path.exists(os.path.join(params['tmp_dir'], params['model_name'])):
            shutil.rmtree(os.path.join(params['tmp_dir'], params['model_name']))

        return performance, p_history, f_history

    def progressive_learn(self,
                          params,
                          train_func,
                          train_data,
                          val_func=None,
                          val_data=None,
                          test_func=None,
                          test_data=None,
                          verbose=False):

        params = self.check_parameters(params)

        original_convergence_measure = params['convergence_measure']
        if val_func:
            params['convergence_measure'] = 'val_' + params['convergence_measure']
        else:
            params['convergence_measure'] = 'train_' + params['convergence_measure']

        misc.test_generator(train_func, train_data, params['input_dim'], params['output_dim'])
        if val_func:
            misc.test_generator(val_func, val_data, params['input_dim'], params['output_dim'])
        if test_func:
            misc.test_generator(test_func, test_data, params['input_dim'], params['output_dim'])

        train_states = misc.initialize_states(params, self.model_name)

        if not train_states['is_finished']:
            for layer_iter in range(train_states['layer_iter'], len(params['max_topology'])):

                if verbose:
                    print('-------------Layer %d ------------------' % layer_iter)

                if layer_iter > 0:
                    train_states['topology'].pop()

                train_states['topology'].append([])
                train_states['topology'].append(('dense', params['output_dim']))

                train_states['history'].append([])
                train_states['measure'].append([])

                if verbose:
                    print('-------------Layer %d ------------------' % layer_iter)

                if verbose:
                    print('##### Iterative Search #####')

                if params['cluster']:
                    search_routine = gop_utils.search_cluster
                else:
                    if params['search_computation'][0] == 'cpu':
                        search_routine = gop_utils.search_cpu
                    else:
                        search_routine = gop_utils.search_gpu

                if verbose:
                    print('##### GISfast #####')

                block_performance, block_weights, block_op_set_idx, history = search_routine(params,
                                                                                             train_states,
                                                                                             train_func,
                                                                                             train_data,
                                                                                             val_func,
                                                                                             val_data,
                                                                                             test_func,
                                                                                             test_data)

                if verbose:
                    self.print_performance(
                        history, params['convergence_measure'], params['direction'])

                train_states['measure'][layer_iter].append(
                    block_performance[params['convergence_measure']])
                train_states['history'][layer_iter].append(history)

                if layer_iter > 0:
                    if misc.check_convergence(train_states['measure'][layer_iter][-1], train_states['measure']
                                              [layer_iter - 1][-1], params['direction'], params['layer_threshold']):
                        train_states['topology'].pop(-2)
                        train_states['topology'][-2].pop(-1)

                        suffix = '_' + str(layer_iter - 1) + '_1'
                        del train_states['weights']['mem_pre_bn' + suffix]
                        del train_states['weights']['mem' + suffix]
                        del train_states['weights']['bn' + suffix]
                        del train_states['history'][-1]

                        train_states['weights']['output'] = train_states['output_weight']

                        break

                train_states['topology'].pop(-2)

                if verbose:
                    print('##### Calculating memory block ########')

                pre_bn_weight, projection, post_bn_weight = gop_utils.calculate_memory_block_standalone(params,
                                                                                                        train_states,
                                                                                                        train_func,
                                                                                                        train_data,
                                                                                                        val_func,
                                                                                                        val_data,
                                                                                                        test_func,
                                                                                                        test_data)
                train_states['topology'].pop()
                train_states['topology'].append([])
                train_states['topology'].append(('dense', params['output_dim']))

                if 'output' in train_states['weights'].keys():
                    train_states['output_weight'] = copy.deepcopy(train_states['weights']['output'])
                else:
                    train_states['output_weight'] = block_weights[-1]

                suffix = '_' + str(layer_iter) + '_0'
                train_states['topology'][-2].append(('gop', params['max_topology'][layer_iter]))
                train_states['op_set_indices']['gop' + suffix] = block_op_set_idx
                train_states['weights']['gop' + suffix] = block_weights[0]
                train_states['weights']['bn' + suffix] = block_weights[1]
                train_states['weights']['output'] = block_weights[2]

                if layer_iter != len(params['max_topology']) - 1:
                    suffix = '_' + str(layer_iter) + '_1'
                    train_states['topology'][-2].append(('mem', projection[0].shape[1]))
                    train_states['weights']['mem_pre_bn' + suffix] = pre_bn_weight
                    train_states['weights']['mem' + suffix] = projection
                    train_states['weights']['bn' + suffix] = post_bn_weight

                train_states['layer_iter'] += 1

            train_states['is_finished'] = True
            path = os.path.join(params['tmp_dir'], params['model_name'], 'train_states.pickle')
            with open(path, 'wb') as fid:
                pickle.dump(train_states, fid)

        model_data = {'model': self.model_name,
                      'topology': train_states['topology'],
                      'op_sets': misc.map_operator_from_index(train_states['op_set_indices'],
                                                              params['nodal_set'],
                                                              params['pool_set'],
                                                              params['activation_set']),
                      'weights': train_states['weights'],
                      'use_bias': train_states['use_bias'],
                      'output_activation': train_states['output_activation']}

        self.model_data = model_data
        params['convergence_measure'] = original_convergence_measure

        return train_states['history']

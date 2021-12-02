#! -*- coding: utf-8 -*-
# CLUE评测
# 模型配置文件

import os
from bert4keras.backend import keras, K
from bert4keras.tokenizers import Tokenizer
from bert4keras.models import build_transformer_model
from bert4keras.optimizers import AdaFactor
from bert4keras.optimizers import extend_with_gradient_accumulation

# 通用参数
data_path = '/root/clue/datasets/'
learning_rate = 5e-4
pooling = 'first'

# 权重目录
if not os.path.exists('weights'):
    os.mkdir('weights')

# 输出目录
if not os.path.exists('results'):
    os.mkdir('results')

# 模型路径
config_path = '/root/kg/bert/chinese_L-12_H-768_A-12/bert_config.json'
checkpoint_path = '/root/kg/bert/chinese_L-12_H-768_A-12/bert_model.ckpt'
dict_path = '/root/kg/bert/chinese_L-12_H-768_A-12/vocab.txt'

# 建立分词器
tokenizer = Tokenizer(dict_path, do_lower_case=True)

# 预训练模型
base = build_transformer_model(
    config_path, checkpoint_path, application='unilm', return_keras_model=False
)

# 模型参数
last_layer = 'Transformer-%s-FeedForward-Norm' % (base.num_hidden_layers - 1)

if pooling == 'first':
    pooling_layer = keras.layers.Lambda(lambda x: x[:, 0])
elif pooling == 'avg':
    pooling_layer = keras.layers.GlobalAveragePooling1D()
elif pooling == 'max':
    pooling_layer = keras.layers.GlobalMaxPooling1D()

# 优化器
AdaFactorG = extend_with_gradient_accumulation(AdaFactor, name='AdaFactorG')

optimizer = AdaFactor(
    learning_rate=learning_rate, beta1=0.9, min_dim_size_to_factor=10**6
)

optimizer2 = AdaFactorG(
    learning_rate=learning_rate,
    beta1=0.9,
    min_dim_size_to_factor=10**6,
    grad_accum_steps=2
)

optimizer4 = AdaFactorG(
    learning_rate=learning_rate,
    beta1=0.9,
    min_dim_size_to_factor=10**6,
    grad_accum_steps=4
)

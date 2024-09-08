# encoding: utf-8
from __future__ import unicode_literals

import unittest
import numpy as np
from keras_transformer import transformer as tfr

import sys
sys.path.append(".")# encoding: utf-8

import os
os.environ['TF_KERAS'] =  '1'

import re
def readData(data_path, num_samples=10000):
  with open(data_path, 'r', encoding='utf-8') as f:
    lines = f.read().split('\n')
  input_texts = []
  target_texts = []
  for line in lines[: min(num_samples, len(lines) - 1)]:
    input_text, target_text = line.split('\t')
    
    input_text= re.findall(r'[.!@#$%^&*()\+\-\*/]|\w+', input_text)
    input_texts.append(input_text)
    target_texts.append(list(target_text))
  return input_texts, target_texts

class TestTranslate(unittest.TestCase):

    @staticmethod
    def _build_token_dict(token_list):
        token_dict = {
            '<PAD>': 0,
            '<START>': 1,
            '<END>': 2,
        }
        for tokens in token_list:
            for token in tokens:
                if token not in token_dict:
                    token_dict[token] = len(token_dict)
        return token_dict

    def test_translate(self):
        '''
        source_tokens = [
            'i need more power'.split(' '),
            'eat jujube and pill'.split(' '),
        ]
        target_tokens = [
            list('我要更多的抛瓦'),
            list('吃枣💊'),
        ]
        '''
        source_tokens, target_tokens = readData("./cmn.txt")
        # Generate dictionaries
        source_token_dict = self._build_token_dict(source_tokens)
        target_token_dict = self._build_token_dict(target_tokens)
        target_token_dict_inv = {v: k for k, v in target_token_dict.items()}

        # Add special tokens
        encode_tokens = [['<START>'] + tokens + ['<END>'] for tokens in source_tokens]
        decode_tokens = [['<START>'] + tokens + ['<END>'] for tokens in target_tokens]
        output_tokens = [tokens + ['<END>', '<PAD>'] for tokens in target_tokens]

        # Padding
        source_max_len = max(map(len, encode_tokens))
        target_max_len = max(map(len, decode_tokens))

        encode_tokens = [tokens + ['<PAD>'] * (source_max_len - len(tokens)) for tokens in encode_tokens]
        decode_tokens = [tokens + ['<PAD>'] * (target_max_len - len(tokens)) for tokens in decode_tokens]
        output_tokens = [tokens + ['<PAD>'] * (target_max_len - len(tokens)) for tokens in output_tokens]

        encode_input = [list(map(lambda x: source_token_dict[x], tokens)) for tokens in encode_tokens]
        decode_input = [list(map(lambda x: target_token_dict[x], tokens)) for tokens in decode_tokens]
        decode_output = [list(map(lambda x: [target_token_dict[x]], tokens)) for tokens in output_tokens]

        # Build & fit model
        model = tfr.get_model(
            token_num=max(len(source_token_dict), len(target_token_dict)),
            embed_dim=32,
            encoder_num=2,
            decoder_num=2,
            head_num=4,
            hidden_dim=128,
            dropout_rate=0.05,
            use_same_embed=False,  # Use different embeddings for different languages
        )
        model.compile('adam', 'sparse_categorical_crossentropy')
        model.summary()
        model.fit(
            x=[np.array(encode_input), np.array(decode_input)],
            y=np.array(decode_output),
            epochs=5,
            batch_size=32,
        )

        # Predict
        number_sentence = 4
        for sentence_idx in range(number_sentence):
          decoded = tfr.decode(
              model,
              #encode_input[0:number_sentence],
              encode_input[sentence_idx:sentence_idx+1],
              start_token=target_token_dict['<START>'],
              end_token=target_token_dict['<END>'],
              pad_token=target_token_dict['<PAD>'],
        )
        for i in range(len(decoded)):
            standard = ''.join(target_tokens[sentence_idx])
            predicted = ''.join(map(lambda x: target_token_dict_inv[x], decoded[i][1:-1]))
            print('標準答案', '',standard)
            print( '預測答案', predicted)
        
        text = standard
        repeat = []                             # 新增 repeat 變數為空串列
        not_repeat = [] 

        for i in text:                          # 使用 for 迴圈，依序取出每個字元
            a = text.count(i, 0, len(text))     # 判斷字元在字串中出現的次數
            if a>1 and i not in repeat:         # 如果次數大於 1，且沒有存在 repeat 串列中
                repeat.append(i)                  # 將字元加入 repeat 串列
            if a == 1 and i not in not_repeat:   # 如果次數等於 1，且沒有存在 not_repeat 串列中
                not_repeat.append(i)              # 將字元加入 not_repeat 串列
        print(repeat)
        print(not_repeat)

x=TestTranslate()
x.test_translate()

# Copyright 2020 Tobias Höfer
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
"""Both convolutional and recurrent operations are building blocks that process
one local neighborhood at a time. In this paper, we present non-local operations
as a generic family of building blocks for capturing long-range dependencies.
Inspired by the classical non-local means method in computer vision,
our non-local operation computes the response at a position as a weighted sum of
the features at all positions. This building block can be plugged into many
computer vision architectures.

Paper: https://arxiv.org/abs/1711.07971, https://arxiv.org/abs/1805.08318
TODO(visualize attention maps)
"""

import tensorflow as tf


class AttentionBlock(tf.keras.layers.Layer):
    """Self-Attention Block."""
    def __init__(self, reduction_ratio=8, visualize_attention_map=False):
        super(AttentionBlock, self).__init__()
        self.reduction_ratio = reduction_ratio
        self.visualize_attention_map = visualize_attention_map
        # Scale parameter which is multiplied to attention map.
        self.gamma = tf.get_variable("gamma", [1],
                                     initializer=tf.constant_initializer(0.0))

    def build(self, input_shape):
        self.filter_size = input_shape[3]
        self.input_shape = input_shape.shape
        self.f = tf.keras.layers.Conv2D(filters=self.filter_size /
                                        self.reduction_ratio,
                                        kernel_size=(1, 1),
                                        strides=(1, 1),
                                        use_bias=False)
        self.g = tf.keras.layers.Conv2D(filters=self.filter_size /
                                        self.reduction_ratio,
                                        kernel_size=(1, 1),
                                        strides=(1, 1),
                                        use_bias=False)
        self.h = tf.keras.layers.Conv2D(filters=self.filter_size /
                                        self.reduction_ratio,
                                        kernel_size=(1, 1),
                                        strides=(1, 1),
                                        use_bias=False)

    def call(self, input):
        # C = Channels; C´= C/reduction_ratio; N = Width * Height
        # Query: 1x1 conv to transform x to feature space f.
        query = self.f(input)  # [bs, h, w, c']
        # Key:  1x1 conv to transform x to feature space g.
        key = self.g(input)  # [bs, h, w, c']
        # Value: 1x1 conv to transform x to feature space h.
        value = self.h(input)  # [bs, h, w, c']

        # Score function for feature similarity (dot product).
        attention_map = tf.matmul(self._hw_flatten(query),
                                  self._hw_flatten(key),
                                  transpose_a=True)  # [bs, N, N]
        # Softmax activation (NxN).
        attention_map = tf.nn.softmax(attention_map)  # [bs, N, N]

        o = tf.matmul(attention_map, self._hw_flatten(value))  # [bs, N, C]

        o = tf.reshape(o, shape=self.input_shape)  # [bs, h, w, C]

        # Add attention map to input.
        x = self.gamma * o + input

        return x

    @staticmethod
    def _hw_flatten(x):
        return tf.reshape(x, shape=[x.shape[0], -1, x.shape[-1]])

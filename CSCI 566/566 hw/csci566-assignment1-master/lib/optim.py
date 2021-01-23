from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np


""" Super Class """
class Optimizer(object):
    """
    This is a template for implementing the classes of optimizers
    """
    def __init__(self, net, lr=1e-4):
        self.net = net  # the model
        self.lr = lr    # learning rate

    """ Make a step and update all parameters """
    def step(self):
        #### FOR RNN / LSTM ####
        if hasattr(self.net, "preprocess") and self.net.preprocess is not None:
            self.update(self.net.preprocess)
        if hasattr(self.net, "rnn") and self.net.rnn is not None:
            self.update(self.net.rnn)
        if hasattr(self.net, "postprocess") and self.net.postprocess is not None:
            self.update(self.net.postprocess)

        #### MLP ####
        if not hasattr(self.net, "preprocess") and \
           not hasattr(self.net, "rnn") and \
           not hasattr(self.net, "postprocess"):
            for layer in self.net.layers:
                self.update(layer)


""" Classes """
class SGD(Optimizer):
    """ Some comments """
    def __init__(self, net, lr=1e-4):
        self.net = net
        self.lr = lr

    def update(self, layer):
        for n, dv in layer.grads.items():
            layer.params[n] -= self.lr * dv


class SGDM(Optimizer):
    """ Some comments """
    def __init__(self, net, lr=1e-4, momentum=0.0):
        self.net = net
        self.lr = lr
        self.momentum = momentum
        self.velocity = {}  # last update of the velocity

    def update(self, layer):
        #############################################################################
        # TODO: Implement the SGD + Momentum                                        #
        #############################################################################
        for n, v in layer.params.items():
            velocity = self.momentum * self.velocity.get(n,0) - layer.grads[n] * self.lr
            self.velocity[n] = velocity
            layer.params[n] += velocity
        #############################################################################
        #                             END OF YOUR CODE                              #
        #############################################################################


class RMSProp(Optimizer):
    """ Some comments """
    def __init__(self, net, lr=1e-2, decay=0.99, eps=1e-8):
        self.net = net
        self.lr = lr
        self.decay = decay
        self.eps = eps
        self.cache = {}  # decaying average of past squared gradients

    def update(self, layer):
        #############################################################################
        # TODO: Implement the RMSProp                                               #
        #############################################################################
        for n, v in layer.params.items():
            grad = layer.grads[n]
            average_decay = self.decay * self.cache.get(n,0) + (1 - self.decay) * grad**2
            layer.params[n] -= (self.lr * grad)/np.sqrt(average_decay + self.eps)
            self.cache[n] = average_decay
        #############################################################################
        #                             END OF YOUR CODE                              #
        #############################################################################


class Adam(Optimizer):
    """ Some comments """
    def __init__(self, net, lr=1e-3, beta1=0.9, beta2=0.999, t=0, eps=1e-8):
        self.net = net
        self.lr = lr
        self.beta1, self.beta2 = beta1, beta2
        self.eps = eps
        self.mt = {}
        self.vt = {}
        self.t = t

    def update(self, layer):
        #############################################################################
        # TODO: Implement the Adam                                                  #
        #############################################################################
        for n, v in layer.params.items():
            m_t = self.beta1 * self.mt.get(n,0) + (1 - self.beta1) * layer.grads[n]
            v_t = self.beta2 * self.vt.get(n,0) + (1 - self.beta2) * layer.grads[n]**2
            self.mt[n] = m_t
            self.vt[n] = v_t
            self.t += 1
            m_t_1 = m_t/(1 - self.beta1**(self.t))
            v_t_1 = v_t/(1 - self.beta2**(self.t))

            layer.params[n] -= (self.lr * m_t_1)/(np.sqrt(v_t_1) + self.eps)
        #############################################################################
        #                             END OF YOUR CODE                              #
        #############################################################################

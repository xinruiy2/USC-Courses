import argparse
import numpy as np
import os
import sys
import csv
import json

class softmax_cross_entropy:
    def __init__(self):
        self.expand_Y = None
        self.calib_logit = None
        self.sum_exp_calib_logit = None
        self.prob = None

    def forward(self, X, Y):
        self.expand_Y = np.zeros(X.shape).reshape(-1)
        self.expand_Y[Y.astype(int).reshape(-1) + np.arange(X.shape[0]) * X.shape[1]] = 1.0
        self.expand_Y = self.expand_Y.reshape(X.shape)

        self.calib_logit = X - np.amax(X, axis = 1, keepdims = True)
        self.sum_exp_calib_logit = np.sum(np.exp(self.calib_logit), axis = 1, keepdims = True)
        self.prob = np.exp(self.calib_logit) / self.sum_exp_calib_logit

        forward_output = - np.sum(np.multiply(self.expand_Y, self.calib_logit - np.log(self.sum_exp_calib_logit))) / X.shape[0]
        return forward_output

    def backward(self, X, Y):
        backward_output = - (self.expand_Y - self.prob) / X.shape[0]
        return backward_output

def predict_label(f):
    if f.shape[1] == 1:
        return (f > 0).astype(float)
    else:
        return np.argmax(f, axis=1).astype(float).reshape((f.shape[0], -1))

class linear_layer:
    def __init__(self, input_D, output_D):
        self.params = dict()
        self.params['W'] = np.random.normal(loc = 0.0, scale = 0.1,size = (input_D, output_D))
        self.params['b'] = np.random.normal(loc = 0.0, scale = 0.1,size = (1, output_D))
        self.gradient = dict()
        self.gradient['W'] = np.zeros((input_D, output_D))
        self.gradient['b'] = np.zeros((1,output_D))

    def forward(self, X):
        forward_output = X @ self.params['W'] + self.params['b']
        return forward_output

    def backward(self, X, grad):
        self.gradient['W'] = X.T @ grad
        self.gradient['b'] = np.sum(grad, axis = 0, keepdims = True)
        return grad@(self.params['W'].T)



class relu:
    def __init__(self):
        self.mask = None

    def forward(self, X):
        forward_output = X.copy()
        forward_output[np.where(forward_output < 0)] = 0
        self.mask = forward_output
        return forward_output

    def backward(self, X, grad):
        self.mask[np.where( self.mask > 0 )] = 1
        return grad * self.mask


class dropout:
    def __init__(self):
        self.mask = None

    def forward(self, X, is_train):

        if is_train:
            self.mask = (np.random.uniform(0.0, 1.0, X.shape) >= 0).astype(float) * (1.0 / (1.0))
        else:
            self.mask = np.ones(X.shape)
        forward_output = np.multiply(X, self.mask)
        return forward_output

    def backward(self, X, grad):
        return grad * self.mask


def miniBatchStochasticGradientDescent(model):
    for module_name, module in model.items():
        if hasattr(module, 'params'):
            for key, _ in module.params.items():
                g = module.gradient[key]
                module.params[key] -= module.gradient[key] * 0.01

    return model

def cvs_to_list(file_name):
    ret = []
    with open(file_name) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            ret.append(row)
    return np.asarray(ret)

def main(arguments):

    try:
        os.remove("test_predictions.csv")
    except OSError:
        pass

    Xtrain = cvs_to_list(arguments[0]) #train input
    Xval = cvs_to_list(arguments[1]) #train label
    Ytest = cvs_to_list(arguments[2]) #test input
    # Yval = cvs_to_list(arguments[3])

    Xtrain = Xtrain.astype('float64')
    Xval = Xval.astype('float64')
    Ytest = Ytest.astype('float64')
    # Yval = Yval.astype('float64')

    Xtrain = Xtrain/255
    Ytest = Ytest/255

    N_train, d = Xtrain.shape

    train_data = Xtrain
    train_label = Xval


    model = dict()

    model['L1'] = linear_layer(input_D = d, output_D = 1000)
    model['nonlinear1'] = relu()
    model['drop1'] = dropout()
    model['L2'] = linear_layer(input_D = 1000, output_D = 10)
    model['loss'] = softmax_cross_entropy()

    for t in range(5):
        print('At epoch ' + str(t + 1))

        for i in range(int(np.floor(N_train / 10))):

            x,y = train_data[i*10 : (i+1) * 10], train_label[i*10 : (i+1) * 10]

            #forward
            a1 = model['L1'].forward(x)
            h1 = model['nonlinear1'].forward(a1)
            d1 = model['drop1'].forward(h1, is_train = True)
            a2 = model['L2'].forward(d1)
            loss = model['loss'].forward(a2, y)

            ### backward ###
            grad_a2 = model['loss'].backward(a2, y)
            grad_d1 = model['L2'].backward(d1, grad_a2)
            grad_h1 = model['drop1'].backward(h1 ,grad_d1)
            grad_a1 = model['nonlinear1'].backward(a1,grad_h1)

            grad_x = model['L1'].backward(x, grad_a1)
            model = miniBatchStochasticGradientDescent(model)


    x = Ytest

    a1 = model['L1'].forward(x)
    h1 = model['nonlinear1'].forward(a1)
    d1 = model['drop1'].forward(h1, is_train = False)
    a2 = model['L2'].forward(d1)

    correct_count = 0
    f_1 = open("test_predictions.csv", "w")
    for i in range(predict_label(a2).shape[0]):
        # if predict_label(a2)[i][0] == Yval[i][0]:
        #     correct_count += 1
        f_1.write(str(int(predict_label(a2)[i][0])))
        f_1.write('\n')
    f_1.close()
    #
    # print("finished" + str(correct_count/Ytest.shape[0]))

if __name__ == "__main__":
    main(sys.argv[1:])

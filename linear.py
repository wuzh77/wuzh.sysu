from IPython import display
from matplotlib import pyplot as plt
from mxnet import autograd, nd
import random
import numpy


def generate_data():
    num_input = 2
    num_examples = 1000
    true_w = [2, -3.4]
    true_b = 4.2
    features = nd.random.normal(scale=1, shape=(num_examples, num_input))
    labels = true_w[0] * features[:, 0] + true_w[1] * features[:, 1] + true_b
    labels += nd.random.normal(scale=0.01, shape=labels.shape)
    return features, labels


class my_linear:
    def __init__(self, data_in, input_labels, batch_size=10):
        self.feagures = data_in
        self.labels = input_labels
        self.num_size = data_in.shape[0]
        self.num_input = data_in.shape[1]
        self.w = nd.random.normal(scale=0.01, shape=(self.num_input, 1))
        self.b = nd.zeros(shape=(1,))
        self.w.attach_grad()
        self.b.attach_grad()
        self.batch_size = batch_size

    def read_data(self, batch_size, feagures, label):
        num_example = len(feagures)
        indices = list(range(num_example))
        random.shuffle(indices)
        for i in range(0, num_example, batch_size):
            j = nd.array(indices[i:min(i + batch_size, num_example)])
            yield feagures.take(j), label.take(j)

    def predict_y(self, X, w, b):
        return nd.dot(X, w) + b

    def squared_loss(self, y_pre, y):
        return (y_pre - y.reshape(y_pre.shape)) ** 2 / 2

    def improve(self, params, lr, batch_size):
        for parm in params:
            parm[:] = parm - lr * parm.grad / batch_size

    def train_mode(self, epoch, lr=0.03):
        num_epoch = epoch
        my_lr = lr
        for cnt in range(num_epoch):
            for X, y in self.read_data(self.batch_size, self.feagures, self.labels):
                with autograd.record():
                    l = self.squared_loss(self.predict_y(X, self.w, self.b), y)
                l.backward()
                self.improve([self.w, self.b], my_lr, self.batch_size)


if __name__ == "__main__":
    feature, label = generate_data()
    linear = my_linear(feature, label, 10)
    linear.train_mode(5)
    print(linear.w)
    print(linear.b)

from mxnet import autograd, nd
from mxnet.gluon import data as gdata
from mxnet.gluon import nn
from mxnet import init
from mxnet import gluon
from mxnet.gluon import loss as gloss


def generate_data():  # 生成数据集
    num_inputs = 2  # 定义w维数
    num_examples = 1000  # 定义输入数据集的大小
    true_w = [2, -3.4]  # w的实际值
    true_b = 4.2  # b的实际值
    features = nd.random.normal(scale=1, shape=(num_examples, num_inputs))  # 此处随机生成数据集张量,生成均值为0，标准差为1的正态分布
    labels = true_w[0] * features[:, 0] + true_w[1] * features[:, 1] + true_b  # 计算标签的值
    labels += nd.random.normal(scale=0.01, shape=labels.shape)  # 加上干扰量
    return features, labels


def read_data(features, labels):  # 读取数据
    batch_size = 10  # 定义一次取数多少
    dataset = gdata.ArrayDataset(features, labels)
    data_iter = gdata.DataLoader(dataset, batch_size, shuffle=True)
    return data_iter


def generate_model():  # 定义模型，并且进行初始化
    net = nn.Sequential()
    net.add(nn.Dense(1))
    net.initialize(init.Normal(sigma=0.01))  # 初始化为均值为0，标准差为0.01的正态分布
    return net


def train_model():
    num_epochs = 100
    features, label = generate_data() #生成数据集和标签
    loss = gloss.L2Loss() #定义loss计算平方损失
    my_net = generate_model() #产生
    trainer = gluon.Trainer(my_net.collect_params(), 'sgd', {'learning_rate': 0.01})
    data_iter = read_data(features, label)
    batch_size = 10
    for epoch in range(1, num_epochs + 1):
        for X, y in data_iter:
            with autograd.record():
                l = loss(my_net(X), y)
            l.backward()
            trainer.step(batch_size)
        l = loss(my_net(features), label)
        print('epoch %d, loss: %f' % (epoch, l.mean().asnumpy()))
    dense = my_net[0]
    print("权重为：" + str(dense.weight.data()))
    print("改变量为：" + str(dense.bias.data()))


if __name__ == "__main__":
    train_model()

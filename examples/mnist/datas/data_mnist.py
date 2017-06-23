# coding: utf-8
import lake
from torchvision import datasets

class DataMnist(object):
	def __init__(self, opt):
		self.opt = opt

	def load(self):
		mnist_train = datasets.MNIST(self.opt.data_dir, train=True, download=True)
		mnist_test = datasets.MNIST(self.opt.data_dir, train=False, download=True)
		train = lake.array.Shuffler(mnist_train['train_data'].numpy(), mnist_train['train_labels'].numpy())
		test = lake.array.Shuffler(mnist_test['test_data'].numpy(), mnist_test['test_labels'].numpy())
		return (train, test)
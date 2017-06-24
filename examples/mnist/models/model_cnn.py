# coding: utf-8
import lake.torch
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np


class ModelCNNBase(torch.nn.Module):
	def __init__(self, opt):
		super(ModelCNNBase, self).__init__()
		self.opt = opt
		self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
		self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
		self.conv2_drop = nn.Dropout2d()
		self.fc1 = nn.Linear(320, 50)
		self.fc2 = nn.Linear(50, 10)

	def forward(self, x, training=True):
		x = F.relu(F.max_pool2d(self.conv1(x), 2))
		x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
		x = x.view(-1, 320)
		x = F.relu(self.fc1(x))
		x = F.dropout(x, training=self.training)
		x = self.fc2(x)
		return F.log_softmax(x)


class ModelCNN(lake.torch.network.Base):
	def __init__(self, opt):
		super(ModelCNN, self).__init__()
		self.opt = opt
		self.model = ModelCNNBase(opt)
		self.critera = F.nll_loss

	def run(self, data, is_train=True):
		x, y = data
		x = torch.FloatTensor(x.astype(np.float32))
		y = torch.from_numpy(y)
		if self.use_cuda:
			x, y = x.cuda(), y.cuda()
		x, y = Variable(x, volatile=not is_train), Variable(y)
		output = self.forward(x)
		error = self.critera(output, y)
		if is_train:
			return dict(loss=error)
		else:
			return dict(loss=float(error.data[0]))

	def train(self, data):
		return self.run(data)

	def test(self, data):
		return self.run(data, False)


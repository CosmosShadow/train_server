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
		self.conv1 = nn.Conv2d(1, 16, kernel_size=5, padding=2)
		self.conv2 = nn.Conv2d(16, 32, kernel_size=5, padding=2)
		self.fc1 = nn.Linear(32*7*7, 64)
		self.fc2 = nn.Linear(64, 10)

	def forward(self, x):
		x = F.relu(F.max_pool2d(self.conv1(x), 2))
		x = F.relu(F.max_pool2d(self.conv2(x), 2))
		x = x.view(-1, 32*7*7)
		x = F.relu(self.fc1(x))
		x = self.fc2(x)
		return F.log_softmax(x)


class ModelCNN(lake.torch.network.Base):
	def __init__(self, opt):
		super(ModelCNN, self).__init__()
		self.opt = opt
		self.model = ModelCNNBase(opt)
		super(ModelCNN, self).init_weights()
		self.critera = F.nll_loss

	def run(self, data, is_train=True):
		x, y = data
		x = torch.FloatTensor(x.astype(np.float32) / 255.0 - 0.5)
		y = torch.from_numpy(y)
		if self.use_cuda:
			x, y = x.cuda(), y.cuda()
		x, y = Variable(x, volatile=not is_train), Variable(y)
		output = self.model(x)
		error = self.critera(output, y)

		pred = output.data.max(1)[1]
		correct = float(pred.eq(y.data).cpu().sum()) / y.data.size()[0]

		if is_train:
			return dict(loss=error, correct=correct)
		else:
			return dict(loss=float(error.data[0]), correct=correct)

	def step_train(self, data):
		return self.run(data)

	def step_test(self, data):
		return self.run(data, False)


# coding: utf-8
import sys
import lake


class Options(lake.option.NNOptions):
	def initialize(self):
		self.parser.add_argument('--model', type=str, default='cnn', help='model')
		self.parser.add_argument('--data', type=str, default='mnist', help='data')
		self.parser.add_argument('--batch_size', type=int, default=64, help='batch_size')
		self.parser.add_argument('--data_dir', type=str, default='datasets/mnist/', help='data')

if __name__ == '__main__':
	opt = Options()()
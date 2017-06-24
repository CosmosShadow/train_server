# coding: utf-8

def load(opt):
	if opt.data == 'mnist':
		from data_mnist import DataMnist
		return DataMnist(opt).load()
	else:
		raise ValueError('data not right')
# coding: utf-8

def load(opt):
	if opt.data == 'mnist':
		from .data_minst import DataMnist
		return DataMnist(opt).load()
	else:
		raise ValueError('data not right')
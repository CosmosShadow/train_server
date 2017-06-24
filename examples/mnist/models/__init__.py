# coding: utf-8

def load(opt):
	if opt.model == 'cnn':
		from model_cnn import ModelCNN
		return ModelCNN(opt)
	else:
		raise ValueError('model should be one of [cnn, ]')
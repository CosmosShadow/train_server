# coding: utf-8
import datas
import models
import lake.torch


trainer = lake.torch.Trainer()
opt = trainer.opt

data_train, data_test = datas.load(opt)
model = models.load(opt)

trainer.model = model
trainer.data_train = data_train
trainer.data_test = data_test

trainer.train()
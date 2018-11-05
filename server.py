# coding: utf-8
import os
import json
import lake.file
from flask import Flask, request
import collections
import numpy as np
import datetime


app = Flask(__name__)

def get_projects():
	projects = lake.file.read('data/projects.csv')
	names = projects[0]
	projects = projects[1:]
	projects = [dict(zip(names, project)) for project in projects]
	return projects


def get_project(project_id):
	for project in get_projects():
		if int(project['id']) == project_id:
			return project


@app.route('/', methods=['GET'])
def index():
	# return 'hello world'
	return app.send_static_file('index.html')


@app.route('/data/projects.json', methods=['GET'])
def projects_json():
	return json.dumps(get_projects())


@app.route('/data/project.json', methods=['GET'])
def project_json():
	project_id = request.values.get('project_id', 1)
	projects = get_projects()
	projects = [project for project in projects if project['id'] == project_id]
	if len(projects) > 0:
		project = projects[0]
		train_output_path = project['path']
		train_dirs = os.listdir(train_output_path)
		train_dirs = [item for item in train_dirs if not (item.startswith('.') or item.startswith('..'))]
		heads = ['option', '开始时间', '结束时间', '训练时长', 'eopchs', 'eopch', '进度', 'lr', 'current_lr', 'loss', '测试', 'model']
		bodys = []
		for start_time in reversed(train_dirs):
			detail = train_detail(train_output_path + start_time)
			option_name = detail[0]
			model_name = detail[1]
			bodys.append([option_name, start_time] + detail[2:] + [model_name])
		return json.dumps(dict(heads=heads, bodys=bodys))
	else:
		return json.dumps([])

def train_detail(train_path):
	option_name = ''
	end_time = ''
	train_time = ''
	epochs = 0
	epoch = 0
	lr = ''
	current_lr = ''
	loss = ''
	test = ''
	if os.path.exists(train_path + '/option.json'):
		options = json.loads(lake.file.read(train_path + '/option.json'))
		option_name = options.get('option_name', '')
		model_name = options.get('model_name', '')
		epochs = int(options.get('epochs', ''))
		lr = options.get('lr', '')
	if os.path.exists(train_path + '/record.txt'):
		records = lake.file.read(train_path + '/record.txt')
		last_record = json.loads(records[-1])
		epoch = int(last_record.get('epoch', ''))
		loss = last_record.get('loss', '')
		current_lr = last_record.get('lr', '')

		most_find = 1000
		for record in reversed(records[-most_find:]):
			record_obj = json.loads(record)
			has_test = False
			test_dict = {}
			for key in record_obj.keys():
				if key.startswith('test_'):
					has_test = True
					test_dict[key[5:]] = record_obj[key]
			if has_test:
				test = json.dumps(test_dict)
				break
	if os.path.exists(train_path + '/train.log'):
		train_log = lake.file.read(train_path + '/train.log')
		if len(train_log) > 0:
			begin_time = train_log[0][:len('2017-07-23 18:07:04')]
			end_time = train_log[-1][:len('2017-07-23 18:07:04')]
			begin = datetime.datetime.strptime(begin_time, '%Y-%m-%d %H:%M:%S')
			end = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
			train_time = str(end - begin)
	if epochs > 0:
		progress = str(int(epoch * 100.0 / epochs)) + '%'
	else:
		progress = '0%'
	return [option_name, model_name, end_time, train_time, epochs, epoch, progress, lr, current_lr, loss, test]


@app.route('/data/train.json', methods=['GET'])
def train_json():
	project_id = int(request.values.get('project', 1))
	train = str(request.values.get('train', 'tmp'))
	the_project = get_project(project_id)

	train_path = os.path.join(the_project['path'], train, 'record.txt')

	if not os.path.exists(train_path):
		return json.dumps({})

	records = lake.file.read(train_path)

	# 只显示最后训练的结果
	start_index = 0
	last_epoch = 0
	for i, record_json in enumerate(records):
		record = json.loads(record_json)
		epoch = record['epoch']
		if epoch < last_epoch:
			start_index = i
		last_epoch = epoch
	records = records[start_index:]

	shows = collections.defaultdict(dict)
	for record_json in records:
		record = json.loads(record_json)
		epoch = record['epoch']
		for key, value in record.items():
			if key not in ['save', 'epoch', 'time']:
				shows[key].setdefault('x', []).append(epoch)
				shows[key].setdefault('y', []).append(value)
	for key, show in shows.items():
		show['name'] = key
		show['type'] = 'scatter'
		if len(show['x']) > 500:
			avg_count = len(show['x']) / 500
			show['x'] = [show['x'][i] for i in range(0, len(show['x'])-avg_count+1, avg_count)]
			show['y'] = [np.mean(show['y'][i:i+avg_count]) for i in range(0, len(show['y'])-avg_count+1, avg_count)]

	print(shows.keys())
	return json.dumps({'show': list(shows.values())})

if __name__ == '__main__':
	# os.system('open -a /Applications/Safari.app http://0.0.0.0:8080')
	app.run(host='0.0.0.0', port=8080)

























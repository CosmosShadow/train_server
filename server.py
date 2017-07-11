# coding: utf-8
import os
import json
import lake
from flask import Flask, request
import collections


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
		train_dirs = os.listdir(project['path'] + '/outputs/')
		train_dirs = [item for item in train_dirs if not (item.startswith('.') or item.startswith('..'))]
		heads = ['项目']
		bodys = [[item] for item in train_dirs]
		return json.dumps(dict(heads=heads, bodys=bodys))
	else:
		return json.dumps([])


@app.route('/data/train.json', methods=['GET'])
def train_json():
	project_id = int(request.values.get('project', 1))
	train = str(request.values.get('trian', 'tmp'))
	the_project = get_project(project_id)

	train_path = the_project['path'] + '/outputs/' + train + '/record.txt'

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
		for key, value in record.iteritems():
			if key != 'epoch':
				shows[key].setdefault('x', []).append(epoch)
				shows[key].setdefault('y', []).append(value)
	for key, show in shows.iteritems():
		show['name'] = key
		show['type'] = 'scatter'

	return json.dumps({'show': shows.values()})

if __name__ == '__main__':
	# os.system('open -a /Applications/Safari.app http://0.0.0.0:8080')
	app.run(host='0.0.0.0', port=8080)

























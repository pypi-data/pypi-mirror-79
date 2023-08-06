
import flask
import json

from pipguitool.PIP import PIP

from flask import request, abort, render_template

import os
import argparse


# Args
# spark-submit arguments
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", help="Port (default: 4040)", type=int, default=4040)
parser.add_argument("-i", "--path", help="Target path for pip when installing a new package", default=None)
args = parser.parse_args()




p = PIP(install_path=args.path)
app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
# if upload folder does not exist then
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


@app.route('/list', methods=['GET'])
def list():
	
    return json.dumps(p.list())


@app.route('/install', methods=['POST'])
def install():

	if not request.json or not 'packages' in request.json or not hasattr(request.json['packages'], "append"):
		abort(400)
	
	return json.dumps(p.install(request.json['packages'])), 201


@app.route('/remove', methods=['POST'])
def remove():

	if not request.json or not 'packages' in request.json or not hasattr(request.json['packages'], "append"):
		abort(400)
	
	return json.dumps(p.remove(request.json['packages'])), 201


@app.route('/file', methods=['POST'])
def file():

	_file = request.files.get('file')
	
	# Save file to UPLOAD dir
	filePath = os.path.join(app.config['UPLOAD_FOLDER'], _file.filename)
	_file.save(filePath)

	# Install the whl file
	res = p.installWhl(filePath)

	# remove the uploaded file
	os.remove(filePath)

	return json.dumps(res), 201


@app.route('/', methods=['GET'])
def index():

	return render_template('index.html', packages=p.list())


def main():

	app.run(host="0.0.0.0", port=args.port, threaded=True)

if __name__ == '__main__':
    main()



from subprocess import Popen, PIPE
import json

from wheel_inspect import inspect_wheel

import re


# REGEX package name
_p_regex = re.compile('^[a-zA-Z0-9\-]+([=]{2}[0-9]+([\.][0-9]+([\.][0-9]+)?)?)?$')
_file_regex = re.compile('^[a-zA-Z0-9-\_\.]+$')


class PIP:

	def __init__(self, install_path=None):
		
		self.install_path = install_path

	def command(self, command):

		if self.install_path is None:
			return ["pip", command]
		else:
			return ["pip", command, "-t", self.install_path]


	def install(self, packages):

		pkgs = {}
		for pkg in packages:

			# validate package name
			if not self.validate(pkg):
				pkgs[pkg] = { 'name': pkg, 'installed': False, 'message': '\'{}\' is invalid'.format(pkg) }
				continue
			
			name = pkg.split("==")[0]
			p = Popen(self.command("install")+[pkg], stdin=PIPE, stdout=PIPE, stderr=PIPE)
			output, err = p.communicate(b"input data that is passed to subprocess' stdin")
			pkgs[name] = { 'name': name, 'installed': True if p.returncode == 0 else False, 'message': (output if p.returncode == 0 else err).decode("utf-8") }

		l = self.list()
		for pkg in l:
			if pkg['name'] in pkgs.keys():
				pkgs[pkg['name']]['version'] = pkg['version']


		return pkgs

	def installWhl(self, filePath):

		filename = filePath.split("/")[-1]

		try:

			# validate filename
			if not self.validate_filename(filename):
				raise Exception("Invalide filename")

			package_info = inspect_wheel(filePath)['dist_info']['metadata']

			p = Popen(self.command("install")+[filePath], stdin=PIPE, stdout=PIPE, stderr=PIPE)
			output, err = p.communicate(b"input data that is passed to subprocess' stdin")
			#(output if p.returncode == 0 else err).decode("utf-8")
			if p.returncode == 0:
				output = {**{"message": output.decode("utf-8")}, **{"name": package_info['name'], "version": package_info['version'], "author": package_info['author']}, **{"installed": True}}
			else:
				output = {**{"message": err.decode("utf-8")}, **{"filename": filename}, **{"installed": False}}

		except:
			output = {"filename": filename, "installed": False, "message": "Invalid File"}

		return [output]

	def remove(self, packages):

		pkgs = {}
		for pkg in packages:
			name = pkg.split("==")[0]
			p = Popen(["pip", "uninstall", "-y", pkg], stdin=PIPE, stdout=PIPE, stderr=PIPE)
			output, err = p.communicate(b"input data that is passed to subprocess' stdin")
			pkgs[name] = { 'name': name, 'removed': True if p.returncode == 0 else False, 'message': (output if p.returncode == 0 else err).decode("utf-8") }

		return pkgs

	def getPackagesInfo(self, packages):

		pkgs = {}
		p = Popen(["pip", "show"]+packages, stdin=PIPE, stdout=PIPE, stderr=PIPE)
		output, err = p.communicate(b"input data that is passed to subprocess' stdin")

		if p.returncode == 0:
			allpkgs = map(lambda x: x.strip(), output.decode("utf-8").split("---"))
			for pkg in allpkgs:
				properties = list(map(lambda line: list(map(lambda x: x.strip(), line.split(":", 1))), pkg.split("\n")))
				properties = { line[0].lower(): line[1] for line in properties}
				if len(properties) <= 0:
					continue
				pkgs[properties['name']] = properties

		return pkgs

	def list(self):

		p = Popen(["pip", "list", "--format", "json"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
		output, err = p.communicate(b"input data that is passed to subprocess' stdin")

		return [ {"name": e['name'], "version": e['version'], "message": "available"} for e in json.loads(output) ] if p.returncode == 0 else []

	def validate(self, package):

		return not _p_regex.match(package) is None

	def validate_filename(self, filename):

		return not _file_regex.match(filename) is None

	def has(self, package):

		return len(list(filter(lambda x: x['name'] == package, self.list()))) > 0


def main():
    #print(PIP().list())
    result = PIP().install(['scipy', 'numpy==1.18', 'asdasfafg3&_'])
    for i in result:
    	if not result[i]['installed']:
    		print(i, result[i]['message'])
    #print(PIP().installWhl("../dist/pip_gui_tools-0.0.8-py3-none-any.whl"))
    #print(PIP().installWhl("../dist/invalid_filename&.ad"))
    #print(PIP().remove(['scipy', 'numpy', 'asdqsd']))
    #print(PIP().getPackagesInfo(['scipy', 'numpy', 'asdqsd']))

if __name__ == '__main__':
    main()
	
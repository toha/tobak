from module import Module
import json, os, pwd
from subprocess import Popen, PIPE

DUPLICITY_BASE_COMMAND = "duplicity"
DUPLICITY_BASE_OPTS = " --asynchronous-upload --volsize 100 --num-retries 3 --verbosity 4 --exclude '**/*'"


def replaceModuleConfigVars(modulecfg, sched):
	return modulecfg.replace("$SCHEDNAME", sched["name"])


def createDuplicityCommand(modulecfg):
	if not modulecfg.has_key("include_files") or not modulecfg.has_key("destination"):
		raise Exception("TODO ERROR")


	base_cmd = DUPLICITY_BASE_COMMAND



	opts = ""
	if modulecfg.has_key("log_file"):
		opts += " --log-file %s" %(modulecfg["log_file"])
	if modulecfg.has_key("encrypt_key"):
		opts += " --hidden-encrypt-key %s" %(modulecfg["encrypt_key"])
	if modulecfg.has_key("signing_key"):
		opts += " --sign-key %s" %(modulecfg["signing_key"])
	if modulecfg.has_key("full_if_older_than"):
		opts += " --full-if-older-than %s" %(modulecfg["full_if_older_than"])

	for include_file in modulecfg["include_files"]:
		opts += " --include '%s'" %include_file

	full_command = "%s%s%s / %s" %(base_cmd, opts, DUPLICITY_BASE_OPTS, modulecfg["destination"])
	return full_command


class Duplicity( Module ):

	def run( self, sched ):
		module_cfg_copy = json.loads(replaceModuleConfigVars(json.dumps(self._module_cfg), sched))
		print "running duplicity profile: %s sched: %s" %(self.getName(), sched["name"])

		cmd = createDuplicityCommand(module_cfg_copy)
		p = Popen(cmd, shell=True, cwd="/tmp", env=os.environ.copy(), bufsize=4096, stdin=PIPE, stdout=PIPE, stderr=PIPE)
		output, err = p.communicate()
		rc = p.returncode
		return rc, output, err

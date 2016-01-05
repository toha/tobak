from module import Module
import json, os, pwd
from subprocess import Popen, PIPE

DUPLICITY_BASE_COMMAND = "duplicity"
DUPLICITY_BASE_OPTS = " --asynchronous-upload --volsize 100 --num-retries 3 --verbosity 4 --exclude '**/*'"


class Duplicity( Module ):

	def run( self, sched ):
		module_cfg_copy = json.loads(replaceModuleConfigVars(json.dumps(self._module_cfg), sched))
		print "running duplicity profile: %s sched: %s" %(self.getName(), sched["name"])

		cmd = createDuplicityCommand(module_cfg_copy)
		p = Popen(cmd, shell=True, cwd="/tmp", env=os.environ.copy(), bufsize=4096, stdin=PIPE, stdout=PIPE, stderr=PIPE)
		output, err = p.communicate()
		rc = p.returncode
		return rc, output, err

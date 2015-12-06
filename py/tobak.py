#!/usr/bin/python2
# -*- coding: utf-8 -*-

import sys, os, json, importlib, modules.module, inspect, time, shutil, traceback
from sched import createJobs
from email.mime.text import MIMEText
from subprocess import Popen, PIPE
from err import handleError
from cfg import *

run_dir = os.path.split(os.path.abspath(os.path.realpath(sys.argv[0])))[0]
# dynammicly import all modules
module_files = os.listdir(os.path.join(run_dir, "modules"))
module_files = filter(lambda x: x.endswith(".py") and "__init__" not in x and "module.py" not in x, module_files)
module_names = []
moduleImports = {}
for module_file in module_files:
	module_name = module_file.replace(".py", "")
	moduleImports[module_name] = importlib.import_module("modules.%s" %module_name)
	locals()[module_name] = moduleImports[module_name]

BACKUPSTARTTIME = int(time.time())

tobak_cfg = loadCfg()

runlogdir = os.path.join(tobak_cfg["tmp_log_dir"], "tobak_%d" %(BACKUPSTARTTIME))
if not os.path.isdir(runlogdir):
	os.mkdir(runlogdir)

class Tobak(object):
	def __init__(self, profiles):
		self.__result_nums = {"total": 0, "ok": 0, "nok": 0}
		self.__result_txt = []

		self.__profiles = []
		for module_cfg in profiles:
			self.__init_profile(module_cfg)

		# which profile has to run?
		alljobs = []
		for profile in self.__profiles:
			alljobs += createJobs(profile)

		print "%d jobs to run" %len(alljobs)

		# order jobs by priority
		alljobs = sorted(alljobs, key=lambda job: job.getProfile().getPriority())
		for job in alljobs:
			retCode, output, erroutput = job.getProfile().run(job.getSched())
			self.__processJobOutputs(job, retCode, output, erroutput)
			if retCode == 0:
				self.__updateLastRunFile(job.getProfile(), job.getSched())

		# send report if jobs had to run
		if len(alljobs) > 0:
			self.__sendResultMail()

		# remove tmpdir and everything in it
		shutil.rmtree(runlogdir)


if __name__ == "__main__":

	Tobak(tobak_profiles)

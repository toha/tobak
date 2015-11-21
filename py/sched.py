import os, sys, json, time, job
from err import handleError
from cfg import *
run_dir, run_file = os.path.split(os.path.abspath(__file__))

tobak_cfg = loadCfg()

lastrun_file = os.path.join(tobak_cfg["last_run_dir"], "lastrun.json")
try:
	filehandle = file(lastrun_file)
	lastrun = json.loads(filehandle.read())
	filehandle.close()
except Exception, e:
	lastrun = {}

def createJobs(profile):
	jobs = []
	for sched in profile.getSched():
		if hasToRun(profile, sched):
			jobs += [job.Job(profile, sched)]
	return jobs


def hasToRun(profile, sched):
	profile_key = "%s-%s" %(profile.getName(), sched["name"])
	
	if not lastrun.has_key(profile_key):
		return True

	last_run_time = lastrun[profile_key]

	sched_timer_secs = int(sched["value"])
	if sched["unit"] == "minutes":
		sched_timer_secs = sched_timer_secs * 60
	elif sched["unit"] == "hours":
		sched_timer_secs = sched_timer_secs * 60 * 60
	elif sched["unit"] == "days":
		sched_timer_secs = sched_timer_secs * 60 * 60	* 24
	elif sched["unit"] == "weeks":
		sched_timer_secs = sched_timer_secs * 60 * 60	* 24 * 7
	elif sched["unit"] == "weeks":
		sched_timer_secs = sched_timer_secs * 60 * 60	* 24 * 7
	elif sched["unit"] == "month":
		sched_timer_secs = sched_timer_secs * 60 * 60	* 24 * 30

	current_time = int(time.time())

	difftime = last_run_time - (current_time-sched_timer_secs)
	if difftime <= 0:
		return True

	return False
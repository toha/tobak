class Job(object):
	def __init__(self, profile, sched):
		self.__profile = profile
		self.__sched = sched

	def getProfile(self):
		return self.__profile
		
	def getSched(self):
		return self.__sched
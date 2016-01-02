class Module( object ):

    def run( self, sched ):
        raise NotImplementedError( "Should have implemented this" )

    def init_module_specific_cfg( self, module_cfg):
        self._module_cfg = module_cfg     

    def setName(self, name):
    	self._name = name

    def setPriority(self, prio):
    	self._priority =  prio

    def setSched(self, sched):
    	self._sched = sched

    def getName(self):
    	return self._name  	

    def getPriority(self):
    	return self._priority  	

    def getSched(self):
    	return self._sched  	
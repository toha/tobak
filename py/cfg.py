import sys, os, json
from err import handleError

def loadCfg():
	cfg_dir = getTobakCfgDir()
	tobak_cfg_file = os.path.join(cfg_dir, "tobak.json")
	try:
		filehandle = file(tobak_cfg_file)
		tobak_cfg_data = filehandle.read()
		filehandle.close()
		tobak_cfg = json.loads(tobak_cfg_data)
	except Exception, e:
		handleError("error on reading tobak cfg file", e)

	tobak_cfg_cache = tobak_cfg
	return tobak_cfg


def getTobakCfgDir():
	if (len(sys.argv) < 2):
		return "/etc/tobak"	
	else:
		return sys.argv[1]	

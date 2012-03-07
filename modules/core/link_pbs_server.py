import pbs

class link:
	URL_STRING = ''
	ID = 0

def connect(URL):
	id = pbs.pbs_connect(URL)
	ID = id
	return id

def getID(ID):
        return ID

def disconnect(ID):
	return pbs.pbs_disconnect(ID)
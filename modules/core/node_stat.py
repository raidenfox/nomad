import stat_job
import pbs
import string

class node_stat:
    val = ''
    
# ricerca dei nodi su cui e' attivo un processo
def node_list_by_job(ID,status,id_job):
    machines = []

    
    attribs = pbs.new_attropl(1)
    
    if id_job == "":
	attribs[0].name = pbs.ATTR_state
	attribs[0].value = status
	attribs[0].op =  pbs.EQ
    else:	
	attribs[0].name = pbs.ATTR_N
	attribs[0].value = job_id
	attribs[0].op =  pbs.EQ
        
    jobs = pbs.pbs_selectjob(ID, attribs, 'NULL')
    
    if status == "W":
	print "Numero Jobs Bloccati:",len(jobs), "\n"

    if status == "R":
	print "Numero Jobs Attivi sul sistema:",len(jobs), "\n"

    if status == "Q":
	print "Numero Jobs in coda:",len(jobs), "\n"

    
    print "Attendere prego ..."
    log = open("logs/result.txt","w")
    for i in jobs:
	py_mach = stat_job.statjob(ID,i)
	py_tot = i, "->" ,py_mach
	py_tot2 = i, "->" ,py_mach,"\r\n"	
	log.write(str(py_tot2))
	machines.append(py_tot)

    log.close()	
    return machines

def write_stat_nodes(ID,file_name):
    stat_file = open(file_name,"w")
    nodes = pbs.pbs_statnode(ID, "", "NULL", "NULL")
    for node in nodes:
	stat_file.write(node.name)
	for attrib in node.attribs:
	    stat_file.write(attrib.value)

    stat_file.close()
    return nodes

# effettua un alistta di tutti i nodi
def list_nodes(ID):
    nodename = []
    nodes = pbs.pbs_statnode(ID, "", "NULL", "NULL")
    for node in nodes:
	nodename.append(node.name)
    
    return nodename
	    
# configurazione d'uso di ogni nodo
def stat_nodeconf(ID):
    nodes = pbs.pbs_statnode(ID, "", "NULL", "NULL")
    for node in nodes:
	print node.name	
	for attrib in node.attribs:
	    print attrib.value
	    
def stat_node_by_name(ID,name_node):
    nodes = pbs.pbs_statnode(ID,name_node,"NULL","NULL")
    for node in nodes:
	print node.name
	for attrib in node.attribs:
	    if attrib.resource:
		print attrib.name, attrib.resource ,attrrib.value
	    else:
		print attrib.name, attrib.value
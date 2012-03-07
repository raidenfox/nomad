import string
import pbs

class stat_job:
    listjobs = ''    
    
    # Ottiene la lista di tutti i jobs attivi, in coda e bloccati, interattiva
def job_list(ID,status):
    # Select jobs on EQ ATTR_state condition
    attribs = pbs.new_attropl(1)
    attribs[0].name = pbs.ATTR_state
    attribs[0].value = status
    attribs[0].op =  pbs.EQ
    
    jobs = pbs.pbs_selectjob(ID, attribs, 'NULL')
    
    return jobs

def statjob(id_conn,id_job):
    result = []
    jobs = pbs.pbs_statjob(id_conn, id_job, "NULL", "NULL")
    nodes = pbs.pbs_statnode(id_conn, "", "NULL", "NULL")
    for job in jobs:
        for attrib in job.attribs:
            for node in nodes:
                if string.find(attrib.value,node.name) != -1:
                    result.append(node.name)

    return result

def statjob_detailed(id_conn,id_job):
    result = []
    jobs = pbs.pbs_statjob(id_conn, id_job, "NULL", "NULL")
    for job in jobs:
        print job.name,"\n"
        for attrib in job.attribs:
            print attrib.name,attrib.resource,attrib.value
            
    return result

# Ritorna il valore numerico della risorsa richiesta per un dato job
def resource_forjob(id_conn,id_job,id_resource):
    result = []
    jobs = pbs.pbs_statjob(id_conn, id_job, "NULL", "NULL")
    for job in jobs:
            attrib = job.attribs
            for i in id_resource:
                result = attrib[i].value
            
    return result

# Ritorna il nome della risorsa REALE richiesta per un dato job
def resource_name_forjob(id_conn,id_job,id_resource):
    result = ""
    jobs = pbs.pbs_statjob(id_conn, id_job, "NULL", "NULL")
    for job in jobs:
            attrib = job.attribs
            for i in id_resource:
                result = attrib[i].resource
            
    return result
    
# Ottieni il valore di una risorsa dall' ID del job e dal nome della risorsa
def getResourceValue(ID,jobid,res_name):
    lista = define_attribs(ID,jobid)
    id = getResourceID(lista,res_name)
    result = resource_forjob(ID,jobid,id)
    if res_name != "ctime" or res_name != "qtime" or res_name != "etime":
        return result
    else:
        time_conv = time.strftime("%a, %d %b %Y %H:%M:%S +0000",time.localtime(float(result)))
        return time_conv

# ID  RESOURCE
# 0   JOB NAME (NON IDENTIFICATORE MA IL NAME)
# 1   OWNER
# 2   CPU TIME
# 3   MEMORIA UTILIZZATA
# 4   MEMORIA VIRTUALE
# 5   WALLTIME
# 6   STATO
# 7   CODA
# 8   SERVER_MONITOR (TORQUE02)
#############################################
# potrebbe esserci anche account_name
# tutti gli indici fanno shift di 1
#############################################
# 9   CHECKPOINT
# 10  CTIME
# 11  PATH REPORT DELL' ERRORE
# 12  HOST SU CUI GIRA IL PROCESSO
# 13  HOLD_TYPES (DI TIPO YES 'Y' O  NO 'N')
# 14  JOIN_PATH (DI TIPO YES 'Y' O  NO 'N')
# 15  KEEP_FILES (DI TIPO YES 'Y' O  NO 'N')
# 16  


# Ritorna i nomi delle risorse i un processo, ma non i valori
def locate_attribs(id_conn, id_job):
    code = []
    attribs = []
    jobs = pbs.pbs_statjob(id_conn, id_job, "NULL", "NULL")
    i = 0
    index = len(jobs)
    for job in jobs:
        print job.name,"\n"
        attrib = job.attribs
        y = 0
        while i < index:
            lenght_a = len(attrib)
            while y < lenght_a:
                attribs.append(attrib[y].name)
                code.append(y)
                y = y + 1
            
            i = i+1
    
    
    #momentaneo - definire una ADT per memorizzare dianmicamente i codici degli attributi
    code_len = len(attribs)
    x = 0
    while x < code_len:
        print attribs[x], "->", code[x], "<-" ,jobs[0].attribs[x].value
        x = x + 1
    
    return attribs

# Ritorna i nomi delle risorse i un processo, ma non i valori
def define_attribs(id_conn, id_job):
    code = []
    attribs = []
    jobs = pbs.pbs_statjob(id_conn, id_job, "NULL", "NULL")
    i = 0
    index = len(jobs)
    for job in jobs:
        attrib = job.attribs
        y = 0
        while i < index:
            lenght_a = len(attrib)
            while y < lenght_a:
                attribs.append(attrib[y].name)
                code.append(y)
                y = y + 1
            
            i = i+1
    
    return attribs

def getResourceID(attribs,resource):
    index = len(attribs)
    i = 0
    indice = []
    while i < index:
        val = string.find(attribs[i],resource)
        if val != -1:
            indice.append(i)
        
        i = i+1
    
    return indice
    
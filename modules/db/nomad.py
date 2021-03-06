# Including system core path
import sys
import time
import os
import string
sys.path.append("core")
sys.path.append("db")

#including modules
import link_pbs_server # link a monitoring server
import stat_job # executes stats on jobs
import node_stat # executes stats on a node
import connect_db # manage connection to mysql db

class nomad:
    URL = ''    
        
def start_nomad(URL,T_SLEEP,STATE):
    os.system("clear")
    
    print "***************************************************************"
    print "*                        n.o.m.a.d.                           *" 
    print "*    DEMONE DI MONITORAGGIO AUTOMATICO NETWORK - ORIENTED     *"    
    print "***************************************************************"
    # Obtain an ID of opened connection with server
    ID = link_pbs_server.connect(URL)
    print "\nConnection with " + URL + " [OK]"
    print "Monitor started"
    print "---------------------------------------------------------------\n"
    
    idconn = connect_db.connect("localhost","root","eclipse88","nomad")
    # explore_cluster(ID,idconn)
    if ID != 0:
        while 1:
            jobs = stat_job.job_list(ID,STATE)
            date_time = time.asctime()
            n_jobs = len(jobs)
            if n_jobs != 0:
                print "[" + str(date_time) + "] Job in Wait state: [" + str(n_jobs) +"]"
                for job in jobs:
                    report_job_problem(idconn,ID,job,STATE)
                #TODO
                # Inizializza la connessione al database
                # Aggiorna database
            else:
                print "[" + str(date_time) + "] Job in Wait state: [" + str(n_jobs) +"]"
            time.sleep(T_SLEEP)    
    else:
        print "Connection with " + URL + " [FAILED]"
        print "------------------------------------------------------------"
    connect_db.close(idconn)   
# Report the details of Wait-Job Selected
def report_job_problem(idconn,ID,job_reported,STATE):
    # Obtain WN where the Wait Job was assigned
    worknodes = stat_job.statjob(ID,job_reported)
    attribs = stat_job.define_attribs(ID,job_reported)
    attribs_resources = []    
    attribs_values = []    
    
    index = len(attribs)    
        
    for attr in attribs:
        id_resource = stat_job.getResourceID(attribs,attr)
        attribs_resources.append(stat_job.resource_name_forjob(ID,job_reported,id_resource))
        attribs_values.append(stat_job.resource_forjob(ID,job_reported,id_resource))
    
    # Controlla se il job e' ancora wait prima di inserire le informazioni
    if (stat_job.getResourceValue(ID,job_reported,"job_state") == STATE):
        store_report(idconn,job_reported,attribs,attribs_values)        
#    
#    sys.stdout.write("Resources assigned to " + job_reported)
#    i = 0
#    j = 0
    
      
        
#    while i < index:
#        if str(attribs_resources[i]) != "None": 
#            sys.stdout.write("\n")    
#            sys.stdout.write(str(i) + " - "+ "\x1b[01;34m" + attribs[i]+ "\x1b[00m" + " - " + attribs_resources[i] + " - " + attribs_values[i])
#            sys.stdout.write("\n")
#        else:
#            sys.stdout.write("\n")    
#            sys.stdout.write(str(i) + " - "+ "\x1b[01;34m" + attribs[i]+ "\x1b[00m" + " - "  + attribs_values[i])
#            sys.stdout.write("\n")
#        
#        i = i+1

def store_report(idconn,job_name,attribs,stack_resource):
    analyzed_stack = []
    processed_resources = []
    processed_info = []
    
    index_time = []
    index_add = []
    
    main_information = ["Job_Name", #0
                        "Job_Owner", #1
                        "job_state", #2
                        "queue", #3
                        "ctime", #4
                        "Error_Path", #5
                        "mtime", #6
                        "Output_Path", #7
                        "Priority", #8
                        "qtime", #9
                        "session_id", #10
                        "stagein", #11
                        "stageout", #12
                        "etime", #13
                        "start_time"] #14


#check on temporal resources (ctime,qtime,etime)

    index = len(attribs)
    
    i = 0
    k = 0
    # analyze the array and substitute temporal values
    while i < index:
        if (attribs[i] == "ctime") or (attribs[i] == "mtime") or (attribs[i] == "qtime") or (attribs[i] == "etime") or (attribs[i] == "start_time"):
            analyzed_stack.append(str(time.strftime("%d %b %Y - %H:%M:%S",time.localtime(float(stack_resource[i])))))
            index_time.append(i)
        else:
            analyzed_stack.append(stack_resource[i])
        
        i = i+1
        
    
    while k < index:
        for key in main_information:
            if attribs[k] == key:
                index_add.append(k)
        
        k = k+1
    
    sys.stdout.write("\n")
    
    # Temporaneo - da modificare (rimozione dei print)
    
    for indici in index_add:
        processed_resources.append(attribs[indici])
        processed_info.append(analyzed_stack[indici])
        sys.stdout.write("\x1b[01;34m" + attribs[indici]+ "\x1b[00m" + " - " + analyzed_stack[indici])
        sys.stdout.write("\n")
    
    # submit_info(idconn,job_name,processed_resources,processed_info)    
   
    
def submit_info(idconn,job_id,table_int,values):    
    
    sql_check = "SELECT * FROM nomad.job WHERE job_id ='" + job_id + "'"
    
    if connect_db.num_rows(idconn,sql_check) == 0:
        #fai un INSERT
        sql_insert = "INSERT INTO job VALUES('"+ job_id +"','"+ values[0] +"','"+ values[2] +"',"+ values[10] +","+ values[8] +",0)"
        sql_insert2 = "INSERT INTO user (job_owner) VALUES('"+ values[1] +"')"
        connect_db.executeSQL(idconn,sql_insert)
        connect_db.executeSQL(idconn,sql_insert2)
        
        sql_id = "SELECT id FROM user WHERE job_owner = '" + str(values[1]) + "'"
        idval = connect_db.executeSQL(idconn,sql_id) 
        
        sql_insert3 = "INSERT INTO sottomissione (job_id,id) VALUES('"+ job_id +"',"+ str(idval[0]) +")"
        connect_db.executeSQL(idconn,sql_insert3)
    else:
        sql_update = ""
        #fai un update
    
def explore_cluster(ID,idconn):
    sql_cluster = "SELECT * FROM worker_node"
    if connect_db.num_rows(idconn,sql_cluster) == 0:
        lista = node_stat.list_nodes(ID)
        for i in lista:
            sql_insert = "INSERT INTO worker_node (node_name) VALUES('"+ i +"')"
            connect_db.executeSQL(idconn,sql_insert)
       
            
    

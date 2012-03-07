# Viene inclusa la libreria per la connessione mysql
import _mysql
import string

class connect_db:
    URL = ""
    user = ""
    passw = ""
    db = ""
    
def connect(URL,user,passw,db):
    id_conn = _mysql.connect(URL,user,passw,db)
    return id_conn

# FIX: implementare il controllo sulla lunghezza del risultato
# Tuple restituite come ((risultato),)
def executeSQL(id, sql):
    print sql
    id.query(sql)
    res = id.store_result()
    if string.find(sql,"SELECT") != -1:
        risultato = res.fetch_row(0)
        return risultato[0]
    else:
        return 0

def num_rows(id, sql):
    id.query(sql)
    res = id.store_result()
    return int(res.num_rows())

def close(id):
    return id.close()
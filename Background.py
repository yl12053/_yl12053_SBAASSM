import sqlite3, queue, threading
from Modules import ModuleBase

que = queue.Queue()

class Query:
    def __init__(self, proc):
        self.proc = proc
        self.ret = None
        self.error = None
    def waitForAnswer(self):
        while self.ret is None:
            pass
        return (self.ret, self.error)

def createQuery(sql):
    def process(cursor):
        cursor.execute(sql)
        ret = cursor.fetchall()
        return ret
    queryobj = Query(process)
    que.put(queryobj)
    ret, err = queryobj.waitForAnswer()
    if err:
        raise ret
    else:
        return ret

def Thread():
    database = sqlite3.connect("Data.db")
    while True:
        f = que.get()
        cursor = database.cursor()
        try:
            ret = f.proc(cursor)
            database.commit()
            f.ret = ret
            f.error = False
        except Exception as e:
            f.ret = e
            f.error = True
        
threading.Thread(target=Thread).start()
ModuleBase.createQuery = createQuery

import sqlite3, queue, threading, sys
from Modules import ModuleBase

que = queue.Queue()
running = False
runProc = 0
procStartList = []
procEndList = []

class Query:
    def __init__(self, proc):
        self.proc = proc
        self.ret = None
        self.error = None
    def waitForAnswer(self):
        while self.ret is None:
            pass
        return (self.ret, self.error)

def createQuery(sql, para = ()):
    def process(cursor):
        cursor.execute(sql, para)
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
    global runProc
    runProc += 1
    database = sqlite3.connect("Data.db")
    while running:
        f = que.get()
        if f is None:
            continue
        cursor = database.cursor()
        try:
            ret = f.proc(cursor)
            database.commit()
            f.ret = ret
            f.error = False
        except Exception as e:
            f.ret = e
            f.error = True
    database.close()
    runProc -= 1


procStartList.append(threading.Thread(target=Thread).start)
procEndList.append(lambda: que.put(None))


def Start():
    global running
    running = True
    for func in procStartList:
        func()

def Shutdown(hook = lambda: 0, blocking = False):
    global running
    running = False
    for func in procEndList:
        func()
    if blocking:
        WaitToDie()
    sys.exit(hook())

def WaitToDie():
    global runProc
    while runProc:
        pass

exceptHook = sys.excepthook
def newExceptHook(*args, **kwargs):
    exceptHook(*args, **kwargs)
    print("Shutdowning...")
    Shutdown(blocking = True, hook = lambda: -1)
    print("Shutdown gracefully")

sys.excepthook = newExceptHook

def run(func, rethook=lambda: 0):
    global running
    Start()
    func()
    if running:
        Shutdown(hook = rethook)
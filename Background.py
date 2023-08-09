import sqlite3, queue, threading, sys

from PyQt5.QtCore import pyqtSignal, QCoreApplication
from PyQt5.QtWidgets import QWidget

from Modules import ModuleBase

que = queue.Queue()
running = False
runProc = 0
procStartList = []
procEndList = []

exitFunc = sys.exit

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
    print("Shutdown start")
    running = False
    for func in procEndList:
        func()
    if blocking:
        WaitToDie()
    print("Done")
    exitFunc(hook())

def WaitToDie():
    global runProc
    while runProc:
        pass

def threadWrapper(func):
    global runProc
    def wrap(*args, **kwargs):
        global runProc
        b = None
        runProc += 1
        try:
            func(*args, **kwargs)
        except Exception as e:
            print("Wrapper have caught an exception: %s"%str(e))
            b = e
        finally:
            runProc -= 1
        if isinstance(b, Exception):
            raise b

    return wrap

def genericEHook(func):
    def newExceptHook(*args, **kwargs):
        func(*args, **kwargs)
        print("Unhandled error caught, Shutting down...")
        Shutdown(blocking = True, hook = lambda: 1)
        print("Shutdown gracefully")
    return newExceptHook


sys.excepthook = genericEHook(sys.excepthook)
threading.excepthook = genericEHook(threading.excepthook)

def run(func, rethook=lambda: 0):
    global running
    Start()
    func()
    if running:
        Shutdown(hook = rethook)

def mround(n, digits):
    p = round(n, digits)
    if p == int(p):
        return int(p)
    return p
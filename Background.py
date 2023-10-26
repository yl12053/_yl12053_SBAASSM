import sqlite3, queue, threading, sys

from PyQt5.QtCore import pyqtSignal, QCoreApplication
from PyQt5.QtWidgets import QWidget

from Modules import ModuleBase

#Defining Global Variable for Cross-threading access of SQLite Database
#Query queue
que = queue.Queue()

#Flag, to control the overall shutdown procedure
running = False

#Thread counting
runProc = 0

#Pre-defined list to store procedure to be run at start and end of program
#Procedures will be appended(registered) during module registering
procStartList = []
procEndList = []

exitFunc = sys.exit

#Defining class Query.
#Used for a single SQL Query
class Query:
    def __init__(self, proc):
        self.proc = proc
        self.ret = None
        self.error = None
    def waitForAnswer(self):
        while self.ret is None:
            pass
        return (self.ret, self.error)

#Procedure to create a single query, which will put its' request into the queue and blocking for result
#Thread-safe
#Parameter injection method, safe from injection.
def createQuery(sql, para = ()):
    #Inner-procedure, to be passede into Query.proc
    def process(cursor):
        cursor.execute(sql, para)
        ret = cursor.fetchall()
        return ret
    
    #Create query object
    queryobj = Query(process)
    #Put into queue
    que.put(queryobj)
    ret, err = queryobj.waitForAnswer()
    #Return result
    if err:
        raise ret
    else:
        return ret

#Thread for SQL
def Thread():
    global runProc
    #increase thread count
    runProc += 1
    database = sqlite3.connect("Data.db")
    #While the program is not stopped yet
    while running:
        #Get a single query from queue
        f = que.get()

        #f will be None if and only if the program is stopped (or during stopping procedure)
        if f is None:
            continue

        #create database cursor
        cursor = database.cursor()
        
        try:
            #pass the cursor into inter-procedure submitted from createQuery
            ret = f.proc(cursor)
            #commit all possible update
            database.commit()
            f.ret = ret
            f.error = False
        except Exception as e:
            f.ret = e
            f.error = True
    #Close the database once the program is stopped
    database.close()
    #unregister the thread
    runProc -= 1

#Register the thread
procStartList.append(threading.Thread(target=Thread).start)
procEndList.append(lambda: que.put(None))

#Program init procedure
def Start():
    global running
    running = True
    for func in procStartList:
        func()

#Program shutdown procedure
def Shutdown(hook = lambda: 0, blocking = False):
    global running
    print("Shutdown start")
    running = False
    for func in procEndList:
        func()
    if blocking:
        #block til all thread have peacefully shutdown
        WaitToDie()
    print("Done")
    exitFunc(hook())

def WaitToDie():
    global runProc
    while runProc:
        pass

#decorator for func --> thread
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

#Unhandled-exception handler hijack
#To shutdown the program peacefully before raise
def genericEHook(func):
    def newExceptHook(*args, **kwargs):
        func(*args, **kwargs)
        print("Unhandled error caught, Shutting down...")
        Shutdown(blocking = True, hook = lambda: 1)
        print("Shutdown gracefully")
    return newExceptHook


sys.excepthook = genericEHook(sys.excepthook)
threading.excepthook = genericEHook(threading.excepthook)

#Program start procedure
def run(func, rethook=lambda: 0):
    global running
    Start()
    func()
    if running:
        Shutdown(hook = rethook)

#Custom round function
def mround(n, digits):
    p = round(n, digits)
    if p == int(p):
        return int(p)
    return p

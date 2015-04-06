import threading
import os
import pexpect

from mainbot.commands import Command


class cca(Command):
    arguments = ["str"]
    permissionLevel = 0
    permitExtraArgs = True
    manArgCheck = False
    defaultArgs = []
    callName = "cca"

    def __init__(self,bot):
        #requirement check
        for directory in os.environ["PATH"].split(":"):
            if os.path.exists(os.path.join(directory,"adventure")):
                Command.__init__(self,bot)
                break
        else:
            raise FileNotFoundError("Executable 'adventure' was not found. \n\
            Try installing 'bsdgames' or disable the 'cca' command.")

    def on_call(self,event,*args):
        base = args[0].lower()
        if base == "start":
            self.sub = pexpect.spawn("adventure",args[1:] if len(args) > 1 else [],timeout=None)
            
            self.printThread = threading.Thread(target = self.outputLoop, name = "output", args = (event,self.sub))
            self.printThread.start()
        elif base == "run":
            self.sub.sendline(" ".join(args[1:]))
            
    def on_die(self,event):
        self.sub.kill()
    
    def outputLoop(self,event,sub):
        try:
            while 1:
                self.pubMsg(event,str(sub.readline(),"utf8").strip("\r\n"))
        
        except KeyboardInterrupt:
            pass
        
        
        

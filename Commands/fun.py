import time
import os
import shlex

from mainbot.commands import Command
import pyfiglet

class slap(Command):
    arguments = ["str"]
    permissionLevel = 3
    permitExtraArgs = False
    manArgCheck = False
    defaultArgs = []
    callName = "slap"
    
    def on_call(self, event, *args):
        print(args[0])
        self.bot.connection.privmsg(self.bot.channelName,"\001ACTION slapped %s.\001" % args[0])

class asciiClock(Command):
    arguments = []
    permissionLevel = 0
    permitExtraArgs = False
    manArgCheck = False
    defaultArgs = []
    callName = "time"
    
    def on_call(self,event,*args):
        font = pyfiglet.Figlet()
        
        x = font.renderText(str(time.ctime()).split(" ")[4])
        for line in x.split("\n"):
            if line != "":
                self.pubMsg(event,line)
        
class cowsay(Command):
    arguments = ["str"]
    permissionLevel = 0
    permitExtraArgs = True
    manArgCheck = False
    defaultArgs = []
    callName = "cowsay"

    withArguments = ["-e","-f","-T","-W"]
    withoutArguments = ["-b", "-d", "-g", "-h", "-l", "-L", "-n", "-N", "-p", "-s", "-t", "-w", "-y"]

    def on_call(self,event,*args):
        args = list(args)
        newArgs = []
        text = []
        while len(args) != 0:
            arg = args.pop(0)
            if arg[0:2] in self.withArguments:
                newArgs.append(arg[0:2])
                if arg not in self.withArguments: #check for arguments without space
                    newArgs.append(arg[2:])
                else:
                    newArgs.append(args.pop(0))
            elif arg in self.withoutArguments:
                newArgs.append(arg)
            elif arg[0] == "-":
                self.privMsg(event,"Invalid argument '%s'." % arg)
            else:
                text.append(arg)
        print("Executing %s." % ("cowsay " + " ".join(newArgs) + " " +shlex.quote(" ".join(text))))
        y = os.popen("cowsay " + " ".join(newArgs) + " " +shlex.quote(" ".join(text)))
        for line in y.read().split("\n"):
            self.pubMsg(event,line)


    
                                   
        
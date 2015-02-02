#!/usr/bin/env python3
import HotFuzz.main as main
import threading
import irc.bot
import subprocess
import time
names = open("./HotFuzz/names").read().split("\n")

class settings():
    channel = "#BANANARAMA"
    callsign = "pollbot"
    name = "PollBot"
    manOplist = ["AlexCarolan","MrMindImplosion","Humanhum"]
    chatlog = open("./irclogs/chat.log","a")
    allowExclaimCommand = True
    textPrefix = "\x0306,99"
    textPostfix = "\x03\z02"
    
def makeBot(name):
    print(name)
    y = main.BaseBot(irc.bot.ServerSpec("home.mrmindimplosion.co.uk",6667),
                    settings.channel,name.replace(" ","").replace(".","").replace('"',""),settings.callsign,
                    settings.manOplist,settings.chatlog,
                    settings.allowExclaimCommand,settings.textPrefix,
                    settings.textPostfix)
    x = threading.Thread(target = y.start)
    threads.append(x)
    x.start()
 
 
threads = []
for name in names:
    if name != "" and name[0] != "#":
        makeBot(name)
        time.sleep(5)

# for name in names:
#     subprocess.Popen(["python3","./main.py",name,channel])

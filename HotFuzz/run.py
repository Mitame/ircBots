import main
import threading
import irc.bot
import subprocess
names = open("names").read().split("\n")

channel = "#BrokenBots"
# def makeBot(name):
#     print(name)
#     y = main.BaseBot(irc.bot.ServerSpec("home.mrmindimplosion.co.uk",6667),channel,name.replace(" ",""))
#     x = threading.Thread(target = y.start)
#     threads.append(x)
#     x.start()
# 
# 
# threads = []
# for name in names:
#     makeBot(name)

for name in names:
    subprocess.Popen(["python3","./main.py",name,channel])
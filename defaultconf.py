import defaultconf

class settings():
    host = "irc.freenode.net"
    port = 6667
    channel = "#BrokenBots"
    callSign = "unbot"
    name = "UnNamedBot"
    manOpList = ["Oper1","Oper2","Oper3"]
    chatLog = open("./irclogs/chat.log","a")
    commandPrefix = "!"
    textPrefix = "\x0306,99"
    textPostfix = "\x03\z02"
    nickPass = "password"
    servPass = ""
    version = 3

if defaultconf.settings.version > settings.version:
    raise ImportWarning("More settings have been added, please update your conf.py.")
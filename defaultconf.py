import defaultconf

class settings():
    host = "irc.rizon.net"
    port = 6667
    channel = "#BrokenBots"
    callsign = "unbot"
    name = "UnNamedBot"
    manOplist = ["Oper1","Oper2","Oper3"]
    chatlog = open("./irclogs/chat.log","a")
    allowExclaimCommand = True
    textPrefix = "\x0306,99"
    textPostfix = "\x03\z02"
    nickPass = "password"
    version = 1

if defaultconf.settings.version > settings.version:
    raise ImportWarning("More settings have been added, please update your conf.py.")
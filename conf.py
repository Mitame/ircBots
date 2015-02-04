import defaultconf

class settings():
    host = "home.mrmindimplosion.co.uk"
    port = 6667
    channel = "#BANANARAMA"
    callsign = "pollbot"
    name = "PollBot"
    manOplist = ["MrMindImplosion"]
    chatlog = open("./irclogs/chat.log","a")
    allowExclaimCommand = True
    textPrefix = "\x0306,99"
    textPostfix = "\x03\z02"
    nickPass = "password"
    version = 1



if defaultconf.settings.version > settings.version:
    raise ImportWarning("More settings have been added, please update your conf.py.")

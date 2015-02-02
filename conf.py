class settings():
	host = "irc.rizon.net"
	port = 6667
    channel = "#BrokenBots"
    callsign = "pollbot"
    name = "PollBot"
    manOplist = ["YourNickHere"]
    chatlog = open("./irclogs/chat.log","a")
    allowExclaimCommand = True
    textPrefix = "\x0306,99"
    textPostfix = "\x03\z02"
#!/usr/bin/env python3
class settings():
    channel = "#BANANARAMA"
    callsign = "gambot"
    name = "GambleBot"
    manOplist = ["AlexCarolan","MrMindImplosion","Humanhum"]
    chatlog = open("./irclogs/chat.log","a")
    allowExclaimCommand = True
    textPrefix = "\x0306,99"
    textPostfix = "\x03\z02"

def main():
    import irc.bot
    from mainbot.main import BaseBot
    bot = BaseBot(irc.bot.ServerSpec("home.mrmindimplosion.co.uk",6667),
                    settings.channel,settings.name,settings.callsign,
                    settings.manOplist,settings.chatlog,
                    settings.allowExclaimCommand,settings.textPrefix,
                    settings.textPostfix)
    
    import mainbot.commands as commands
    commands.ping(bot)
    commands.die(bot)
    commands.help(bot)

    import games.card
    games.card.blackjack(bot)
    games.card.ison(bot)
    
    bot.start()

if __name__ == "__main__":
    main()

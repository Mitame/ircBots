#!/usr/bin/env python3
import irc.bot

import conf

class settings(conf.settings):
    name = "MMI-GambleBot"
    callSign = "gambot"


def main():
    from mainbot.main import BaseBot
    bot = BaseBot(irc.bot.ServerSpec(settings.host,settings.port,settings.servPass),
                    settings.channel,settings.name,settings.callSign,
                    settings.manOpList,settings.chatLog,
                    settings.allowExclaimCommand,settings.textPrefix,
                    settings.textPostfix)
    
    import mainbot.commands as commands
    commands.ping(bot)
    commands.die(bot)
    commands.help(bot)

    import games.card
    games.card.blackjack(bot)
    games.card.gofish(bot)
        
    bot.start()

if __name__ == "__main__":
    main()

import random
import copy

from mainbot.commands import Command


class cardClasses():
    
    class Card():
        suits = ["H","D","C","S"]
        ranks = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
        def __init__(self,suit,rank):
            self.suit = suit
            self.rank = rank
        
        def __str__(self):
            return self.suit+self.rank
        
        def __int__(self):
            return self.ranks.index(self.rank)
        
        def __repr__(self):
            return str(self)
        
        def index(self,order="SR"):
            if order == "SR":
                return self.suits.index(self.suit)+self.ranks.index(self.rank)*4
            elif order == "RS":
                return self.suits.index(self.suit)*13+self.ranks.index(self.rank)
            else:
                raise ValueError
        
    class Stack():
        
        def __init__(self):
            self.reset()
        
        def deal(self,count):
            rtr = []
            for x in range(count):
                rtr.append(self.cards.pop(random.randint(0,len(self.cards)-1)))
            return rtr
        
        def reset(self):
            self.cards = []
            for suit in cardClasses.Card.suits:
                for rank in cardClasses.Card.ranks:
                    self.cards.append(cardClasses.Card(suit,rank))
        
    class Hand():
        def __init__(self,name):
            self.cards = []
            self.name = name
            self.points = 0
        
        def addCard(self,*cards):
            self.cards.extend(cards)
        
        def sort(self,order="SR"):
            self.cards.sort(cardClasses.Card.index)
            

class blackjack(Command):
    class Card(cardClasses.Card):
        bjValue = [0,2,3,4,5,6,7,8,9,10,10,10,10]
    
    class Stack(cardClasses.Stack):
        pass
    
    class Hand(cardClasses.Hand):
        def __int__(self):
            acount = 0
            result = 0
            for card in self.cards:
                i = blackjack.Card.ranks.index(card.rank)
                if i == 0:
                    acount += 1
                else:
                    result += blackjack.Card.bjValue[i]
            
            for x in range(acount):
                if result + 11 > 21:
                    result += 1
                else:
                    result += 11
            
            return result
        
        def getScore(self,cardCount=True):
            x = self.__int__()
            
            if x > 21:
                return 0
            else:
                return x + ((len(self.cards)/11) if cardCount else 0)
        
    arguments = []
    permissionLevel = -1
    permitExtraArgs = True
    manArgCheck = False
    defaultArgs = []
    callName = "bj"
    
    messages = {"newturn":"%s, it's your turn!",
                "cards":"You currently have [%s], giving you a total score of %s.",
                "playInstructions":"Say `%s:bj hit` to get another card or `%s:bj stick` to keep the ones you have and pass the turn to the next player.",
                "endgame":"The game has ended and %s won. Say `%s:bj join` to join or `%s:bj leave` to leave.",
                "bust":"%s has gone bust and is out of the game.",
                "newPlayer":"%s has joined BlackJack and will be playing in the next game.",
                "newgame":"BlackJack has started. The current players are: ",
                "newcard":"You got %s.",
                "lostPlayer":"%s has left BlackJack.",
                "noPlayers":"The game must have atleast one participant in order to start.",
                "youbust":"You have gone bust",
                "playerleft": "%s has left the ghannel. Continuing game without them.",
                "hit":"%s hit.",
                "stick":"%s stuck.",
                "gameScore":"The scores for this round were:",
                "totalScore":"The total scores are",
                
    }
    
                 
    def __init__(self,bot):
        Command.__init__(self,bot)
        self.players = []
        self.gameInProgress = False
        self.totalScores = {}
        
    def on_call(self,event,*args):
        args = " ".join(args).lower().split(" ")
        base = args[0]
        print(base)
        
        if base == "join":
            if event.source.nick not in self.players:
                self.players.append(event.source.nick)
            self.pubMsg(event,self.messages["newPlayer"] % event.source.nick)
            self.totalScores[event.source.nick] = 0
            
        elif base in ("quit","leave"):
            if event.source.nick in self.players:
                self.players.remove(event.source.nick)
            self.pubMsg(event,self.messages["lostPlayer"] % event.source.nick)
        
        elif base == "start":
            if self.gameInProgress:
                self.privMsg(event,)
            self.start(event)
        
        elif base == "hit":
            if self.gameInProgress:
                self.hit(event)
        
        elif base == "stick":
            if self.gameInProgress:
                self.stick(event)      
        
        elif base == "scores":
            self.getTotalScores(event)  
            
        
    def getCurrentHand(self):
        return self.curPlayers[self.playerOrder[self.curplayer]]        
    
    def start(self,event):
        if len(self.players) == 0:
            self.pubMsg(event,self.messages["noPlayers"])
            return
        
        self.gameInProgress = True
        self.curStack = blackjack.Stack()
        self.curPlayers = {}
        self.playerOrder = []
        self.curplayer = 0
        PlayerOrder = copy.deepcopy(self.players)
        for x in range(len(PlayerOrder)):
            self.playerOrder.append(PlayerOrder.pop(random.randint(0,len(PlayerOrder)-1)))
        
        for player in self.playerOrder:
            self.curPlayers[player] = blackjack.Hand(player)
            self.curPlayers[player].addCard(*self.curStack.deal(2))
        
        self.pubMsg(event, self.messages["newgame"]+", ".join(self.playerOrder))
        self.passTurn(event, 0)
        
        
    def showHand(self,event):
        self.curPlayers(event.source.nick).sort()
        self.privMsg(event,self.messages["cards"] % ( ", ".join(self.getCurrentHand().cards),int(self.getCurrentHand())))
            
    def passTurn(self,event,curplayer=False):
        print(len(self.playerOrder))
        print(self.curplayer)
        if curplayer is False:
            self.curplayer += 1
            while self.curplayer != len(self.playerOrder) and not self.bot.channels[self.bot.channelName].has_user(self.playerOrder[self.curplayer]):
                self.pubMsg(event,self.messages["playerleft"] % self.playerOrder[self.curplayer])
                self.curplayer += 1
                
                
            if self.curplayer % len(self.playerOrder) == 0:
                self.endGame(event)
                return
        else:
            self.curplayer = curplayer
        self.pubMsg(event,self.messages["newturn"] % self.playerOrder[self.curplayer])
        self.privMsg(self.playerOrder[self.curplayer], self.messages["playInstructions"] % (self.bot.callsign,self.bot.callsign))
        self.privMsg(self.playerOrder[self.curplayer], self.messages["cards"] % ( ", ".join(str(card) for card in self.getCurrentHand().cards),int(self.getCurrentHand())))
        
    def hit(self,event):
        self.pubMsg(event,self.messages["hit"] % event.source.nick)
        x = self.curStack.deal(1)
        self.getCurrentHand().addCard(*x)
        self.privMsg(event,self.messages["newcard"] % x[0])
        if int(self.getCurrentHand()) > 21:
            self.privMsg(event, self.messages["youbust"])
            self.pubMsg(event, self.messages["bust"] % event.source.nick)
            self.passTurn(event)
        else:
            self.privMsg(event,self.messages["cards"] % ( ", ".join(str(card) for card in self.getCurrentHand().cards),int(self.getCurrentHand())))
            
    def stick(self,event):
        self.pubMsg(event,self.messages["stick"] % event.source.nick)
        self.passTurn(event)
    
    def endGame(self,event):
        self.gameInProgress = False
        self.playersort = list(self.curPlayers.values())
        self.playersort.sort(key=self.Hand.getScore)
        for x in self.playersort:
            print(x.name,x.getScore())
        
        self.playersort.reverse()
        self.totalScores[x.name] += 1
        self.pubMsg(event,self.messages["endgame"] % (self.playersort[0].name,self.bot.callsign,self.bot.callsign))
        self.printScores(event)
        
    def printScores(self,event):
        self.pubMsg(event,self.messages["gameScore"])
        for x in self.playersort:
            self.pubMsg(event,(x.name+" | "+str(x.getScore(False))+" + "+str(len(x.cards))))
        
    
    def getTotalScores(self,event):
        self.pubMsg(event,self.messages["totalScore"])
        for x in self.totalScores.keys():
            self.pubMsg(event,(x+" | "+str(self.totalScores[x])))
            
    
    def checkPermissions(self,event,*args):
        if len(args) == 0:
            return False
        base = args[0].lower()
        if base in ["hit","stick"]:
            if event.source.nick != self.playerOrder[self.curplayer]:
                self.privMsg(event,"Only the current player can use this command.")
                return False
            else:
                return True
        
        elif base in ["join","leave","quit","scores"]:
            return True
        
        elif base in ["start"]:
            if self.bot.getPermLevel(event) >= 3:
                return True
            else:
                return False
                
    
    def checkArgs(self,event,*args):
        return True
        

class gofish(Command):
    arguments = []
    permissionLevel = -1
    permitExtraArgs = True
    manArgCheck = True
    defaultArgs = []
    callName = "gf"
    
    messages = {"newturn":"%s, it's your turn!",
                "cards":"You currently have [%s]",
                "playInstructions":"Say `%s:gf help` if you need help with commands. Say `%s:gf rules` or look on wikipedia for the rules.",
                "endgame":"The game has ended and %s won. Say `%s:gf join` to join or `%s:gf leave` to leave.",
                "newPlayer":"%s has joined GoFish and will be playing in the next game.",
                "newgame":"GoFish has started. The current players are: ",
                "newcard":"You got %s.",
                "lostPlayer":"%s has left GoFish.",
                "lowPlayers":"The game must have atleast three participants in order to start.",
                "playerleft": "%s has left the channel. Continuing game without them.",
                "gameScore":"The scores for this round were:",
                "totalScore":"The total scores are:",
                "ingame":"You are already in the game.",
                "invalidCommand":"`%s` is an invalid command. Type `%s:gf help` for a list of commands.",
                "invalidCard":"`%s` is not a valid card. Please choose from [A,2,3,4,5,6,7,8,9,10,J,Q,K].",
                "askCards":"Does %s have any %ss?",
                "gotCards":"%s got %s %ss from %s.",
                "noCards":"No, Go Fish!",
                "poolCard":"You got a %s from the pool.",
                "notPlaying":"%s is not playing GoFish right now.",
                "completeSet": "%s just completed a set of %ss. He has earned 1 point.",
                "mustHaveCard":"You must have atleast 1 %s card in order to ask for it."
    }
    
    def __init__(self,bot):
        Command.__init__(self,bot)
        self.players = []
        self.gameInProgress = False
        self.totalScores = {}

    def checkPermissions(self,event,*args):
        base = args[0].lower()
        print(base,"permissions")
        if base in ["join","leave"]: return True
        elif base in ["start"]:
            return event.source.nick in self.players
        elif self.gameInProgress:
            if base in ["cards"]:
                return True
            else:
                if self.playerOrder[self.curplayer] == event.source.nick:
                    return args[0] in self.playerOrder

        return False
    
    def checkArgs(self,event,*args):
        base = args[0].lower()
        if base in ["join","leave","start"]:
            return len(args) == 1
        else:
            if self.gameInProgress: 
                if args[0] in self.playerOrder:
                    if args[1].upper() not in cardClasses.Card.ranks:
                        self.privMsg(event,self.messages["invalidCard"] % args[1])
                        return False
                    else:
                        return True
                else:
                    self.privMsg(event,self.messages["notPlaying"] % args[0])
                    return False
            
        
    def on_call(self,event,*args):
        base = args[0].lower()
        
        if base == "start":
            self.startgame(event)
        
        elif base == "join":
            self.join(event)
        
        elif base == "leave":
            self.leave(event)
        
        else:
            print(args)
            self.play(event,*args)
        
    
    def play(self,event,*args):
        target = args[0]
        cardRank = args[1].upper()
        
        for card in self.curPlayers[event.source.nick].cards:
            if card.rank == cardRank:
                break
        else:
            self.privMsg(event,self.messages["mustHaveCard"] % cardRank)
            return
        
        self.pubMsg(event,self.messages["askCards"] % args)
        targetCards = self.curPlayers[args[0]].cards
        
        gotCard = []
        for card in targetCards:
            if card.rank == cardRank:
                self.curPlayers[target].cards.remove(card)
                self.getCurrentHand().cards.append(card)
                gotCard.append(card)
        
        if gotCard:
            self.pubMsg(event,self.messages["gotCards"] % (event.source.nick, str(len(gotCard)),args[1],target))
            self.privMsg(event,self.messages["newcard"] % ", ".join(str(card) for card in gotCard))
        else:
            self.pubMsg(event,self.messages["noCards"])
            card = self.curStack.deal(1)
            self.privMsg(event,self.messages["poolCard"] % card)
            self.curPlayers[event.source.nick].cards.append(card)
        
        self.checkHand(event)
        self.nextTurn(event)
        
    def join(self,event):
        if event.source.nick not in self.players:
            self.players.append(event.source.nick)
            self.pubMsg(event,self.messages["newPlayer"] % event.source.nick)
        else:
            self.privMsg(event,self.messages["ingame"] % self.bot.callsign)

    
    def leave(self,event):
        if event.source.nick in self.players:
            self.players.remove(event.source.nick)
            self.pubMsg(event,self.messages["lostPlayer"] % event.source.nick)
        else:
            pass


    def getCurrentHand(self):
        return self.curPlayers[self.playerOrder[self.curplayer]]        
    
    
    def checkHand(self,event):
        cardCount = {}
        nick = event if type(event) == str else event.source.nick
        for card in self.curPlayers[nick].cards:
            try:
                cardCount[card.rank] += 1
            except KeyError:
                cardCount[card.rank] = 1
        
        for rank in cardCount.keys():
            if cardCount[rank] == 4:
                self.pubMsg(event,self.messages["completeSet"] % (nick,rank))
                self.curPlayers[nick].score += 1
    
    def startgame(self,event):
        #Don't allow few players
        if len(self.players) < 3:
            self.pubMsg(event,self.messages["lowPlayers"])
            return
        
        #set game variables
        self.gameInProgress = True
        self.curStack = cardClasses.Stack()
        self.curPlayers = {}
        self.playerOrder = []
        self.curplayer = 0
        
        #add currently joined players in random order
        temp = copy.deepcopy(self.players)
        for x in range(len(temp)):
            self.playerOrder.append(temp.pop(random.randint(0,len(temp)-1)))
        
        #give all players a hand and 7 cards
        for player in self.playerOrder:
            self.curPlayers[player] = cardClasses.Hand(player)
            self.curPlayers[player].addCard(*self.curStack.deal(7))
            self.checkHand(player)
        
        #say the game is starting and pass the turn to the first player
        self.pubMsg(event, self.messages["newgame"]+", ".join(self.playerOrder))
        self.showAllHands(event)
        self.nextTurn(event, 0)
    
    
    def nextTurn(self,event,playerIndex = -1):
        if playerIndex == -1:
            playerIndex = self.curplayer + 1
        
        while playerIndex != len(self.curPlayers) and not self.bot.channels[self.bot.channelName].has_user(self.playerOrder[playerIndex]):
            self.pubMsg(event,self.messages["playerleft"] % self.playerOrder[playerIndex])
            self.players.remove(self.playerOrder[playerIndex])
            playerIndex += 1
        
        if playerIndex == len(self.curPlayers):
            self.nextTurn(event, 0)
        else:
            self.curplayer = playerIndex
            self.pubMsg(event,self.messages["newturn"] % self.playerOrder[self.curplayer])
        
    
    def showHand(self,event):
        self.curPlayers[event.source.nick].sort()
        self.privMsg(event,self.messages["cards"] % ( ", ".join(self.getCurrentHand().cards),int(self.getCurrentHand())))
    
    
    def endGame(self,event):
        self.gameInProgress = False
    
    def showAllHands(self,event):
        for x in self.playerOrder:
            self.curPlayers[x].sort()
            self.privMsg(x,self.messages["cards"] % ", ".join(str(y) for y in self.curPlayers[x].cards))
        

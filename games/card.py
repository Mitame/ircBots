from mainbot.commands import Command
import random
import copy

class blackjack(Command):
    arguments = []
    permissionLevel = -1
    permitExtraArgs = True
    manArgCheck = False
    defaultArgs = []
    callname = "bj"
    
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
    
    class Card():
        suits = ["H","D","C","S"]
        ranks = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
        value = [0,2,3,4,5,6,7,8,9,10,10,10,10]
        def __init__(self,suit,rank):
            self.suit = suit
            self.rank = rank
        
        def __str__(self):
            return self.suit+self.rank
        
        def __int__(self):
            return self.ranks.index(self.rank)
        
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
            for suit in blackjack.Card.suits:
                for rank in blackjack.Card.ranks:
                    self.cards.append(blackjack.Card(suit,rank))
        
    class Hand():
        def __init__(self,name):
            self.cards = []
            self.name = name
        
        def addCard(self,*cards):
            self.cards.extend(cards)
        def __int__(self):
            acount = 0
            result = 0
            for card in self.cards:
                i = blackjack.Card.ranks.index(card.rank)
                if i == 0:
                    acount += 1
                else:
                    result += blackjack.Card.value[i]
            
            for x in range(acount):
                if result + 11 > 21:
                    result += 1
                else:
                    result += 11
            return result
        
        def getScore(self):
            x = self.__int__()
            
            return x if x <=21 else 0
                 
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
        
        
    def getCurrentHand(self):
        return self.curPlayers[self.playerOrder[self.curplayer]]        
    
    def start(self,event):
        if len(self.players) == 0:
            self.pubMsg(event,self.messages["noPlayers"])
            return
        
        self.gameInProgress = True
        self.curStack = self.Stack()
        self.curPlayers = {}
        self.playerOrder = []
        self.curplayer = 0
        PlayerOrder = copy.deepcopy(self.players)
        for x in range(len(PlayerOrder)):
            self.playerOrder.append(PlayerOrder.pop(random.randint(0,len(PlayerOrder)-1)))
        
        for player in self.playerOrder:
            self.curPlayers[player] = self.Hand(player)
            self.curPlayers[player].addCard(*self.curStack.deal(2))
        
        self.pubMsg(event, self.messages["newgame"]+", ".join(self.playerOrder))
        self.passTurn(event, 0)
    
    def showHand(self,event):
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
            self.pubMsg(event,(x.name+" | "+str(x.getScore())))
        
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
        
        elif base in ["join","leave","quit"]:
            return True
        
        elif base in ["start"]:
            if self.bot.getPermLevel(event) >= 3:
                return True
            else:
                return False
                
    
    def checkArgs(self,event,*args):
        return True
        
class ison(Command):
    arguments = ["str"]
    permissionLevel = 0
    permitExtraArgs = False
    manArgCheck = False
    defaultArgs = []
    callname = "ison"
    
    def on_call(self,event,*args):
        self.pubMsg(event,self.bot.channels[self.bot.channelName].has_user(args[0]))
        

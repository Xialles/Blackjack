
'''
#####    ##         ##      ####    ##  ##       ##     ##      ####    ##  ##  
 ##  ##   ##        ####    ##  ##   ## ##        ##    ####    ##  ##   ## ##   
 #####    ##       ##  ##   ##       ####         ##   ##  ##   ##       ####    
 ##  ##   ##       ##  ##   ##       ####         ##   ##  ##   ##       ####    
 ##  ##   ##       ######   ##  ##   ## ##    ##  ##   ######   ##  ##   ## ##   
 #####    ######   ##  ##    ####    ##  ##    ####    ##  ##    ####    ##  ##  
                                                                                 
created with ASCII art
'''

'''
Thing To Do:
explanation of the rules
option to double the bet
option to split cards when they are equall
keep track of winning percentage
put the open .save file in a function
GET RID OF ALL THE GLOBAL VARIABLES
'''
import random
import pandas as pd
import numpy as np
import pathlib 

#The deck of card is described in a dictionary
deck = {
    '1':{'card':'2', 'value':2},
    '2':{'card':'3', 'value':3},
    '3':{'card':'4', 'value':4},
    '4':{'card':'5', 'value':5},
    '5':{'card':'6', 'value':6},
    '6':{'card':'7', 'value':7},
    '7':{'card':'8', 'value':8},
    '8':{'card':'9', 'value':9},
    '9':{'card':'10', 'value':10},
    '10':{'card':'Jack', 'value':10},
    '11':{'card':'Queen', 'value':10},
    '12':{'card':'King', 'value':10},
    '13':{'card':'Ace', 'value':11}
}
         
def getcard (player, theDeck, deck):
    global player1CardsList 
    global bankCardsList 
    pick = random.choice(theDeck) 
    
    #get a card for the player and append it to its list
    if  player == 'player1':
        player1Cards.append(deck[pick]['card'])
        player1Value.append(deck[pick]['value'])
        #formating for a nice printable string    
        player1CardsList = ''
        for card in player1Cards:
            player1CardsList += card + ', '
        player1CardsList = player1CardsList[:-2]

    #get a card for the bank and append it to its list
    elif  player == 'bank':
        bankCards.append(deck[pick]['card'])    
        bankValue.append(deck[pick]['value'])
        #formating for a nice printable string    
        bankCardsList = ''
        for card in bankCards:
            bankCardsList += card + ', '
        bankCardsList = bankCardsList[:-2]
    theDeck.remove(pick)
    
#count the points
def countPoints(playerCards, playerValue, bankCards, bankValue):
    global player1Points  
    player1Points = 0
    global bankPoints 
    bankPoints = 0
    
    for card in player1Value:
        player1Points += card
    if player1Points > 21:
        if player1Cards.count("Ace") > 0:
            Aces = player1Cards.count("Ace")
            player1Points = player1Points - 10 * Aces
    for card in bankValue:
        bankPoints += card
    if bankPoints > 21:
        if bankCards.count("Ace") > 0:
            Aces = bankCards.count("Ace")
            bankPoints = bankPoints - 10 * Aces    

def printOutput(printPlayer1=False, printBank=False):
    if printPlayer1:
        print(yourName + " this are your cards: ", player1CardsList, ". You have: ", player1Points, "points.")
    if printBank:
        print("The bank has: ", bankCardsList, ". The bank has" , bankPoints, 'points.')

def printCredits(yourName, credits):
    print(yourName, ", you have" , credits , "credits.")
    
def start():          
    global credits 
    global player1Cards 
    global player1Value
    global bankCards 
    global bankValue
    global player1Cash
    global df
    
    player1Cards = []
    player1Value = []
    bankCards = []
    bankValue = []    
    
    #the actual deck of cards 52 cards. When a card is given to a player/bank
    #it is taken out of the deck.
    global theDeck
    theDeck = ['1','2','3','4','5','6','7','8','9','10','11','12','13',
               '1','2','3','4','5','6','7','8','9','10','11','12','13',
               '1','2','3','4','5','6','7','8','9','10','11','12','13',
               '1','2','3','4','5','6','7','8','9','10','11','12','13',
               ]
#place your bets
    while True:
        try:
            bet = int(input("How much do you want to bet?"))
            break
        except ValueError:
            print("Please only insert digits")  
    
    #dealing the cards 2 for the player and 1 for the bank
    getcard('player1', theDeck, deck)
    getcard('player1', theDeck, deck)
    getcard('bank', theDeck, deck)
    countPoints(player1Cards, player1Value, bankCards, bankValue)
    printOutput(printPlayer1=True, printBank=True)
    
    while True:
        if player1Points == 21:
            break
        wantCard = input(yourName+", do you want another card? y/n ")
        print('\n')
        if wantCard == "Y" or wantCard == 'y':
            getcard('player1', theDeck, deck)
            countPoints(player1Cards, player1Value, bankCards, bankValue)
            if player1Points > 21:
                printOutput(printPlayer1=True)
                print("You're busted, game over!")
                credits -= bet
                printCredits(yourName, credits)
                break
            elif player1Points == 21:
                printOutput(printPlayer1=True)
                break
            else:
                countPoints(player1Cards, player1Value, bankCards, bankValue)
                printOutput(printPlayer1=True)
        else:
            break
    #bank getting cards
    if player1Points <= 21: 
        getcard('bank', theDeck, deck)
        countPoints(player1Cards, player1Value, bankCards, bankValue)
        while bankPoints < 17:
            getcard('bank', theDeck, deck)
            countPoints(player1Cards, player1Value, bankCards, bankValue)
        if bankPoints > 21:
            printOutput(printBank=True)
            print("The bank has busted, you are a winner")
            credits += bet
            printCredits(yourName, credits)
        elif bankPoints >= player1Points:
            printOutput(printBank=True)
            print("The bank has more (or equall) points, you lost you're money!")
            credits -= bet
            printCredits(yourName, credits)
        else:
            printOutput(printBank=True)
            credits += bet
            print("You have more point than the bank, you are a winner!")
            printCredits(yourName, credits)
    playAgain = input(yourName+ ", do you want to play again ? y/n ")
    if playAgain == "Y" or wantCard == 'y':
        print('\n')
        ### Loop to restart the game         
        start()
    else:
        print('\n')
        printCredits(yourName, credits)
        df.iloc[nRow,1] = credits
        df = df[["name", "credits"]].sort_values(by=["credits", "name"], ascending=False)
        df.to_csv('Blackjack.csv', index=False)

        
        
#retrieving game data, if filename not exist, create it       
filename = pathlib.Path("Blackjack.csv")
if not filename.exists ():
    createFile = open(filename, mode='w+')
    createFile.close()
    print ("A file was created to save the progress. The filename is Blackjack.csv")
    df = pd.DataFrame(columns=['name' , 'credits']) #create necesary columns
    df.to_csv('Blackjack.csv', index = False) 

df = pd.DataFrame(pd.read_csv(filename))
print(df)

yourName = input("Player 1, what is you're name?")
#yourName = 'Xialles'

#check if the name exist, if not,create the name. 
#nRow is the name of the (new) name (yourName)
nRow = df[df['name']==yourName].index.values
if nRow.size > 0:
    nRow= (nRow[0])
else:
    df.loc[len(df.index)] = [yourName,1000]
    nRow = len(df.index)-1

credits = df.iloc[nRow,1]
printCredits(yourName, credits)

start()



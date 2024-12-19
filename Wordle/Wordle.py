import pygame
import random

class LetterBox:
    def __init__(self, xPos, yPos):
        self.font = pygame.font.SysFont("clear sans", 50)
        self.box_surf = pygame.Surface((55, 55))
        self.box_rect = self.box_surf.get_rect(topleft=(xPos, yPos))
        self.box_surf.fill("#787c7f")
        self.letter = ""

    def display(self, scr):
        scr.blit(self.box_surf, self.box_rect)

    def displayLetter(self):
        text_surf = self.font.render(self.letter.upper(), True, "#ffffff")
        screen.blit(text_surf, (self.box_rect.x+14, self.box_rect.y+12))

class Button:
    def __init__(self, text, color, posX, posY, sizeX, sizeY):
            #Text
        self.button_font = pygame.font.SysFont("clear sans", 30)
        self.button_text = self.button_font.render(text, True, (255, 255, 255))
        self.text_rect = self.button_text.get_rect(center=(posX, posY))
            #Background
        self.button_surf = pygame.Surface((sizeX, sizeY))
        self.button_surf.fill(color)
        self.button_rect = self.button_surf.get_rect(center=(posX, posY))

    def display(self, screen):
        screen.blit(self.button_surf, self.button_rect)
        screen.blit(self.button_text, self.text_rect)

class KeyBox:
    def __init__(self, let, xPos, yPos):
        self.letter = let
            #Text
        self.font = pygame.font.SysFont("clear sans", 25)
        self.key_text = self.font.render(self.letter, True, (255, 255, 255))
        self.keytext_rect = self.key_text.get_rect(center=(xPos, yPos))
            #Box
        self.key_surf = pygame.Surface((30, 40))
        self.key_rect = self.key_surf.get_rect(center=(xPos, yPos))
        self.key_surf.fill("#B5BAC4")

    def display(self, screen):
        screen.blit(self.key_surf, self.key_rect)
        screen.blit(self.key_text, self.keytext_rect)

#---------------------------------------------------------------------------------------------





pygame.init()
screen = pygame.display.set_mode((600, 700))

#---Wordle color Palette---
black = "#000000"
gray = "#787c7f"
green = "#6ca965"
yellow = "#c8b653"
white = "#ffffff"
lightgray = "#B5BAC4"

#Multidimensional Array
#[box, box, box, box, box] 1
#[box, box, box, box, box] 2
#[box, box, box, box, box] 3
#[box, box, box, box, box] 4
#[box, box, box, box, box] 5
#[box, box, box, box, box] 6
boxes = [[LetterBox(x*60 + 150, j*60+100) for x in range(5)] for j in range(6)]

#Keyboard Display
allLetters = "QWERTYUIOPASDFGHJKLZXCVBNM"
keys = {allLetters[i]: KeyBox(allLetters[i], 143+i*35, 550) for i in range(0, 10)}
keys.update({allLetters[i]: KeyBox(allLetters[i], -185+i*35, 600) for i in range(10, 19)})
keys.update({allLetters[i]: KeyBox(allLetters[i], -465+i*35, 650) for i in range(19, 26)})

#Variables
guesses = []
currentRow = 0
currentLetter = 0
words = open(r"C:\Users\bliss\source\repos\Wordle\five_letter_words.txt").read().split("\n")
remainingWords = words.copy()
won = False
mode = "computer"
targetWord = words[random.randint(0, len(words))]

#Buttons
nextButton = Button("NEXT", green, 300, 490, 80, 40)
compButton = Button("COMPUTER", gray, 75, 70, 130, 30)
playerButton = Button("PLAYER", gray, 540, 70, 100, 30)

#Title
title_font = pygame.font.SysFont("Clear Sans", 50)
title_surf = title_font.render("Wordle", True, black)
title_rect = title_surf.get_rect(midtop=(300, 10))

while True:
    screen.fill("#ffffff")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            SystemExit()

        #Computer Button -------------------------------------------------
        if event.type == pygame.MOUSEBUTTONDOWN and compButton.button_rect.collidepoint(event.pos):
            mode = "computer"

            #Reset color
            for i in range(6):
                for j in range(5):
                    boxes[i][j].box_surf.fill(gray)

            [keys[x].key_surf.fill(lightgray) for x in allLetters]

            #Reset Letters
            for i in range(6):
                for j in range(5):
                    boxes[i][j].letter = ""

            #Reset variables
            currentRow = 0
            currentLetter = 0
            remainingWords = words.copy()
            won = False
            targetWord = words[random.randint(0, len(words))]
            guesses = []

        #Player Button -------------------------------------------------
        if event.type == pygame.MOUSEBUTTONDOWN and playerButton.button_rect.collidepoint(event.pos):
            mode = "player"

            #Reset color
            for i in range(6):
                for j in range(5):
                    boxes[i][j].box_surf.fill(gray)

            [keys[x].key_surf.fill(lightgray) for x in allLetters]

            #Reset Letters
            for i in range(6):
                for j in range(5):
                    boxes[i][j].letter = ""

            #Reset variables
            currentRow = 0
            currentLetter = 0
            remainingWords = words.copy()
            won = False
            targetWord = words[random.randint(0, len(words))]
            guesses = []


        #Player Mode --------------------------------------------------------
        if event.type == pygame.KEYDOWN and not won and mode == "player":
            if currentRow < 6:
                if event.key == pygame.K_BACKSPACE:
                    if currentLetter > 0:
                        currentLetter -= 1
                        boxes[currentRow][currentLetter].letter = ""
                
                #Type into wordle
                if event.unicode.isalpha():
                    if currentLetter <= 4:
                        boxes[currentRow][currentLetter].letter = event.unicode
                        currentLetter += 1                    

                #Press Enter to Submit Guess
                if event.key == pygame.K_RETURN:
                    if currentLetter >= 5:

                        #Say if it's already Guessed
                        if "".join([b.letter for b in boxes[currentRow]]).lower() in guesses:
                            print("Already Guessed")

                        #If it's in word list, add the word to guesses list
                        elif "".join([b.letter for b in boxes[currentRow]]).lower() in words:
                            guesses.append("".join([b.letter for b in boxes[currentRow]]))

                            

                            #Iterate through guessed word, changing color of each letter
                            for i in range(5):
                                remainingWords = [w for w in remainingWords if len(w) == 5]
                                #Green
                                if guesses[currentRow][i] == targetWord[i]:
                                    boxes[currentRow][i].box_surf.fill(green)
                                    remainingWords = list([w for w in remainingWords if guesses[currentRow][i] == w[i]])
                                    keys[boxes[currentRow][i].letter.upper()].key_surf.fill(green)
                                    
                                #Yellow
                                elif guesses[currentRow][i] in targetWord:
                                    boxes[currentRow][i].box_surf.fill(yellow)
                                    remainingWords = list([w for w in remainingWords if guesses[currentRow][i] in w])
                                    keys[boxes[currentRow][i].letter.upper()].key_surf.fill(yellow)
                                #Gray
                                else:
                                    boxes[currentRow][i].box_surf.fill(gray)
                                    remainingWords = list([w for w in remainingWords if guesses[currentRow][i] not in w])
                                    keys[boxes[currentRow][i].letter.upper()].key_surf.fill(gray)

                            #Stop game when won
                            if "".join([b.letter for b in boxes[currentRow]]) == targetWord:
                                mode = 1
                                won = True

                            currentLetter = 0
                            currentRow += 1
                        else:
                            print("Not in Word List")

        #Computer Mode--------------------------------------------------------
        if not won and mode == "computer":
            if currentRow < 6:
                #Press Next to Generate Guess
                if event.type == pygame.MOUSEBUTTONDOWN and nextButton.button_rect.collidepoint(event.pos):
                    guesses.append(remainingWords[random.randint(0,len(remainingWords)-1)])

                    #Set the boxes to the new guess
                    for i in range(5):
                        boxes[currentRow][i].letter = guesses[currentRow][i]

                    #Iterate through guessed word, changing color of each letter
                    for i in range(5):
                        remainingWords = [w for w in remainingWords if len(w) == 5]

                        #Green
                        if guesses[currentRow][i] == targetWord[i]:
                            boxes[currentRow][i].box_surf.fill(green)
                            remainingWords = list([w for w in remainingWords if guesses[currentRow][i] == w[i]])
                            keys[boxes[currentRow][i].letter.upper()].key_surf.fill(green)
                                    
                        #Yellow
                        elif guesses[currentRow][i] in targetWord:
                            boxes[currentRow][i].box_surf.fill(yellow)
                            remainingWords = list([w for w in remainingWords if guesses[currentRow][i] in w and guesses[currentRow][i] != w[i]])
                            keys[boxes[currentRow][i].letter.upper()].key_surf.fill(yellow)

                        #Gray
                        else:
                            boxes[currentRow][i].box_surf.fill(gray)
                            remainingWords = list([w for w in remainingWords if guesses[currentRow][i] not in w])
                            keys[boxes[currentRow][i].letter.upper()].key_surf.fill(gray)
                    #Stop game when won
                    if "".join([b.letter for b in boxes[currentRow]]) == targetWord:
                        mode = 0
                        won = True

                    currentRow += 1


                
    #Display the Title
    screen.blit(title_surf, title_rect)
    pygame.draw.line(screen, black, (10, 50), (590, 50))

    #Display all boxes to screen
    [b.display(screen) for j in range(6) for b in boxes[j]]
    [b.displayLetter() for j in range(6) for b in boxes[j]]

    #Display Buttons
    if mode == "computer":
        nextButton.display(screen)
    compButton.display(screen)
    playerButton.display(screen)

    #Display Keys
    [keys[a].display(screen) for a in allLetters]

    pygame.display.update()

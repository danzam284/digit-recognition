import cv2 as cv
import os 
import os.path
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import pygame
import PIL
from PIL import Image

#colors
DRAW = (0, 0, 0)
BACKGROUND = (255, 255, 255)
COLORCYCLE = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (230, 230, 250), (255, 192, 203)]

#Sets up the pygame
pygame.init()
clock = pygame.time.Clock()
user_width, user_height = 1440, 900
screen = pygame.display.set_mode((user_width, user_height), pygame.FULLSCREEN)

#used for the questionmark in bottom left
help = False

#sets up the color cycle
currCol = 0
colorWall = COLORCYCLE[currCol]

#Gets the trained ML model from a file
model = tf.keras.models.load_model('saved/my_model')
print(user_width, user_height)
#Defines variables for the rectangle buttons
rClear = pygame.Rect(user_width - 1230, user_height - 510, 180, 130)
rQuit = pygame.Rect(user_width - 390, user_height - 510, 180, 130)
rGo = pygame.Rect(user_width / 2 - 90, user_height - 190, 180, 130)
clearcol = BACKGROUND
quitcol = BACKGROUND
gocol = BACKGROUND

#Creates the various fonts used
pygame.font.init() 
myfont = pygame.font.SysFont('Comic Sans MS', 30)
answerFont = pygame.font.SysFont('Comic Sans MS', 120)
danfont = pygame.font.SysFont('Comic Sans MS', 5)
questionfont = pygame.font.SysFont('Comic Sans MS', 60)
smallerfont = pygame.font.SysFont('Comic Sans MS', 20)

#Defining all of the texts used through the program
tagText = myfont.render("Daniel Zamloot - 2022", False, colorWall)
questionText = questionfont.render("?", False, colorWall)
text = myfont.render("", False, BACKGROUND)
answerText = ""
answer = answerFont.render(answerText, False, BACKGROUND)
clearText = myfont.render("CLEAR", False, colorWall)
quitText = myfont.render("QUIT", False, colorWall)
goText = myfont.render("GO", False, colorWall)
helpText1 = smallerfont.render("DRAW INSIDE THE CENTER BOX", False, colorWall)
helpText2 = smallerfont.render("PRESS GO TO GET A GUESS", False, colorWall)
helpText3 = smallerfont.render("PRESS CLEAR TO ERASE DRAWING", False, colorWall)
helpText4 = smallerfont.render("PRESS QUIT TO STOP THE GAME", False, colorWall)

#Other variables used throughout the program
pressed = False
rects = []
colors = []

#sets the background color
screen.fill((99, 3, 48))

#creates the array for drawing on and sets the rects and colors list appropriately
for i in range(28):
	for j in range(28):
		rects.append(pygame.Rect(user_width / 2 - 140 + (10 * i), user_height / 2 - 140 + (10 * j), 10, 10))
		colors.append(BACKGROUND)

#Function which is called on every loop and updates all changes
def draw(all=-1):
	#colors in background
	screen.fill((99, 3, 48))

	#draws the coloring grid to screen
	for i in range(len(rects)):
		pygame.draw.rect(screen, colors[i], rects[i])

	#draws the lines around the coloring grid
	pygame.draw.line(screen, colorWall, (user_width / 2 - 140, user_height / 2 - 140), (user_width / 2 - 140, user_height / 2 + 140), 10)
	pygame.draw.line(screen, colorWall, (user_width / 2 - 140, user_height / 2 - 140), (user_width / 2 + 140, user_height / 2 - 140), 10)
	pygame.draw.line(screen, colorWall, (user_width / 2 + 140, user_height / 2 - 140), (user_width / 2 + 140, user_height / 2 + 140), 10)
	pygame.draw.line(screen, colorWall, (user_width / 2 + 140, user_height / 2 + 140), (user_width / 2 - 140, user_height / 2 + 140), 10)

	#Sets up the alternating color boxes
	pygame.draw.rect(screen, colorWall, [200, 380, 200, 150])
	pygame.draw.rect(screen, colorWall, [user_width - 400, 380, 200, 150])
	pygame.draw.rect(screen, colorWall, [user_width / 2 - 100, 700, 200, 150])

	#draws the buttons on screen
	pygame.draw.rect(screen, clearcol, rClear)
	pygame.draw.rect(screen, quitcol, rQuit)
	pygame.draw.rect(screen, gocol, rGo)

	#Draws the answer text on screen
	text = myfont.render("I PREDICT THAT YOU DREW", False, colorWall)
	answer = answerFont.render(answerText, False, colorWall)
	screen.blit(text, (500, 130))
	screen.blit(answer, (680, 150))

	#Draws the button text on screen
	clearText = myfont.render("CLEAR", False, colorWall)
	quitText = myfont.render("QUIT", False, colorWall)
	goText = myfont.render("GO", False, colorWall)
	screen.blit(clearText, (250, 433))
	screen.blit(quitText, (user_width - 345, 433))
	screen.blit(goText, (user_width / 2 - 25, 753))

	#Draws other texts to screen
	tagText = myfont.render("Daniel Zamloot - 2021", False, colorWall)
	screen.blit(tagText, (user_width - 320, user_height - 45))
	questionText = questionfont.render("?", False, colorWall)
	screen.blit(questionText, (10, user_height - 85))

	#If touching the questionmark then draw help box and texts
	if help:
		pygame.draw.rect(screen, colorWall, [0, user_height - 300, 400, 300])
		pygame.draw.rect(screen, (99, 3, 48), [10, user_height - 290, 380, 280])
		helpText1 = smallerfont.render("DRAW INSIDE THE CENTER BOX", False, colorWall)
		helpText2 = smallerfont.render("PRESS GO TO GET A GUESS", False, colorWall)
		helpText3 = smallerfont.render("PRESS CLEAR TO ERASE DRAWING", False, colorWall)
		helpText4 = smallerfont.render("PRESS QUIT TO STOP THE GAME", False, colorWall)
		screen.blit(helpText1, (40, user_height - 260))
		screen.blit(helpText2, (60, user_height - 190))
		screen.blit(helpText3, (30, user_height - 120))
		screen.blit(helpText4, (35, user_height - 50))
	#Update all of these changes
	pygame.display.flip()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
		if event.type == pygame.MOUSEBUTTONUP: #stops drawing
			pressed = False
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #starts drawing
			pressed = True
			pos = pygame.mouse.get_pos()

			#checks if buttons are clicked
			if rGo.collidepoint(pos):
				pixels =[]
				for i in range(28):
					col = []

					#converts the pixels drawn to an array
					for j in range(28):
						col.append(colors[j * 28 + i])
					pixels.append(col)
				#coonverts the array to an image
				arr = np.invert(np.array(pixels, dtype=np.uint8))
				img = arr[:, :, 0]
				img = np.array([img])
				#creates a prediction based off the image
				prediction = model.predict(img)
				answer = np.argmax(prediction)
				answerText = str(answer)
				screen.blit(text, (300, 100))
			if rQuit.collidepoint(pos):
				pygame.quit()
			if rClear.collidepoint(pos):
				#sets all the grid boxes to white
				answerText = ""
				colors = [BACKGROUND] * 784
		if event.type == pygame.MOUSEMOTION: #If mouse moves
			pos = pygame.mouse.get_pos()

			#checks if mouse is on question mark
			if pos[0] < 65 and pos[1] > user_height - 65:
				help = True
				print("yes")
			else:
				help = False

			#changes color if mouse is on a button
			if rGo.collidepoint(pos):
				gocol = (99, 3, 48)
			else:
				gocol = BACKGROUND
			if rQuit.collidepoint(pos):
				quitcol = (99, 3, 48)
			else:
				quitcol = BACKGROUND
			if rClear.collidepoint(pos):
				clearcol = (99, 3, 48)
			else:
				clearcol = BACKGROUND

			#If mouse is down, draw on the grid
			if pressed: 
				answerText = ""
				for i in range(len(rects)):
					if rects[i].collidepoint(pos):
						colors[i] = DRAW
						if i % 28 > 0:
							colors[i - 1] = DRAW
						if i % 28 < 0:
							colors[i + 1] = DRAW
						if i > 28:
							colors[i - 28] = DRAW
						if i < 756:
							colors[i + 28] = DRAW
						if i < 756 and i % 28 < 0:
							colors[i + 29] = DRAW
						if i < 756 and i % 28 > 0:
							colors[i + 27] = DRAW
						if i > 28 and i % 28 > 0:
							colors[i - 29] = DRAW
						if i > 28 and i % 28 < 0:
							colors[i - 27] = DRAW 
		if event.type == pygame.KEYDOWN:
			#If enter key then run algorithm
			if event.key == pygame.K_RETURN:
				pixels =[]
				for i in range(28):
					col = []
					for j in range(28):
						col.append(colors[j * 28 + i])
					pixels.append(col)
				arr = np.invert(np.array(pixels, dtype=np.uint8))
				img = arr[:, :, 0]
				img = np.array([img])
				prediction = model.predict(img)
				answer = np.argmax(prediction)
				answerText = str(answer)
				screen.blit(text, (300, 100))
			if event.key == pygame.K_q:
				pygame.quit()
			if event.key == pygame.K_SPACE:
				answerText = ""
				colors = [BACKGROUND] * 784

	#Allows for the color cycle to occur			
	nxtIndex = (currCol + 1) % 8
	if colorWall == COLORCYCLE[nxtIndex]:
		currCol = nxtIndex

	#Slowly changes RGB val of current color until it is the same as set value
	if colorWall[0] < COLORCYCLE[nxtIndex][0]:
		colorWall = (colorWall[0] + 1, colorWall[1], colorWall[2])
	elif colorWall[0] > COLORCYCLE[nxtIndex][0]:
		colorWall = (colorWall[0] - 1, colorWall[1], colorWall[2])
	if colorWall[1] < COLORCYCLE[nxtIndex][1]:
		colorWall = (colorWall[0], colorWall[1] + 1, colorWall[2])
	elif colorWall[1] > COLORCYCLE[nxtIndex][1]:
		colorWall = (colorWall[0], colorWall[1] - 1, colorWall[2])
	if colorWall[2] < COLORCYCLE[nxtIndex][2]:
		colorWall = (colorWall[0], colorWall[1], colorWall[2] + 1)
	elif colorWall[2] > COLORCYCLE[nxtIndex][2]:
		colorWall = (colorWall[0], colorWall[1], colorWall[2] - 1)

	#Updates changes
	draw()
	clock.tick()

	

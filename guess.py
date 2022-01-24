import cv2 as cv
import os 
import os.path
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import pygame
import PIL
from PIL import Image

stats = []
with open('stats.txt') as f:
	lines = f.readlines()
	if lines == []:
		stats.append([0, 0])
		for _ in range(10):
			stats.append([0] * 12)
	else:
		lines[0] = lines[0].split(', ')
		stats.append(list(map(lambda x: int(x), lines[0][:2])))
		for i in range(1, 11):
			lines[i] = lines[i].split(', ')
			stats.append(list(map(lambda x: int(x), lines[i][:12])))
	f.close()

#colors
DRAW = (0, 0, 0)
BACKGROUND = (255, 255, 255)
COLORCYCLE = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (230, 230, 250), (255, 192, 203)]

#Sets up the pygame
pygame.init()
clock = pygame.time.Clock()
user_width, user_height = 1440, 900
screen = pygame.display.set_mode((user_width, user_height), pygame.FULLSCREEN)

#used for hover boxes
help = False
stat = False

#sets up the color cycle
currCol = 0
colorWall = COLORCYCLE[currCol]

#Gets the trained ML model from a file
model = tf.keras.models.load_model('/Users/danzam284/Desktop/Python Codes/saved/my_model')

#Defines variables for the rectangle buttons
rClear = pygame.Rect(user_width - 1230, user_height - 510, 180, 130)
rQuit = pygame.Rect(user_width - 390, user_height - 510, 180, 130)
rGo = pygame.Rect(user_width / 2 - 90, user_height - 190, 180, 130)
rYes = pygame.Rect(1090, 110, 80, 40)
rNo = pygame.Rect(1220, 110, 80, 40)
rZero = pygame.Rect(1035, 110, 30, 30)
rOne = pygame.Rect(1095, 110, 30, 30)
rTwo = pygame.Rect(1155, 110, 30, 30)
rThree = pygame.Rect(1215, 110, 30, 30)
rFour = pygame.Rect(1275, 110, 30, 30)
rFive = pygame.Rect(1035, 170, 30, 30)
rSix = pygame.Rect(1095, 170, 30, 30)
rSeven = pygame.Rect(1155, 170, 30, 30)
rEight = pygame.Rect(1215, 170, 30, 30)
rNine = pygame.Rect(1275, 170, 30, 30)

#keeps track of button colors
clearcol = BACKGROUND
quitcol = BACKGROUND
gocol = BACKGROUND
yescol = BACKGROUND
nocol = BACKGROUND
zerocol = BACKGROUND
onecol = BACKGROUND
twocol = BACKGROUND
threecol = BACKGROUND
fourcol = BACKGROUND
fivecol = BACKGROUND
sixcol = BACKGROUND
sevencol = BACKGROUND
eightcol = BACKGROUND
ninecol = BACKGROUND

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
answer = answerFont.render(answerText, False, colorWall)
clearText = myfont.render("CLEAR", False, colorWall)
quitText = myfont.render("QUIT", False, colorWall)
goText = myfont.render("GO", False, colorWall)
helpText1 = smallerfont.render("DRAW INSIDE THE CENTER BOX", False, colorWall)
helpText2 = smallerfont.render("PRESS GO TO GET A GUESS", False, colorWall)
helpText3 = smallerfont.render("PRESS CLEAR TO ERASE DRAWING", False, colorWall)
helpText4 = smallerfont.render("PRESS QUIT TO STOP THE GAME", False, colorWall)
statsText = myfont.render("STATS", False, colorWall)
checkText = myfont.render("WAS IT CORRECT?", False, colorWall)
yesText = smallerfont.render("YES", False, colorWall)
noText = smallerfont.render("NO", False, colorWall)
whichText = myfont.render("WHICH WAS CORRECT?", False, colorWall)

#Other variables used throughout the program
pressed = False
rects = []
colors = []
mode = 0
answer = -1
clickdelay = 0

#sets the background color
screen.fill((99, 3, 48))

#creates the array for drawing on and sets the rects and colors list appropriately
for i in range(28):
	for j in range(28):
		rects.append(pygame.Rect(user_width / 2 - 140 + (10 * i), user_height / 2 - 140 + (10 * j), 10, 10))
		colors.append(BACKGROUND)

#Saves new data to the local file for constant storage
def saveFile():
	with open('stats.txt', 'w') as f:
		f.truncate(0)
		for line in stats:
			f.write(', '.join(list(map(lambda x: str(x), line))) + '\n')

#Function which is called on every loop and updates all changes
def draw():
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
	statsText = myfont.render("STATS", False, colorWall)
	screen.blit(statsText, (0, 0))

	#If checking whether guess was correct or not
	if mode == 1:
		checkText = myfont.render("WAS IT CORRECT?", False, colorWall)
		screen.blit(checkText, (1050, 40))
		pygame.draw.rect(screen, colorWall, [1080, 100, 100, 60])
		pygame.draw.rect(screen, colorWall, [1210, 100, 100, 60])
		pygame.draw.rect(screen, yescol, rYes)
		pygame.draw.rect(screen, nocol, rNo)
		yesText = smallerfont.render("YES", False, colorWall)
		noText = smallerfont.render("NO", False, colorWall)
		screen.blit(yesText, (1108, 115))
		screen.blit(noText, (1243, 115))

	#If figuring out which one they actually drew
	if mode == 2:
		whichText = myfont.render("WHICH WAS CORRECT?", False, colorWall)
		screen.blit(whichText, (1000, 40))
		for i in range(5):
			if result != i:
				pygame.draw.rect(screen, colorWall, [1025 + 60 * i, 100, 50, 50])
			if result != 5 + i:
				pygame.draw.rect(screen, colorWall, [1025 + 60 * i, 160, 50, 50])
		if result != 0:
			pygame.draw.rect(screen, zerocol, rZero)
		if result != 1:
			pygame.draw.rect(screen, onecol, rOne)
		if result != 2:
			pygame.draw.rect(screen, twocol, rTwo)
		if result != 3:
			pygame.draw.rect(screen, threecol, rThree)
		if result != 4:
			pygame.draw.rect(screen, fourcol, rFour)
		if result != 5:
			pygame.draw.rect(screen, fivecol, rFive)
		if result != 6:
			pygame.draw.rect(screen, sixcol, rSix)
		if result != 7:
			pygame.draw.rect(screen, sevencol, rSeven)
		if result != 8:
			pygame.draw.rect(screen, eightcol, rEight)
		if result != 9:
			pygame.draw.rect(screen, ninecol, rNine)
		for i in range(5):
			if result != i:
				tempText = smallerfont.render(str(i), False, colorWall)
				screen.blit(tempText,(1045 + 60 * i, 110))
			if result != 5 + i:
				tempText = smallerfont.render(str(i + 5), False, colorWall)
				screen.blit(tempText,(1045 + 60 * i, 170))


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

	#If touching Stats then display a bunch of stat information
	if stat:
		pygame.draw.rect(screen, colorWall, [0, 0, user_width, user_height])
		textTotal = myfont.render("Total Attempts: " + str(stats[0][1]) + " Total Correct: " + str(stats[0][0]), False, (99, 3, 48))
		screen.blit(textTotal, (500, 0))
		largeStats = []
		largeStats.append(questionfont.render("0", False, (99, 3, 48)))
		largeStats.append(questionfont.render("1", False, (99, 3, 48)))
		largeStats.append(questionfont.render("2", False, (99, 3, 48)))
		largeStats.append(questionfont.render("3", False, (99, 3, 48)))
		largeStats.append(questionfont.render("4", False, (99, 3, 48)))
		largeStats.append(questionfont.render("5", False, (99, 3, 48)))
		largeStats.append(questionfont.render("6", False, (99, 3, 48)))
		largeStats.append(questionfont.render("7", False, (99, 3, 48)))
		largeStats.append(questionfont.render("8", False, (99, 3, 48)))
		largeStats.append(questionfont.render("9", False, (99, 3, 48)))

		for i in range(len(largeStats)):
			screen.blit(largeStats[i], (0, 155 + 70 * i))
		
		horizontal = questionfont.render("    Tries   Correct   Most Common Misconception", False, (99, 3, 48))
		screen.blit(horizontal, (0, 75))

		for i in range(10):
			pygame.draw.line(screen, (99, 3, 48), (0, 235 + 70 * i), (2000, 235 + 70 * i))
			rowtext = "                "
			rowtext += str(stats[i + 1][0]) + "                       "
			rowtext += str(stats[i + 1][1]) + "                         "
			arr = stats[i + 1][2:2 + i] + stats[i + 1][2 + i + 1:]
			if max(arr) == 0:
				rowtext += "n/a"
			else:
				rowtext += str(arr.index(max(arr)) + 1)
				
			row = myfont.render(rowtext, False, BACKGROUND)
			screen.blit(row, (0, 175 + 70 * i))
		
		pygame.draw.line(screen, (99, 3, 48), (70, 0), (70, 1000))
		pygame.draw.line(screen, (99, 3, 48), (0, 160), (2000, 160))
		pygame.draw.line(screen, (99, 3, 48), (250, 0), (250, 1000))
		pygame.draw.line(screen, (99, 3, 48), (522, 0), (522, 1000))

	#Update all of these changes
	pygame.display.flip()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			saveFile()
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
						if colors[j * 28 + i] == BACKGROUND:
							col.append(BACKGROUND)
						else:
							col.append(DRAW)
					pixels.append(col)
				#coonverts the array to an image
				arr = np.invert(np.array(pixels, dtype=np.uint8))
				img = arr[:, :, 0]
				img = np.array([img])
				img = np.array(img).reshape(-1, 28, 28, 1)
				#creates a prediction based off the image
				prediction = model.predict(img)
				answer = np.argmax(prediction)
				result = np.argmax(prediction)
				answerText = str(answer)
				screen.blit(text, (300, 100))
				mode = 1
			if rQuit.collidepoint(pos):
				saveFile()
				pygame.quit()
			if rClear.collidepoint(pos):
				#sets all the grid boxes to white
				answerText = ""
				colors = [BACKGROUND] * 784
				mode = 0
			if mode == 1:
				if rYes.collidepoint(pos):
					mode = 0
					stats[0][0] += 1
					stats[0][1] += 1
					stats[result + 1][0] += 1
					stats[result + 1][1] += 1
					answerText = ""
					colors = [BACKGROUND] * 784
				if rNo.collidepoint(pos):
					mode = 2
					clickdelay = 100

			#Update stats if guess was wrong
			if mode == 2 and clickdelay < 0:
				clicked = False
				if rZero.collidepoint(pos):
					stats[0][1] += 1
					stats[1][result + 2] += 1
					stats[1][0] += 1
					clicked = True
				elif rOne.collidepoint(pos):
					stats[0][1] += 1
					stats[2][result + 2] += 1
					stats[2][0] += 1
					clicked = True
				elif rTwo.collidepoint(pos):
					stats[0][1] += 1
					stats[3][result + 2] += 1
					stats[3][0] += 1
					clicked = True
				elif rThree.collidepoint(pos):
					stats[0][1] += 1
					stats[4][result + 2] += 1
					stats[4][0] += 1
					clicked = True
				elif rFour.collidepoint(pos):
					stats[0][1] += 1
					stats[5][result + 2] += 1
					stats[5][0] += 1
					clicked = True
				elif rFive.collidepoint(pos):
					stats[0][1] += 1
					stats[6][result + 2] += 1
					stats[6][0] += 1
					clicked = True
				elif rSix.collidepoint(pos):
					stats[0][1] += 1
					stats[7][result + 2] += 1
					stats[7][0] += 1
					clicked = True
				elif rSeven.collidepoint(pos):
					stats[0][1] += 1
					stats[8][result + 2] += 1
					stats[8][0] += 1
					clicked = True
				elif rEight.collidepoint(pos):
					stats[0][1] += 1
					stats[9][result + 2] += 1
					stats[9][0] += 1
					clicked = True
				elif rNine.collidepoint(pos):
					stats[0][1] += 1
					stats[10][result + 2] += 1
					stats[10][0] += 1
					clicked = True
				if clicked:
					mode = 0
					answerText = ""
					colors = [BACKGROUND] * 784

		if event.type == pygame.MOUSEMOTION: #If mouse moves
			pos = pygame.mouse.get_pos()

			#checks if mouse is on question mark
			if pos[0] < 65 and pos[1] > user_height - 65:
				help = True
			else:
				help = False

			#checks if mouse is on stats text
			if pos[0] < 100 and pos[1] < 50:
				stat = True
			else:
				stat = False

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
			if rNo.collidepoint(pos):
				nocol = (99, 3, 48)
			else:
				nocol = BACKGROUND
			if rYes.collidepoint(pos):
				yescol = (99, 3, 48)
			else:
				yescol = BACKGROUND
			if rZero.collidepoint(pos):
				zerocol = (99, 3, 48)
			else:
				zerocol = BACKGROUND
			if rOne.collidepoint(pos):
				onecol = (99, 3, 48)
			else:
				onecol = BACKGROUND
			if rTwo.collidepoint(pos):
				twocol = (99, 3, 48)
			else:
				twocol = BACKGROUND
			if rThree.collidepoint(pos):
				threecol = (99, 3, 48)
			else:
				threecol = BACKGROUND
			if rFour.collidepoint(pos):
				fourcol = (99, 3, 48)
			else:
				fourcol = BACKGROUND
			if rFive.collidepoint(pos):
				fivecol = (99, 3, 48)
			else:
				fivecol = BACKGROUND
			if rSix.collidepoint(pos):
				sixcol = (99, 3, 48)
			else:
				sixcol = BACKGROUND
			if rSeven.collidepoint(pos):
				sevencol = (99, 3, 48)
			else:
				sevencol = BACKGROUND
			if rEight.collidepoint(pos):
				eightcol = (99, 3, 48)
			else:
				eightcol = BACKGROUND
			if rNine.collidepoint(pos):
				ninecol = (99, 3, 48)
			else:
				ninecol = BACKGROUND

			#If mouse is down, draw on the grid
			if pressed: 
				answerText = ""
				for i in range(len(rects)):
					if rects[i].collidepoint(pos):
						colors[i] = colorWall

						#OPTIONAL for thicker lines
						"""
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
						"""
						
		if event.type == pygame.KEYDOWN:
			#If enter key then run algorithm
			if event.key == pygame.K_RETURN:
				pixels =[]
				for i in range(28):
					col = []
					#converts the pixels drawn to an array
					for j in range(28):
						if colors[j * 28 + i] == BACKGROUND:
							col.append(BACKGROUND)
						else:
							col.append(DRAW)
					print(col)
					pixels.append(col)
				#coonverts the array to an image
				arr = np.invert(np.array(pixels, dtype=np.uint8))
				img = arr[:, :, 0]
				img = np.array([img])
				img = np.array(img).reshape(-1, 28, 28, 1)
				#creates a prediction based off the image
				prediction = model.predict(img)
				answer = np.argmax(prediction)
				result = np.argmax(prediction)
				answerText = str(answer)
				screen.blit(text, (300, 100))
				mode = 1
			if event.key == pygame.K_q:
				saveFile()
				pygame.quit()
			if event.key == pygame.K_SPACE:
				#If space then clear board
				answerText = ""
				colors = [BACKGROUND] * 784
				mode = 0

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
	clickdelay -= 1
	#Updates changes
	draw()
	clock.tick()

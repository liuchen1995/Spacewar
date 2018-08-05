
import sys
import pygame as pg
from pygame.sprite import Group

#import self made classes
from settings import Settings
import gameFunctions as gf #Event checker and update screen
import mainMenu as mm #Main menu
import about as About
from ship import Ship
from alien import Alien
from gameStats import GameStats #Game stats that are changed during the duration of the game
from button import Button #A button class that can be called for every new button
from selector import Selector #Import the main menu selector
from scoreboard import Scoreboard #Score board for points, high score, lives, level ect.



def runGame():
	#Initialize game and create a window
	pg.init()
	pg.mixer.init()
	pg.time.delay(1000)
	#create a new object using the settings class
	setting = Settings()
	#creaete a new object from pygame display
	screen = pg.display.set_mode((setting.screenWidth, setting.screenHeight))
	#set window caption using settings obj
	pg.display.set_caption(setting.windowCaption)

	bgm = pg.mixer.Sound('music/背景音乐.ogg')
	bgm.set_volume(0.05)
	bgm.play(-1)


	fps = 120
	fclock = pg.time.Clock()

	playBtn = Button(setting, screen, "PLAY", 200)
	menuBtn = Button(setting, screen, "MENU", 250)
	aboutBtn = Button(setting, screen, "ABOUT", 250)
	quitBtn = Button(setting, screen, "QUIT", 300)

	#make slector for buttons
	sel = Selector(setting, screen)
	sel.rect.x = playBtn.rect.x + playBtn.width + 10
	sel.rect.centery = playBtn.rect.centery

	#Create an instance to stor game stats
	stats = GameStats(setting)
	sb = Scoreboard(setting, screen, stats)

	#Make a ship
	ship = Ship(setting, screen)
	#Ships for two player 
	ship1 = Ship(setting, screen)
	ship2 = Ship(setting, screen)

	#make a group of bullets to store
	bullets = Group()

	#Make an alien
	aliens = Group()
	gf.createFleet(setting, screen, ship, aliens)
	icon = pg.image.load('gfx/SpaceShip.png')
	pg.display.set_icon(icon)

	runGame = True

	#Set the two while loops to start mainMenu first
	while runGame:
		#Set to true to run main game loop
		while stats.mainMenu:
			mm.checkEvents(setting, screen, stats, sb, playBtn, aboutBtn, quitBtn, menuBtn, sel, ship, aliens, bullets)
			mm.drawMenu(setting, screen, sb, playBtn, menuBtn, aboutBtn, quitBtn, sel)

		while stats.mainGame:
			#Game functions
			gf.checkEvents(setting, screen, stats, sb, playBtn, quitBtn, sel, ship, aliens, bullets) #Check for events
			if stats.gameActive:
				gf.updateAliens(setting, stats, sb, screen, ship, aliens, bullets) #Update aliens
				gf.updateBullets(setting, screen, stats, sb, ship, aliens, bullets) #Update collisions
				ship.update() #update the ship
			gf.updateScreen(setting, screen, stats, sb, ship, aliens, bullets, playBtn, menuBtn, quitBtn, sel) #Update the screen

			fclock.tick(fps)

		while stats.mainAbout:
			About.checkEvents(setting, screen, stats, sb, playBtn, quitBtn, menuBtn, sel, ship, aliens, bullets)
			About.drawMenu(setting, screen, sb, menuBtn, quitBtn, sel)

		while stats.mainGame:
			if runGame == True:
				print("test")
#run the runGame method to run the game
runGame()

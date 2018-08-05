import sys
import pygame as pg
from time import sleep
from bullet import Bullet
from alien import Alien
import random
pauseBtnState = 1
back = False
clock = 0
def checkEvents(setting, screen, stats, sb, playBtn, quitBtn, sel, ship, aliens, bullets):
	"""Respond to keypresses and mouse events."""
	global pauseBtnState
	for event in pg.event.get():
		#Check for quit event
		if event.type == pg.QUIT:
			sys.exit()

		#Check for key down has been pressed
		elif event.type == pg.KEYDOWN:
			checkKeydownEvents(event, setting, screen, stats, sb, playBtn, quitBtn, sel, ship, aliens, bullets, pauseBtnState)
			#Pause menu controls
			if event.key == pg.K_UP:
				if pauseBtnState > 1:
					pauseBtnState -= 1
					sel.rect.y -= 50
			elif event.key == pg.K_DOWN:
				if pauseBtnState < 3:
					pauseBtnState += 1
					sel.rect.y += 50	

			elif event.key == pg.K_RETURN:
				if pauseBtnState == 1:
					checkPlayBtn(setting, screen, stats, sb, playBtn, sel, ship, aliens, bullets)
				elif pauseBtnState == 2:
					stats.mainGame = False
					stats.mainAbout = False
					stats.twoPlay = False
					stats.mainMenu = True
					sel.rect.centery = playBtn.rect.centery
					pauseBtnState = 1
				elif pauseBtnState == 3:
					sys.exit()	

		#Check if the key has been released
		elif event.type == pg.KEYUP:
			checkKeyupEvents(event, ship)


def checkKeydownEvents(event, setting, screen, stats, sb, playBtn, quitBtn, sel, ship, aliens, bullets, pauseBtnState):
	"""Response to kepresses"""
	global back
	if event.key == pg.K_RIGHT:
		#Move the ship right
		ship.movingRight = True
	elif event.key == pg.K_LEFT:
		#Move the ship left
		ship.movingLeft = True
	elif event.key == pg.K_SPACE:
		newBullet = Bullet(setting, screen, ship)
		bullets.add(newBullet)
		pg.mixer.music.load("music/开火.wav")
		pg.mixer.music.play()
		pg.mixer.music.set_volume(0.1)
	#Check for pause key
	elif event.key == pg.K_p:
		pause(stats)
	elif event.key == pg.K_ESCAPE:
		#Quit game
		sys.exit()

def checkKeyupEvents(event, ship):
	"""Response to keyrealeses"""
	if event.key == pg.K_RIGHT:
		ship.movingRight = False
	elif event.key == pg.K_LEFT:
		ship.movingLeft = False


def pause(stats):
	"""Pause the game when the pause button is pressed"""
	stats.gameActive = False
	stats.paused = True


def checkPlayBtn(setting, screen, stats, sb, playBtn, sel, ship, aliens, bullets):
	"""Start new game if playbutton is pressed"""
	if not stats.gameActive and not stats.paused:
		setting.initDynamicSettings()
		stats.resetStats()
		stats.gameActive = True

		#Reset the alien and the bullets
		aliens.empty()
		bullets.empty()

		#Create a new fleet and center the ship
		createFleet(setting, screen, ship, aliens)
		ship.centerShip()

		#Reset score and level
		sb.prepScore()
		sb.prepLevel()
		sb.prepHighScore()

	elif not stats.gameActive and stats.paused:
		#IF the game is not running and game is paused unpause the game
		stats.gameActive = True
		stats.paused = False



def createFleet(setting, screen, ship, aliens):
	"""Create a fleet of aliens"""
	global clock
	alien = Alien(setting, screen)
	alienWidth = alien.rect.width

	if clock % 50 == 0:
		alien.x = random.randint(0, setting.screenWidth - alienWidth)
		alien.rect.x = alien.x
		aliens.add(alien)
	clock += 1
	if clock >= setting.createalienfrequency:
		clock = 0




def shipHit(setting, stats, sb, screen, ship, aliens, bullets):
	"""Respond to ship being hit"""
	if stats.shipsLeft > 0:
		pg.mixer.music.load("music/被打中.ogg")
		pg.mixer.music.play()
		pg.mixer.music.set_volume(0.1)
		sb.prepShips()
		stats.shipsLeft -= 1
		#Empty teh list of aliens and bullets
		aliens.empty()
		bullets.empty()
		#Create a new fleet and center the ship.
		createFleet(setting, screen, ship, aliens)
		ship.centerShip()
		sb.prepShips()
		sb.prepScore()
		sleep(1.5)
	else:
		stats.gameActive = False
		checkHighScore(stats, sb)


def updateAliens(setting, stats, sb, screen, ship, aliens, bullets):
	"""Update the aliens"""
	createFleet(setting, screen, ship, aliens)
	aliens.update(setting, screen, ship, aliens)

	#look for alien-ship collision
	if pg.sprite.spritecollideany(ship, aliens):
		shipHit(setting, stats, sb, screen, ship, aliens, bullets)
		sb.prepShips()

	for alien in aliens.copy():
		if alien.rect.bottom >= setting.screenHeight:
			aliens.remove(alien)


def updateBullets(setting, screen, stats, sb, ship, aliens, bullets):
	"""update the position of the bullets"""
	#check if we are colliding
	bullets.update()
	checkBulletAlienCol(setting, screen, stats, sb, ship, aliens, bullets)
	#if bullet goes off screen delete it
	for bullet in bullets.copy(): 
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	

def checkBulletAlienCol(setting, screen, stats, sb, ship, aliens, bullets):
	"""tDetect collisions between alien and bulles"""
	collisions = pg.sprite.groupcollide(bullets, aliens, True, True)
	if collisions:
		pg.mixer.music.load("music/打中.ogg")
		pg.mixer.music.play()
		pg.mixer.music.set_volume(0.5)
		for aliens in collisions.values():
			stats.score += setting.alienPoints * len(aliens)
		checkHighScore(stats, sb)
		if stats.score % 400 >= 350:
			#Destroy exsiting bullets and create new fleet
			setting.increaseSpeed() #Speed up game
			stats.level += 1
			sb.prepLevel()

	sb.prepScore()
	# Check if there are no more aliens





def checkHighScore(stats, sb):
	"""Check to see if high score has been broken"""
	if stats.score > stats.highScore:
		stats.highScore = stats.score
		sb.prepHighScore()


def updateScreen(setting, screen, stats, sb, ship, aliens, bullets, playBtn, menuBtn, quitBtn, sel):
	"""Update images on the screen and flip to the new screen"""
	#Redraw the screen during each pass through the loop
	#Fill the screen with background color
	#Readjust the quit menu btn position
	quitBtn.rect.y = 300
	quitBtn.msgImageRect.y = 300
	menuBtn.rect.y = 250
	menuBtn.msgImageRect.y = 250
	# screen.fill(setting.bgColor)
	screen.blit(setting.bg, (0,0))

	#draw all the bullets
	for bullet in bullets.sprites():
		bullet.drawBullet()



	ship.blitme()
	aliens.draw(screen)

	#Draw the scoreboard
	sb.showScore()

	#Draw the play button if the game is inActive
	if not stats.gameActive:
		playBtn.drawBtn()
		menuBtn.drawBtn()
		quitBtn.drawBtn()
		sel.blitme()
	#Make the most recently drawn screen visable.
	pg.display.flip()

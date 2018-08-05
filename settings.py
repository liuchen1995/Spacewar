import pygame as pg

class Settings():
	"""A class to store all settings for game"""
	def __init__(self):
		"""Initialize the class"""
		self.windowCaption = 'SPACEWAR'
		self.screenWidth = 450
		self.screenHeight = 550
		self.bgColor = (61, 145, 64)
		self.bg = pg.image.load("gfx/Background.png")

		#Ships speed
		self.shipLimit = 3

		#Bullet settings
		self.bulletWidth = 3
		self.bulletHeight = 15
		self.bulletColor = (60, 60, 60)

		#Alien settings

		#How quickly the game speeds up
		self.speedUp = 1.15
		self.scoreSpeedUp = 1.5

		self.initDynamicSettings()

	def initDynamicSettings(self):
		self.shipSpeed = 1.5
		self.bulletSpeed = 3
		self.alienDropSpeed = 1
		self.alienPoints = 50
		self.createalienfrequency = 400

	def increaseSpeed(self):
		"""Increase the speed settings"""
		#self.shipSpeed *= self.speedUp
		#self.bulletSpeed *= self.speedUp
		if self.alienDropSpeed <= 2:
			self.alienDropSpeed *= self.speedUp
		# if self.createalienfrequency >=30:
		# 	self.createalienfrequency /= self.speedUp

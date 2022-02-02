#imports
import pygame, sys, random, time
from pygame.locals import *
pygame.init()

#player class
class enemies(pygame.sprite.Sprite):
	def __init__(self, texture, Map, wall, borders):
		super().__init__()
		
		#load texture
		self.texture=pygame.image.load(texture).convert_alpha()
		self.texture=pygame.transform.scale(self.texture, (int(self.texture.get_width()*0.75), int(self.texture.get_height()*0.75)))
		
		#load enemies
		self.rect=self.texture.get_rect()
		self.rect.move_ip(48*4, 48*10)
		
		#base variables
		self.life=10
		self.strength=10
		self.mana=10
		self.luck=10
		self.gold=0
		self.inventory=[["shield", True],["axe", True], ["armor", True]]
		
		self.map=Map
		self.wall=wall
		self.borders=borders
		
		#moving variables
		self.move_step=0
		self.step=48
		self.moving=False
		
		self.player_pos_x=0
		self.player_pos_y=0
		
		self.move_dir="down"
		
		#moving animation variables
		self.anim_x=0
		self.anim_y=0
		self.anim_delay=0
		
		self.move_x=0
		self.move_y=0
		self.speed=int(48/self.step)
		
		#self.map_move_dir={"up":False, "down":False, "left":False, "right":False}
		
		#absolute position varaible
		self.pos_x=5
		self.pos_y=11
		
		#relativ position variables
		self.rel_pos_x=0
		self.rel_pos_y=0
		
		#map origin
		self.map_x=0
		self.map_y=0
		
		#gui variables
		self.pause=False
		self.open_inventory=False
		
		#attack variables
		self.hit=False
	
	def move(self):
		
		#get pressed key
		pressed_key=pygame.key.get_pressed()
		border=False
		
		if self.moving!=True:
			
			if self.player_pos_y<self.pos_y:
				self.move_dir="up"
				if self.map[self.pos_y][self.pos_x] in self.borders[0]:
					border=True
				if self.map[self.pos_y-1][self.pos_x] not in self.wall[0] and border!=True:
					self.pos_y-=1
					self.rel_pos_y-=1
					self.move_y=-self.speed
					self.moving=True
					
			if self.player_pos_y>self.pos_y:
				self.move_dir="down"
				if self.map[self.pos_y][self.pos_x] in self.borders[1]:
					self.border=True
				if self.map[self.pos_y+1][self.pos_x] not in self.wall[1] and border!=True:
					self.pos_y+=1
					self.rel_pos_y+=1
					self.move_y=self.speed
					self.moving=True
				
			if self.player_pos_x<self.pos_x:
				self.move_dir="left"
				if self.map[self.pos_y][self.pos_x] in self.borders[2]:
					border=True
				if self.map[self.pos_y][self.pos_x-1] not in self.wall[2] and border!=True:
					self.pos_x-=1
					self.rel_pos_x-=1
					self.move_x=-self.speed
					self.moving=True
					
			if self.player_pos_x>self.pos_x:
				self.move_dir="right"
				
				#if self.pos_x==player_pos_x:
				#	self.touch["right"]=True
				
				if self.map[self.pos_y][self.pos_x] in self.borders[3]:
					border=True
				if self.map[self.pos_y][self.pos_x+1] not in self.wall[3] and border!=True:# and self.touch["right"]==True:
					self.pos_x+=1
					self.rel_pos_x+=1
					self.move_x=self.speed
					self.moving=True
			
		else:
			
			self.rect.move_ip(self.move_x, self.move_y)
				
			self.move_step+=1
			if self.move_step==self.step:
				
				self.moving=False
				self.move_step=0
				self.move_x=0
				self.move_y=0
		
		if self.map_move_dir["up"]==True:
			self.rect.move_ip(0, 2)
		if self.map_move_dir["down"]==True:
			self.rect.move_ip(0, -2)
				
		if self.map_move_dir["left"]==True:
			self.rect.move_ip(2, 0)
		if self.map_move_dir["right"]==True:
			self.rect.move_ip(-2, 0)
				
	def anim(self):
		self.anim_delay+=1
		del_lim=10
		lim=4
		
		if self.move_dir=="up":
			self.anim_y=8
		if self.move_dir=="down":
			self.anim_y=10
		
		if self.move_dir=="left":
			self.anim_y=9
		if self.move_dir=="right":
			self.anim_y=11
			
		if self.moving!=True:
			self.anim_y+=4
			del_lim=30
			lim=1
		
		if self.anim_delay>del_lim:
			self.anim_delay=0
			self.anim_x+=1
		if self.anim_x>lim:
			self.anim_x=0
	
	def attack(self):
		self.hit=False
		if self.pos_x==self.player_pos_x and self.pos_y==self.player_pos_y:
			return True
	
	def get_player_pos(self, pos_x, pos_y, map_move_dir):
		self.player_pos_x=pos_x
		self.player_pos_y=pos_y
		self.map_move_dir=map_move_dir
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		

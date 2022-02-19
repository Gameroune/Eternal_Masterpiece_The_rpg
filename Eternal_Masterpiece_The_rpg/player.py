#imports
import pygame, sys, random, time
from pygame.locals import *
pygame.init()

#player class
class player(pygame.sprite.Sprite):
	def __init__(self, texture, Map, wall, borders):
		super().__init__()
		
		#load texture
		self.texture=pygame.image.load(texture).convert_alpha()
		self.texture=pygame.transform.scale(self.texture, (int(self.texture.get_width()*0.75), int(self.texture.get_height()*0.75)))
		
		#load player
		self.rect=self.texture.get_rect()
		self.rect.move_ip(48*3, 48*3)
		
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
		self.step=24
		self.moving=False
		
		
		self.move_dir="down"
		
		#moving animation variables
		self.anim_x=0
		self.anim_y=0
		self.anim_delay=0
		
		self.move_x=0
		self.move_y=0
		self.speed=int(48/self.step)
		
		#absolute position varaible
		self.pos_x=4
		self.pos_y=4
		
		#relativ position variables
		self.rel_pos_x=4
		self.rel_pos_y=4
		
		#map origin
		self.map_x=0
		self.map_y=0
		
		self.map_move_dir={"up":False, "down":False, "left":False, "right":False}
		
		#gui variables
		self.pause=False
		self.open_inventory=False
		
		#attack variables
		self.hited=False
		self.hit_delay=0
	
	def update(self):
		self.move()
		self.anim()
		
		if self.hited!=True:
			self.hit_delay=0
		
		if self.hit_delay>=60 and self.hited==True:
			self.hited=False
			self.hit_delay=0
			
		self.hit_delay+=1
	
	def move(self):
	
		#get pressed key
		pressed_key=pygame.key.get_pressed()
		border=False
		
		if self.moving!=True:
		
			self.map_move_dir={"up":False, "down":False, "left":False, "right":False}
		
			if pressed_key[K_UP]:
				self.move_dir="up"
				if self.map[self.pos_y][self.pos_x] in self.borders[0]:
					border=True
				if self.map[self.pos_y-1][self.pos_x] not in self.wall[0] and border!=True:
					self.pos_y-=1
					self.rel_pos_y-=1
					self.move_y=-self.speed
					self.moving=True
					
			if pressed_key[K_DOWN]:
				self.move_dir="down"
				if self.map[self.pos_y][self.pos_x] in self.borders[1]:
					self.border=True
				if self.map[self.pos_y+1][self.pos_x] not in self.wall[1] and border!=True:
					self.pos_y+=1
					self.rel_pos_y+=1
					self.move_y=self.speed
					self.moving=True
				
			if pressed_key[K_LEFT]:
				self.move_dir="left"
				if self.map[self.pos_y][self.pos_x] in self.borders[2]:
					border=True
				if self.map[self.pos_y][self.pos_x-1] not in self.wall[2] and border!=True:
					self.pos_x-=1
					self.rel_pos_x-=1
					self.move_x=-self.speed
					self.moving=True
					
			if pressed_key[K_RIGHT]:
				self.move_dir="right"
				if self.map[self.pos_y][self.pos_x] in self.borders[3]:
					border=True
				if self.map[self.pos_y][self.pos_x+1] not in self.wall[3] and border!=True:
					self.pos_x+=1
					self.rel_pos_x+=1
					self.move_x=self.speed
					self.moving=True
				
			
		else:
			if self.rel_pos_x<7 and self.rel_pos_x>3:
				self.rect.move_ip(self.move_x, 0)
			if self.rel_pos_y<7 and self.rel_pos_y>3:
				self.rect.move_ip(0, self.move_y)

			if self.rel_pos_x>=7:
				self.map_x-=self.speed
				self.map_move_dir["right"]=True
			if self.rel_pos_x<=3:
				self.map_x+=self.speed
				self.map_move_dir["left"]=True
			
			if self.rel_pos_y>=7:
				self.map_y-=self.speed
				self.map_move_dir["down"]=True
			if self.rel_pos_y<=3:
				self.map_y+=self.speed
				self.map_move_dir["up"]=True

			self.move_step+=1
			if self.move_step==self.step:
				if self.rel_pos_x>=7:
					self.rel_pos_x-=1
				if self.rel_pos_y>=7 :
					self.rel_pos_y-=1
				if self.rel_pos_x<=3:
					self.rel_pos_x+=1
				if self.rel_pos_y<=3:
					self.rel_pos_y+=1
					
				self.moving=False
				self.move_step=0
				self.move_x=0
				self.move_y=0
				
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
	
	def gui(self):
	
		pressed_key=pygame.key.get_pressed()

		if pressed_key[K_e]:
			if self.open_inventory==False:
				self.open_inventory=True
				self.pause=True
			else:
				self.open_inventory=False
				self.pause=False
		
		if pressed_key[K_SPACE]:
			if self.pause==False:
				self.pause=True
			else:
				self.pause=False
	
	def get_damage(self, enemies_strength):
		damage=int(enemies_strength/10)
		#if self.hited!=True:
		self.life-=damage
		self.hited=True
		if self.life<=0:
			print("Game over")
			pygame.quit()
			sys.exit()
		
		
	
	def attack(self, enemie_pos_x, enemie_pos_y):
		pressed_key=pygame.key.get_pressed()
		if pressed_key[K_p]:
			if self.pos_x<=enemie_pos_x+1 and self.pos_x>=enemie_pos_x-1 and self.pos_y<=enemie_pos_y+1 and self.pos_y>=enemie_pos_y-1:
				return True
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		

#import
import pygame, sys, random, time
import player, enemies
exec(open('textures/item/item_pos.py').read())

from pygame.locals import *

#initializing
pygame.init()

screen_width=15
screen_lenght=10

#setting up screen
displaySurf=pygame.display.set_mode((screen_width*48, screen_lenght*48))
pygame.display.set_caption("Eternal Masterpiece: the RPG   ver: indev/pre-beta")

#setting up FPS
FPS=pygame.time.Clock()
fps=60

size=48

#setting up textures
tileset=pygame.image.load("textures/tileset/tileset.png").convert_alpha()
tileset=pygame.transform.scale(tileset, (int(tileset.get_width()*1.5), int(tileset.get_height()*1.5)))

gui=pygame.image.load("textures/gui/gui.png").convert_alpha()
gui=pygame.transform.scale(gui, (int(gui.get_width()*3), int(gui.get_height()*3)))

item=pygame.image.load("textures/item/items1.png").convert_alpha()
item=pygame.transform.scale(item, (int(item.get_width()*1.5), int(item.get_height()*1.5)))


life=pygame.image.load("textures/player/life.png").convert_alpha()
mana=pygame.image.load("textures/player/mana.png").convert_alpha()

#tmp/test variables
hited=False
hit_delay=0

#setting up map
Map=[]
with open("maps/map_1.txt", 'r') as file:
	Map_0=file.read().split("\n")

for i in range(len(Map_0)):
	Map.append(Map_0[i].replace(' ', '').split(','))
	
Map.pop(-1)

#setting up object map
obj=[[-1],
	 [-1],
	 [-1],
	 [-1],
	 [-1, -1, -1,117]] 

#defining walls
borders=[[' '],[' '],['48', '43'],['50','42']]
u_wall=['-1','58','56','74','72','73','46','57']
d_wall=['-1','58','56','74','72','73','46','57']
l_wall=['-1','58','56','74','72','73','46','57','50','42']
r_wall=['-1','58','56','74','72','73','46','57','48','40','43']

wall=[u_wall, d_wall, l_wall, r_wall]

#creating player
player=player.player("textures/player/player_texture.png", Map, wall, borders)

enemies=enemies.enemies("textures/enemies/orc_1.png", Map, wall, borders)

#Map generation function
def map_gen(Map, tileset, size, img_length, x_dep, y_dep):
	i=0
	j=0
	
	x=-size+x_dep
	y=-size+y_dep
	
	while i<len(Map):
		while j<len(Map[i]):
			a=int(Map[i][j])%img_length
			b=int(Map[i][j])//img_length
			tile=pygame.Rect(a*size, b*size, size, size)
			displaySurf.blit(tileset, (x, y), tile)
			x+=size
			j+=1
		x=-size+x_dep
		y+=size
		j=0
		i+=1

#main loop
while True:

	#quit function
	for event in pygame.event.get():
		if event.type==QUIT:
			pygame.quit()
			sys.exit()
	
	#update gui variables
	player.gui()
	
	if player.pause!=True:
		
		#reset screen
		displaySurf.fill(pygame.Color('#000000'))
		#draw map
		map_gen(Map, tileset, size, 8, player.map_x, player.map_y)
		map_gen(obj, tileset, size, 8, player.map_x, player.map_y)
		
		#player functions
		player.move()
		player.anim()
		
		#enemies_function
		enemies.get_player_pos(player.pos_x, player.pos_y, player.map_move_dir)
		enemies.move()
		enemies.anim()
		
		#draw player
		displaySurf.blit(player.texture, player.rect, pygame.Rect(player.anim_x*size, player.anim_y*size, size, size))
		
		displaySurf.blit(enemies.texture, enemies.rect, pygame.Rect(enemies.anim_x*size, enemies.anim_y*size, size, size))
		
		if enemies.attack() and hited!=True:
			player.get_damage(int(enemies.strength/10))
			hited=True
		
		if hit_delay>=60:
			hited=False
			hit_delay=0
			
		hit_delay+=1
		
		#draw lif/mana
		for i in range(player.life):
			displaySurf.blit(life, (i*32, (screen_lenght-1)*48))
		for i in range(player.mana):
			displaySurf.blit(mana, (i*32, (screen_lenght-2)*48))
	
	#inventory function
	if player.open_inventory==True:
		a=0
		#draw inventory background
		displaySurf.blit(gui, (2*size, 2*size), pygame.Rect(5*96, 0*96, 5*96, 3*96))
		
		#draw inventory cases
		for i in range(5):
			for j in range(3):
				displaySurf.blit(gui,(int(2*size+((i+2.5)*48)), int(2*size+((j+1.5)*48))), pygame.Rect(1*48, 0*48, 1*48, 1*48))
				
				#draw inventory contents
				if a<len(player.inventory):
					displaySurf.blit(item,(int(2*size+((i+2.5)*48)), int(2*size+((j+1.5)*48))), pygame.Rect(item_pos[player.inventory[a][0]][0]*48, item_pos[player.inventory[a][0]][1]*48, 1*48, 1*48))
				a+=1
			a+=1
	
	#update screen
	pygame.display.update()
	FPS.tick(fps)

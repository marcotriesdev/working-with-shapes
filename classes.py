from raylibpy import *
from enum import Enum
import asyncio

terrainSize = {
    "small" : Vector2(50,50),
    "medium": Vector2(100,100),
    "big"   : Vector2(150,150)
}

#LITERALES PARA QUE LOS ARRAYS DE MAPAS NO SE DISTORSIONEN MUCHO
c = "c"
x = "x"


testscenarios = {
    "test0" :  [[1,0,2,0,3,0,1],
                [0,0,0,0,0,0,0]],

    "test1" : [[1,0,1,1,1,1,1],
               [1,0,0,0,0,0,1],
               [1,0,0,0,0,0,1],
               [1,0,0,0,0,0,1],
               [1,0,0,0,0,0,1],
               [1,1,1,1,0,1,1]],

    "test2" : [[2,1,0,1,0,1,2],
               [1,0,0,0,0,0,1],
               [1,0,0,0,0,0,1],
               [1,0,0,2,0,0,1],
               [1,0,0,0,0,0,1],
               [2,1,0,1,0,1,2]],

    "test3" : [[2,1,0,0,0,1,2],
               [1,0,0,0,0,0,1],
               [1,0,0,0,0,0,1],
               [0,0,0,3,0,0,0],
               [1,0,0,0,0,0,1],
               [2,1,0,0,0,1,2]],

    "test4" : [[2,1,0,0,0,1,2,1,1,1,1,1],
               [1,0,x,0,0,0,x,0,0,c,0,1],
               [1,0,x,0,0,0,0,0,c,0,0,1],
               [0,0,0,3,0,c,0,0,0,0,c,0],
               [1,x,0,0,0,0,1,0,0,c,0,2],
               [2,1,0,0,x,1,2,0,0,0,0,3]],

}


class Estado_global(Enum):

    intro = 1
    main_game = 2
    pause = 3
    dead = 4


class Estado(Enum):

    idle = 1 
    chasing = 2
    attack = 3
    flee = 4


class TerrainGenerator:

    def __init__(self):

        pass

    def generate_terrain(self,array: list, xstart: int, ystart:int, group_terrain,group_items,group_enemy):
        marginy = 0
        for line in array:
        
            marginx = 0

            for number in line:
                    
                match number:

                    case 1 :
                        newblock = TerrainBlock(Vector2(xstart+marginx,ystart+marginy),"small")
                        marginx += terrainSize["small"].x
                        
                    case 2 :
                        newblock = TerrainBlock(Vector2(xstart+marginx,ystart+marginy),"medium")
                        marginx += terrainSize["medium"].x

                    case 3 :
                        newblock = TerrainBlock(Vector2(xstart+marginx,ystart+marginy),"big")
                        marginx += terrainSize["big"].x

                    case "c":
                        newitem = Coin(Vector2(xstart+marginx,ystart+marginy),15,GREEN,1)
                        group_items.add(newitem)

                    case "x":
                        newenemy = Enemy(Vector2(xstart+marginx,ystart+marginy),20,BLACK,10,2,2)
                        group_enemy.add(newenemy)

                    case 0 :
                        marginx += terrainSize["big"].x


                    
                if newblock:
                    group_terrain.add(newblock)

            marginy += terrainSize["big"].y
                    




class SimpleStateMachine:

    def __init__(self, init_state,WINDOW_WIDTH,WINDOW_HEIGHT,gametitle):
        self.init_state = init_state
        self.current_state = self.init_state
        self.dimensions = Vector2(WINDOW_WIDTH,WINDOW_HEIGHT)
        self.gametitle = gametitle
        

    def update(self):

        while not window_should_close():

            match self.current_state:

                case Estado_global.intro:
                    print(self.current_state)
                    self.current_state = intro_loop(self.dimensions.x,self.dimensions.y,self.gametitle,self.current_state)

                case Estado_global.main_game:

                    print(self.current_state)
                    print("EMPEZAMOS juego MALDITOS")
                    self.current_state = game_loop(self.dimensions.x, self.dimensions.y,self.gametitle,self.current_state)
                #case Estado_global.pause
                case Estado_global.dead:
                    print(self.current_state)
                    self.current_state = dead_loop(self.dimensions.x, self.dimensions.y,self.gametitle,self.current_state)

class TerrainBlock:

    def __init__(self,position,size,color = BROWN):

        self.location = position
        self.smallRock = Rectangle(position.x,position.y,terrainSize["small"].x,terrainSize["small"].y)
        self.mediumRock = Rectangle(position.x,position.y,terrainSize["medium"].x,terrainSize["medium"].y)
        self.bigRock = Rectangle(position.x,position.y,terrainSize["big"].x,terrainSize["big"].y)

        self.size = size
        self.drawsize = None
        self.color = color
        self.type = "rock"
        self.sizeMatch()

    def sizeMatch(self):

        match self.size:
            case "small":
                self.drawsize = self.smallRock
                self.color = DARKGRAY
            case "medium":
                self.drawsize = self.mediumRock
                self.color = BROWN
            case "big":
                self.drawsize = self.bigRock
                self.color = BLACK

    def draw(self):

        draw_rectangle_rec(self.drawsize,self.color)
        
class Circle:

    def __init__(self,location,radius,color,hp,movespeed = 1):

        self.location = location
        self.radius = radius 
        self.color = color
        self.hp = hp
        self.score = 0
        self.velocity = Vector2(0,0)
        self.movespeed = movespeed
        self.hurt = False
        self.movebuffer = 0
        self.type = "player"
        self.collisions_list = []
        self.erase = False

        self.direction = 0
        self.value = 1    



    def draw(self):

        if self.hurt:
            draw_circle_v(self.location,self.radius,RED)
        else:    
            draw_circle_v(self.location,self.radius,self.color)

       
    def collision_coins(self,group):

        for e in group.elements:


            if check_collision_circles(self.location,self.radius,e.location,e.radius) and e.type == "coin" :
                
                newfadingcoin = FadingCoin(e.location,e.radius,e.color,e.hp)
                group.remove_element(e)
                group.add(newfadingcoin)
                self.score += 1
                
               


    def collision_enemy(self,group):

        self.collisions_list.clear()

        for e in group.elements:

            if check_collision_circles(self.location,self.radius,e.location,e.radius):

                self.collisions_list.append(e)
                
        if  self.collisions_list:

            if self.hurt == False:

                self.hurt = True
                self.hp -= e.enemylevel
                    
                
                

        if not self.collisions_list:       
            self.hurt = False
        



    def terraincollision(self,group):

        for e in group.elements:

            if e.type == "rock" and check_collision_circle_rec(self.location, self.radius, e.drawsize):

                self.location -= self.input(self.velocity)
                            


    def input(self,velocity):

        velocity = Vector2(0,0)



        if is_key_down(KEY_A):
            velocity.x -= self.movespeed
        if is_key_down(KEY_D):
            velocity.x += self.movespeed
        if is_key_down(KEY_W):
            velocity.y -= self.movespeed
        if is_key_down(KEY_S):
            velocity.y += self.movespeed

        return velocity


    def screenlimits(self,dimensions):

        if self.location.x < 0:
            self.location.x = 0
        if self.location.x > dimensions.x:
            self.location.x = dimensions.x
            
        if self.location.y < 0:
            self.location.y = 0
        if self.location.y > dimensions.y:
            self.location.y = dimensions.y
                       

    def update(self,dimensions):

        self.screenlimits(dimensions)

        self.location += self.input(self.velocity)

class Enemy(Circle):

    def __init__(self,location,radius,color,hp, enemylevel, movespeed = 1):
        super().__init__(location,radius,color,hp,movespeed = 1)

        self.color = BLACK
        self.enemylevel = enemylevel
        self.type = "enemy"


    def enemyAI(self):

        movement_range1, movement_range2 = 5, 100

        if self.movebuffer == 0:

            self.direction = get_random_value(0,1)
            self.value = get_random_value(-1,1)
            self.movebuffer = get_random_value(movement_range1,movement_range2)

    
        if self.direction == 0:

            self.location.x += self.movespeed * self.value
            self.movebuffer -= 1
            

        elif self.direction == 1:
            self.location.y -= self.movespeed * self.value
            self.movebuffer -=1

    def update(self,dimensions):
        
        self.screenlimits(dimensions)
        self.enemyAI()

    def draw(self):

        draw_circle_v(self.location,self.radius,self.color)

class Coin(Circle):

    def __init__(self,*args):
        super().__init__(*args)

        self.color = GREEN
        self.thickness = 10
        self.type = "coin"
        

    def coinWobble(self):

        movement_range1, movement_range2 = 1,3

        if self.movebuffer == 0:
            self.movebuffer = get_random_value(movement_range1,movement_range2)
            self.value = -self.value

        self.location.y += self.movespeed * self.value
        self.movebuffer -= 1


    def update(self, dimensions):

        self.screenlimits(dimensions)
        self.coinWobble()


    def draw(self):

        for i in range(self.thickness):
            draw_circle_lines_v(self.location, self.radius+i, self.color)

class FadingCoin(Coin):

    def __init__(self,*args):

        super().__init__(*args)
        self.type = "fading_coin"
        self.color = Color(0,228,48,255)        

    def coin_fade(self):
 
        print(self.radius)
        if self.radius < 30:
            self.radius += 5
            self.color.a -= 10
        else:
            self.erase = True


    def update(self,dimensions):

        self.coin_fade()
 

class Group:

    def __init__(self,elements):

        self.elements = elements

    def add(self,new_element):

        self.elements.append(new_element) 

    def remove_element(self,element):

        self.elements.remove(element)

    def update(self,dimensions):

        for element in self.elements:
            element.update(dimensions)
            if element.erase:
                self.elements.remove(element)

    def draw(self):

        for element in self.elements:
            element.draw()
            if hasattr(element,"erase"):
                draw_text(str(element.type),element.location.x+20,element.location.y+20,20,WHITE)
            

class Gui:

    def __init__(self, window_width, window_height,title,player = None):
        
        self.window_width = window_width
        self.window_height = window_height
        self.title = title
        self.titlepositionx = (window_width/2)-(25*(len(self.title)/2))
        self.player = player

        self.debug_state = False

        pass

    
    def draw_hud(self):

        #DRAW GAME TITLE
        draw_text(self.title, self.titlepositionx, 5, 40, BLACK)

        #DRAW SCORE
        draw_text(f"SCORE: {self.player.score}",50,50,40,BLACK)

        #DRAW HP
        draw_text(f"HP: {self.player.hp}", 50,120,40,BLACK)

    def draw_intro(self):

        draw_text(self.title, self.titlepositionx,self.window_height/2,30,BLACK)
        draw_text("//presiona ENTER//", self.titlepositionx+20,(self.window_height/2)+50,30,RED)

    def draw_dead(self):

        draw_text("//TE MORISTE JAJAJAJAJA//", self.titlepositionx+20,(self.window_height/2)+50,30,RED)
        draw_text("PRESIONA ENTER PARA REVIVIR", self.titlepositionx+20,(self.window_height/2)+80,30,GREEN)


    def draw_pause(self):

        draw_rectangle(0,(self.window_height/2)+20,self.window_width,50,GRAY)
        draw_text("PAUSA", self.titlepositionx+100,(self.window_height/2)+10,80,RED)
        draw_text("Presiona P para continuar", self.titlepositionx+150,(self.window_height/2)+100,30,RED)


    def draw_debug(self,player,activate):

        self.debug_state = activate

        if activate:
            draw_text(f"hurted player? {player.hurt}",self.window_width/2,50,20,RED)
            draw_text(f"colision list {player.collisions_list}",2,100,20,RED)

def intro_loop(WINDOW_WIDTH,WINDOW_HEIGHT,gametitle,current_state):

    introGUI = Gui(WINDOW_WIDTH,WINDOW_HEIGHT,gametitle)

    while not window_should_close():

        begin_drawing()

        clear_background(WHITE)

        introGUI.draw_intro()

        if is_key_pressed(KEY_ENTER):

            current_state = Estado_global.main_game
            print(f"orale me voy a {current_state}")
            return current_state

        end_drawing()
    
    close_window()


def game_loop(WINDOW_WIDTH,WINDOW_HEIGHT,game_title,current_state):

    dimensions = Vector2(WINDOW_WIDTH,WINDOW_HEIGHT)
                    
    player1 = Circle(Vector2(500,500),10,SKYBLUE,10,5)
    gamegui = Gui(WINDOW_WIDTH,WINDOW_HEIGHT, game_title,player1)


    player_group = Group([player1])
    coins_group = Group([])
    enemy_group = Group([])
    terrain_group = Group([])

    terraingen = TerrainGenerator()
    terraingen.generate_terrain(testscenarios["test4"],5,5,terrain_group,coins_group,enemy_group)

    paused = False


    while not window_should_close():

        if is_key_pressed(KEY_P):
            paused = not paused

        if not paused:
            begin_drawing()

            clear_background(LIGHTGRAY)

            player_group.update(dimensions)

            if player1.hp <= 0:
                current_state = Estado_global.dead
                print(f"orale me voy a {current_state}")
                return current_state

            enemy_group.update(dimensions)
            coins_group.update(dimensions)

            player1.collision_coins(coins_group)
            player1.collision_enemy(enemy_group)
            player1.terraincollision(terrain_group)

            terrain_group.draw()
            player_group.draw()
            coins_group.draw()
            enemy_group.draw()
            
            gamegui.draw_hud()
            gamegui.draw_debug(player1,False)

            end_drawing()
        
        else:
            begin_drawing()
            gamegui.draw_pause()
            end_drawing()

    close_window()
    

def dead_loop(WINDOW_WIDTH,WINDOW_HEIGHT,gametitle,current_state):

    deadGUI = Gui(WINDOW_WIDTH,WINDOW_HEIGHT,gametitle)

    while not window_should_close():

        begin_drawing()
        clear_background(WHITE)
        deadGUI.draw_dead()

        if is_key_pressed(KEY_ENTER):

            current_state = Estado_global.main_game
            print(f"orale me voy a {current_state}")
            return current_state

        end_drawing()
    
    close_window()

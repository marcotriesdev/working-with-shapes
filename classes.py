from raylibpy import *
from enum import Enum

terrainSize = {
    "small" : (100,100),
    "medium": (150,150),
    "big"   : (300,300)
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

class SimpleStateMachine:

    def __init__(self, init_state,WINDOW_WIDTH,WINDOW_HEIGHT,gametitle):
        self.init_state = init_state
        self.current_state = self.init_state
        self.dimensions = Vector2(WINDOW_WIDTH,WINDOW_HEIGHT)
        self.gametitle = gametitle
        

    def update(self):

        while not window_should_close():
            print("xulo")

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

    def __init__(self,position,size,color):

        self.location = position
        self.smallRock = Rectangle(position.x,position.y,terrainSize["small"][0],terrainSize["small"][1])
        self.mediumRock = Rectangle(position.x,position.y,terrainSize["medium"][0],terrainSize["medium"][1])
        self.bigRock = Rectangle(position.x,position.y,terrainSize["big"][0],terrainSize["big"][1])

        self.size = size
        self.drawsize = None
        self.color = color
        self.type = "rock"
        self.sizeMatch()

    def sizeMatch(self):

        match self.size:
            case "small":
                self.drawsize = self.smallRock
            case "medium":
                self.drawsize = self.mediumRock
            case "big":
                self.drawsize = self.bigRock

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

        self.direction = 0
        self.value = 1    


    def draw(self):

        draw_circle_v(self.location,self.radius,self.color)
       

    def collision(self,group):

        for e in group.elements:

            if check_collision_circles(self.location,self.radius,e.location,e.radius):

                match e.type:

                    case "coin":
                        self.score += 1
                        group.elements.remove(e)

                    case "enemy":
                        if not self.hurt:
                            self.hurt = True
                            self.hp -= e.enemylevel
            
            elif not check_collision_circles(self.location,self.radius,e.location,e.radius) and e.type == "enemy":
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

    def __init__(self,*args):
        super().__init__(*args)

        self.color = BLACK
        self.enemylevel = 1
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

        movement_range1, movement_range2 = 2,6

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

class Group:

    def __init__(self,elements):

        self.elements = elements

    def add(self,new_element):

        self.elements.append(new_element) 

    def update(self,dimensions):

        for element in self.elements:
            element.update(dimensions)

    def draw(self):

        for element in self.elements:
            element.draw()

class Gui:

    def __init__(self, window_width, window_height,title,player = None):
        
        self.window_width = window_width
        self.window_height = window_height
        self.title = title
        self.titlepositionx = (window_width/2)-(25*(len(self.title)/2))
        self.player = player

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


    def draw_debug(self,player):

        draw_text(f"hurted player? {player.hurt}",self.window_width/2,50,20,RED)

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
                    
    circle1 = Circle(Vector2(500,500),10,PINK,10,5)
    gamegui = Gui(WINDOW_WIDTH,WINDOW_HEIGHT, game_title,circle1)

    circle2 = Coin(Vector2(400,400),15,GREEN,1)
    circle3 = Coin(Vector2(460,400),15,GREEN,1)
    circle4 = Coin(Vector2(520,400),15,GREEN,1)

    enemy1 = Enemy(Vector2(800,800),20,BLACK,10,2)
    enemy2 = Enemy(Vector2(600,360),20,BLACK,10,2)

    rock1 = TerrainBlock(Vector2(100,100),"small",BROWN)

    player_group = Group([circle1])
    circle_group = Group([circle2,circle3,circle4])
    enemy_group = Group([enemy1])
    terrain_group = Group([rock1])

    paused = False


    while not window_should_close():

        if is_key_pressed(KEY_P):
            paused = not paused

        if not paused:
            begin_drawing()

            clear_background(WHITE)

            player_group.update(dimensions)

            if circle1.hp <= 0:
                current_state = Estado_global.dead
                print(f"orale me voy a {current_state}")
                return current_state

            enemy_group.update(dimensions)
            circle_group.update(dimensions)

            circle1.collision(circle_group)
            circle1.collision(enemy_group)
            circle1.terraincollision(terrain_group)

            terrain_group.draw()
            player_group.draw()
            circle_group.draw()
            enemy_group.draw()
            
            gamegui.draw_hud()
            gamegui.draw_debug(circle1)

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

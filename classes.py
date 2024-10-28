from raylibpy import *
from enum import Enum

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




        close_window()

class Circle:

    def __init__(self,location,radius,color,type,hp,movespeed = 1,enemylevel = 0):

        self.location = location
        self.radius = radius
        self.color = color
        self.type = type
        self.hp = hp
        self.score = 0
        self.velocity = Vector2(0,0)
        self.movespeed = movespeed
        self.hurt = False
        self.thickness = 1
        self.movebuffer = 0
        self.enemylevel = enemylevel
 

        self.direction = 0
        self.value = 1    


    def draw(self):

        match self.type:

            case "fill":
                draw_circle_v(self.location,self.radius,self.color)
            case "outline":
                for i in range(self.thickness):
                    draw_circle_lines_v(self.location, self.radius+i, self.color)
            case "enemy":
                draw_circle_v(self.location,self.radius,self.color)

    def collision(self,group):

        for e in group.elements:

            if check_collision_circles(self.location,self.radius,e.location,e.radius):
                match e.type:
                    case "outline":
                        self.score += 1
                        group.elements.remove(e)

                    case "enemy":
                        if not self.hurt:
                            self.hurt = True
                            self.hp -= e.enemylevel
            
            elif not check_collision_circles(self.location,self.radius,e.location,e.radius) and e.type == "enemy":
                self.hurt = False


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


    def coinWobble(self):
        movement_range1, movement_range2 = 2,6

        if self.movebuffer == 0:
            self.movebuffer = get_random_value(movement_range1,movement_range2)
            self.value = -self.value

        self.location.y += self.movespeed * self.value
        self.movebuffer -= 1

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

        if self.type == "enemy":
            self.enemyAI()

        elif self.type == "fill":
            self.location += self.input(self.velocity)

        elif self.type == "outline":
            self.coinWobble()




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

    def set_group_thickness(self,thic):

        for element in self.elements:
            element.thickness = thic




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
        draw_text("//press ENTER//", self.titlepositionx+20,(self.window_height/2)+50,30,RED)

    def draw_dead(self):
        draw_text("//TE MORISTE JAJAJAJAJA//", self.titlepositionx+20,(self.window_height/2)+50,30,RED)
        draw_text("PRESIONA ENTER PARA REVIVIR", self.titlepositionx+20,(self.window_height/2)+80,30,GREEN)


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
                    
    circle1 = Circle(Vector2(500,500),10,PINK,"fill",10,5)
    gamegui = Gui(WINDOW_WIDTH,WINDOW_HEIGHT, game_title,circle1)

    circle2 = Circle(Vector2(400,400),15,GREEN,"outline",1)
    circle3 = Circle(Vector2(460,400),15,GREEN,"outline",1)
    circle4 = Circle(Vector2(520,400),15,GREEN,"outline",1)

    enemy1 = Circle(Vector2(800,800),20,BLACK,"enemy",10,4,2)

    player_group = Group([circle1])
    circle_group = Group([circle2,circle3,circle4])
    circle_group.set_group_thickness(10)

    enemy_group = Group([enemy1])


    while not window_should_close():

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

        player_group.draw()
        circle_group.draw()
        enemy_group.draw()
        gamegui.draw_hud()

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

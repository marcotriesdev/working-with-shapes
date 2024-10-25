from raylibpy import *

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

    def __init__(self, window_width, window_height,title,player):
        
        self.window_width = window_width
        self.window_height = window_height
        self.title = title
        self.titleposition = (window_width/2)-(25*(len(self.title)/2))
        self.player = player

        pass

    
    def draw_hud(self):

        #DRAW GAME TITLE
        draw_text(self.title, self.titleposition, 5, 40, BLACK)

        #DRAW SCORE
        draw_text(f"SCORE: {self.player.score}",50,50,40,BLACK)

        #DRAW HP
        draw_text(f"HP: {self.player.hp}", 50,120,40,BLACK)

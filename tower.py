import pygame
import os
import math

TOWER_IMAGE = pygame.image.load(os.path.join("images", "rapid_test.png"))


class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
        self.transparency = 60 # set the transparency that display on attack range of towers
        
    def collide(self, enemy):
        """
        Q2.2)check whether the enemy is in the circle (attack range), if the enemy is in range return True
        :param enemy: Enemy() object
        :return: Bool
        """

        """
        Hint:
        x1, y1 = enemy.get_pos()
        ...
        """
        # get the distance between enemy and tower
        x1, y1 = enemy.get_pos()
        x2, y2 = self.center
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        # return whether is in range
        if distance < self.radius:
            return True
        else:
            return False

    def draw_transparent(self, win):
        """
        Q1) draw the tower effect range, which is a transparent circle.
        :param win: window surface
        :return: None
        """
        # create a transparent surface ; transparent_surface = pygame.Surface((width , height), pygame.SRCALPHA)       
        transparent_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        # draw a circle on the transparent surface ; pygame.draw.circle(surface, (COLOR), (center(x, y)), radius)
        pygame.draw.circle(transparent_surface, (255, 255, 255, self.transparency), (self.radius, self.radius), self.radius)
        # display on the window ; win.blit(surface, start point(x , y))
        win.blit(transparent_surface, (self.center[0]-self.radius , self.center[1]-self.radius))

class Tower:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(TOWER_IMAGE, (70, 70))  # image of the tower
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # center of the tower
        self.range = 150  # tower attack range
        self.damage = 2   # tower damage
        self.range_circle = Circle(self.rect.center, self.range)  # attack range circle (class Circle())
        self.cd_count = 0  # used in self.is_cool_down()
        self.cd_max_count = 60  # used in self.is_cool_down()
        self.is_selected = False  # the state of whether the tower is selected, default is not selected
        self.type = "tower"
        

    def is_cool_down(self):
        """
        Q2.1) Return whether the tower is cooling down
        (1) Use a counter to computer whether the tower is cooling down (( self.cd_count
        :return: Bool
        """

        """
        Hint:
        let counter be 0
        if the counter < max counter then
            set counter to counter + 1
        else 
            counter return to zero
        end if
        """
        # counting cool down, default is cooling
        if self.cd_count < self.cd_max_count : 
            self.cd_count += 1
            return False
        return True
        

    def attack(self, enemy_group):
        """
        Q2.3) Attack the enemy.
        (1) check the the tower is cool down ((self.is_cool_down()
        (2) if the enemy is in attack range, then enemy get hurt. ((Circle.collide(), enemy.get_hurt()
        :param enemy_group: EnemyGroup()
        :return: None
        """
        cd = self.is_cool_down()
        
        # attack enemies in list sequentially
        for atk_list in enemy_group.expedition:
            if cd and self.range_circle.collide(atk_list):
                atk_list.get_hurt(self.damage)
                # cooling down after attacking, set cd count = 0
                self.cd_count = 0
                return 0 # break for loop
            

    def is_clicked(self, x, y):
        """
        Bonus) Return whether the tower is clicked 
        (1) If the mouse position is on the tower image, return True
        :param x: mouse pos x
        :param y: mouse pos y
        :return: Bool
        """
        # whether the mouse is clicked on the range of rectangle ; point [(x1, y1), (x1, y2), (x2, y1), (x2, y2)]
        if (x, y) >= (self.rect.x, self.rect.y) and (x, y) <= self.rect.bottomright:
            return True
        else:
            return False        

    def get_selected(self, is_selected):
        """
        Bonus) Change the attribute self.is_selected
        :param is_selected: Bool
        :return: None
        """
        self.is_selected = is_selected

    def draw(self, win):
        """
        Draw the tower and the range circle
        :param win:
        :return:
        """
        # draw range circle
        if self.is_selected:
            self.range_circle.draw_transparent(win)
        # draw tower
        win.blit(self.image, self.rect)


class TowerGroup:
    def __init__(self):
        self.constructed_tower = [Tower(250, 380), Tower(420, 400), Tower(600, 400)]

    def get(self):
        return self.constructed_tower


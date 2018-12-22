import pygame
import vector
import button
import box
from pygame.constants import *
from colors import *

from tile import Tile
from towers import CannonTower, ArtilleryTower
from enemy import Boss
from map import Map

def get_active(group):
    for active_sprite in group:
        if active_sprite.active_state == 1:
            return active_sprite
    empty_sprite = pygame.sprite.Sprite()
    empty_sprite.active_state = 0
    return empty_sprite


class Game:
    def __init__(self, map_name):
        pygame.init()

        self.map = Map(map_name)
        self.window_size = [self.map.pixel_size[0] + 250, self.map.pixel_size[1] + 150]
        self.window = pygame.display.set_mode(self.window_size)

        self.clock = pygame.time.Clock()
        self.fps = 120
        self.init_content()


    def init_content(self):
        info_box = box.Box(200, 400, [self.map.pixel_size[0] + 25, 100], white, 150)
        info_box.add_text([100, 10], "this is awesome", 20, black, 'center')

        cannon_button = button.Button(white, 60, 60, [self.map.pixel_size[0] + 25, 10])
        cannon_button.set_icon_image('data/images/cannon.png', 40, 40)
        cannon_button.function = self.create_cannon_tower

        artillery_button = button.Button(white, 60, 60, [self.map.pixel_size[0] + 25 + 60 + 10, 10])
        artillery_button.set_icon_image('data/images/artillery.png', 55, 55)
        artillery_button.function = self.create_artillery_tower

        self.box_group = pygame.sprite.Group(info_box)
        self.button_group = pygame.sprite.Group(cannon_button, artillery_button)

        

    def create_cannon_tower(self):
        self.map.moving_tower_group.add(CannonTower(self))

    def create_artillery_tower(self):
        self.map.moving_tower_group.add(ArtilleryTower(self))

    def mainloop(self):
        while True:

            mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():
                self.button_group.update(event)
                self.map.handle_event(event, mouse)
                self.handle_event(event)

            # Logic testing:
            self.map.update()

            # Draw everything:
            self.draw_everything()

            # Delay framerate and update display:
            self.clock.tick(self.fps)
            pygame.display.flip()


    def handle_event(self, event):
        if event.type == QUIT:
            pygame.quit()
            quit()
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                self.map.enemy_group.add(Boss(self.map))
            elif event.key == K_r:
                self.map.static_tower_group.empty()
                self.map.enemy_group.empty()
            elif event.key == K_DELETE:
                get_active(self.map.static_tower_group).kill()

    def draw_everything(self):
        self.window.fill(backround)
        self.map.draw(self.window)
        self.button_group.draw(self.window)
        self.box_group.draw(self.window)

        
        
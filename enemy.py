import arcade
from constants import TILE_SCALING

ENEMY_IMAGE = ":resources:images/enemies/wormGreen.png"
ENEMY_MOVE_IMAGE = ":resources:images/enemies/wormGreen_move.png"

ENEMY_SPEED = 1.5
UPDATES_PER_FRAME = 10


class EnemySprite(arcade.Sprite):

    def __init__(self, left_boundary: float, right_boundary: float):
        super().__init__(ENEMY_IMAGE, TILE_SCALING)

        self.left_boundary = left_boundary
        self.right_boundary = right_boundary
        self.change_x = ENEMY_SPEED

        self.idle_texture_right = arcade.load_texture(ENEMY_IMAGE)
        self.idle_texture_left = arcade.load_texture(ENEMY_IMAGE, flipped_horizontally=True)
        self.move_texture_right = arcade.load_texture(ENEMY_MOVE_IMAGE)
        self.move_texture_left = arcade.load_texture(ENEMY_MOVE_IMAGE, flipped_horizontally=True)

        self.cur_frame = 0

    def update(self):
        self.center_x += self.change_x

        if self.center_x >= self.right_boundary:
            self.change_x = -ENEMY_SPEED
        elif self.center_x <= self.left_boundary:
            self.change_x = ENEMY_SPEED

        self.cur_frame += 1
        if self.cur_frame >= UPDATES_PER_FRAME * 2:
            self.cur_frame = 0

        if self.change_x > 0:
            if self.cur_frame < UPDATES_PER_FRAME:
                self.texture = self.idle_texture_right
            else:
                self.texture = self.move_texture_right
        else:
            if self.cur_frame < UPDATES_PER_FRAME:
                self.texture = self.idle_texture_left
            else:
                self.texture = self.move_texture_left

import arcade
from constants import CHARACTER_SCALING

CHARACTER_PATH = ":resources:images/animated_characters/female_adventurer/femaleAdventurer"
UPDATES_PER_FRAME = 5

RIGHT_FACING = 0
LEFT_FACING = 1


def load_texture_pair(filename: str) -> list[arcade.Texture]:
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]


class PlayerSprite(arcade.Sprite):

    def __init__(self):
        super().__init__(scale=CHARACTER_SCALING)

        self.facing_direction = RIGHT_FACING
        self.cur_texture_index = 0

        self.idle_textures = load_texture_pair(f"{CHARACTER_PATH}_idle.png")
        self.jump_texture = load_texture_pair(f"{CHARACTER_PATH}_jump.png")
        self.fall_texture = load_texture_pair(f"{CHARACTER_PATH}_fall.png")

        self.walk_textures = []
        for i in range(8):
            self.walk_textures.append(
                load_texture_pair(f"{CHARACTER_PATH}_walk{i}.png")
            )

        self.texture = self.idle_textures[RIGHT_FACING]

    def update_animation(self, delta_time: float = 1 / 60):
        if self.change_x < 0:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0:
            self.facing_direction = RIGHT_FACING

        if self.change_y > 0:
            self.texture = self.jump_texture[self.facing_direction]
            return
        if self.change_y < 0:
            self.texture = self.fall_texture[self.facing_direction]
            return

        if self.change_x == 0:
            self.texture = self.idle_textures[self.facing_direction]
            return

        self.cur_texture_index += 1
        if self.cur_texture_index >= UPDATES_PER_FRAME * len(self.walk_textures):
            self.cur_texture_index = 0
        frame = self.cur_texture_index // UPDATES_PER_FRAME
        self.texture = self.walk_textures[frame][self.facing_direction]

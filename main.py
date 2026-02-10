import arcade
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_TITLE,
    TILE_SCALING,
    GRID_PIXEL_SIZE,
    PLAYER_MOVEMENT_SPEED,
    GRAVITY,
    PLAYER_JUMP_SPEED,
    PLAYER_DOUBLE_JUMP_SPEED,
    MAX_JUMPS,
    PLAYER_LIVES,
    PLAYER_START_X,
    PLAYER_START_Y,
    LEVELS,
)
from player import PlayerSprite
from enemy import EnemySprite
from particles import make_coin_emitter, make_enemy_emitter, make_hurt_emitter
from highscore import load_highscore, save_highscore
from sound import SoundManager

GRASS_IMAGE = ":resources:images/tiles/grassMid.png"
BOX_IMAGE = ":resources:images/tiles/boxCrate_double.png"
COIN_IMAGE = ":resources:images/items/coinGold.png"
EXIT_IMAGE = ":resources:images/items/flagGreen1.png"
SPIKES_IMAGE = ":resources:images/tiles/spikes.png"

COIN_SCALING = 0.5
EXIT_SCALING = 0.5
SPIKES_SCALING = 0.5
ENEMY_PATROL_RADIUS = 120


def load_level(filename: str) -> list[str]:
    with open(filename, "r") as f:
        lines = f.readlines()
    return [line.rstrip("\n") for line in lines]


def create_sound_manager() -> SoundManager:
    sm = SoundManager()
    sm.register("coin", ":resources:sounds/coin1.wav")
    sm.register("jump", ":resources:sounds/jump1.wav")
    sm.register("hit", ":resources:sounds/hurt1.wav")
    sm.register("gameover", ":resources:sounds/gameover1.wav")
    sm.register("win", ":resources:sounds/upgrade1.wav")
    sm.register("stomp", ":resources:sounds/hit2.wav")
    return sm


class GameView(arcade.View):

    def __init__(self):
        super().__init__()

        self.player_sprite = None
        self.wall_list = None
        self.player_list = None
        self.coin_list = None
        self.exit_list = None
        self.enemy_list = None
        self.hazard_list = None
        self.physics_engine = None
        self.camera = None
        self.gui_camera = None

        self.score = 0
        self.lives = PLAYER_LIVES
        self.current_level = 0
        self.jump_count = 0
        self.cached_highscore = load_highscore()

        self.emitters = []
        self.sfx = create_sound_manager()

    def setup(self):
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)
        self.exit_list = arcade.SpriteList(use_spatial_hash=True)
        self.enemy_list = arcade.SpriteList()
        self.hazard_list = arcade.SpriteList(use_spatial_hash=True)
        self.emitters = []

        self.player_sprite = PlayerSprite()
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.player_list.append(self.player_sprite)

        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.gui_camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        self._build_level(LEVELS[self.current_level])

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            self.wall_list,
            gravity_constant=GRAVITY,
        )

    def _load_next_level(self):
        self.current_level += 1
        if self.current_level >= len(LEVELS):
            save_highscore(self.score)
            self.cached_highscore = max(self.cached_highscore, self.score)
            self.sfx.play("win")
            from views import WinView
            self.window.show_view(WinView(self.score))
            return

        self.wall_list.clear()
        self.coin_list.clear()
        self.exit_list.clear()
        self.enemy_list.clear()
        self.hazard_list.clear()
        self.emitters.clear()

        self._build_level(LEVELS[self.current_level])

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            self.wall_list,
            gravity_constant=GRAVITY,
        )

    def _respawn_player(self):
        self.lives -= 1
        self.sfx.play("hit")
        # self.emitters.append(
        #     make_hurt_emitter(self.player_sprite.center_x, self.player_sprite.center_y)
        # )

        if self.lives <= 0:
            save_highscore(self.score)
            self.cached_highscore = max(self.cached_highscore, self.score)
            self.sfx.play("gameover")
            from views import GameOverView
            self.window.show_view(GameOverView(self.score))
            return

        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y

    def _build_level(self, map_file: str):
        level_data = load_level(map_file)

        for row_index, row in enumerate(level_data):
            for col_index, char in enumerate(row):
                if char == ".":
                    continue

                x = col_index * GRID_PIXEL_SIZE + GRID_PIXEL_SIZE / 2
                y = (len(level_data) - 1 - row_index) * GRID_PIXEL_SIZE + GRID_PIXEL_SIZE / 2

                if char == "G":
                    sprite = arcade.Sprite(GRASS_IMAGE, TILE_SCALING)
                    sprite.center_x = x
                    sprite.center_y = y
                    self.wall_list.append(sprite)
                elif char == "B":
                    sprite = arcade.Sprite(BOX_IMAGE, TILE_SCALING)
                    sprite.center_x = x
                    sprite.center_y = y
                    self.wall_list.append(sprite)
                elif char == "C":
                    sprite = arcade.Sprite(COIN_IMAGE, COIN_SCALING)
                    sprite.center_x = x
                    sprite.center_y = y
                    self.coin_list.append(sprite)
                elif char == "E":
                    sprite = arcade.Sprite(EXIT_IMAGE, EXIT_SCALING)
                    sprite.center_x = x
                    sprite.center_y = y
                    self.exit_list.append(sprite)
                elif char == "S":
                    sprite = arcade.Sprite(SPIKES_IMAGE, SPIKES_SCALING)
                    sprite.center_x = x
                    sprite.center_y = y
                    self.hazard_list.append(sprite)
                elif char == "W":
                    enemy = EnemySprite(
                        left_boundary=x - ENEMY_PATROL_RADIUS,
                        right_boundary=x + ENEMY_PATROL_RADIUS,
                    )
                    enemy.center_x = x
                    enemy.center_y = y
                    self.enemy_list.append(enemy)
                elif char == "1":
                    self.player_sprite.center_x = x
                    self.player_sprite.center_y = y

    def _center_camera_on_player(self):
        screen_center_x = self.player_sprite.center_x - SCREEN_WIDTH / 2
        screen_center_y = self.player_sprite.center_y - SCREEN_HEIGHT / 2

        screen_center_x = max(screen_center_x, 0)
        screen_center_y = max(screen_center_y, 0)

        self.camera.move_to((screen_center_x, screen_center_y))

    def on_draw(self):
        self.clear()

        self.camera.use()
        self.wall_list.draw()
        self.hazard_list.draw()
        self.coin_list.draw()
        self.exit_list.draw()
        self.enemy_list.draw()
        self.player_list.draw()

        for emitter in self.emitters:
            emitter.draw()

        self.gui_camera.use()
        arcade.draw_text(
            f"Очки: {self.score}", 10, SCREEN_HEIGHT - 30,
            arcade.csscolor.WHITE, 18, font_name="Arial",
        )
        arcade.draw_text(
            f"Уровень: {self.current_level + 1}/{len(LEVELS)}",
            10, SCREEN_HEIGHT - 55,
            arcade.csscolor.WHITE, 18, font_name="Arial",
        )
        arcade.draw_text(
            f"Жизни: {self.lives}", 10, SCREEN_HEIGHT - 80,
            arcade.csscolor.RED, 18, font_name="Arial",
        )
        arcade.draw_text(
            f"Рекорд: {self.cached_highscore}",
            SCREEN_WIDTH - 150, SCREEN_HEIGHT - 30,
            arcade.csscolor.GOLD, 18, font_name="Arial",
        )

    def on_update(self, delta_time: float):
        self.physics_engine.update()
        self.enemy_list.update()
        self.player_sprite.update_animation(delta_time)
        self._center_camera_on_player()

        for emitter in self.emitters:
            emitter.update()
        self.emitters = [e for e in self.emitters if not e.can_reap()]

        if self.physics_engine.can_jump():
            self.jump_count = 0

        coins_hit = arcade.check_for_collision_with_list(
            self.player_sprite, self.coin_list
        )
        for coin in coins_hit:
            # self.emitters.append(make_coin_emitter(coin.center_x, coin.center_y))
            coin.remove_from_sprite_lists()
            self.score += 10
            self.sfx.play("coin")

        enemies_hit = arcade.check_for_collision_with_list(
            self.player_sprite, self.enemy_list
        )
        for enemy in enemies_hit:
            if self.player_sprite.center_y > enemy.center_y and self.player_sprite.change_y < 0:
                # self.emitters.append(make_enemy_emitter(enemy.center_x, enemy.center_y))
                enemy.remove_from_sprite_lists()
                self.score += 20
                self.player_sprite.change_y = PLAYER_JUMP_SPEED * 0.6
                self.sfx.play("stomp")
            else:
                self._respawn_player()
                return

        if arcade.check_for_collision_with_list(self.player_sprite, self.hazard_list):
            self._respawn_player()
            return

        if arcade.check_for_collision_with_list(self.player_sprite, self.exit_list):
            self._load_next_level()

        if self.player_sprite.center_y < -100:
            self._respawn_player()

    def on_key_press(self, key: int, modifiers: int):
        if key in (arcade.key.UP, arcade.key.W, arcade.key.SPACE):
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                self.jump_count = 1
                self.sfx.play("jump")
            elif self.jump_count < MAX_JUMPS:
                self.player_sprite.change_y = PLAYER_DOUBLE_JUMP_SPEED
                self.jump_count += 1
                self.sfx.play("jump")
        elif key in (arcade.key.LEFT, arcade.key.A):
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key: int, modifiers: int):
        if key in (arcade.key.LEFT, arcade.key.A):
            self.player_sprite.change_x = 0
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player_sprite.change_x = 0


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    from views import MenuView
    window.show_view(MenuView())
    arcade.run()


if __name__ == "__main__":
    main()

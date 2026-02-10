import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from highscore import load_highscore


class MenuView(arcade.View):

    def on_show_view(self):
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "GALAXY RUNNER",
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 80,
            arcade.csscolor.GOLD, 54,
            anchor_x="center", font_name="Arial",
        )
        arcade.draw_text(
            "Собери монеты и доберись до флага!",
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20,
            arcade.csscolor.WHITE, 20,
            anchor_x="center", font_name="Arial",
        )
        arcade.draw_text(
            "WASD / Стрелки \u2014 движение    |    Пробел \u2014 прыжок",
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 25,
            arcade.csscolor.LIGHT_GRAY, 16,
            anchor_x="center", font_name="Arial",
        )

        highscore = load_highscore()
        if highscore > 0:
            arcade.draw_text(
                f"Рекорд: {highscore}",
                SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 70,
                arcade.csscolor.GOLD, 20,
                anchor_x="center", font_name="Arial",
            )

        arcade.draw_text(
            "Нажми ENTER чтобы начать",
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 130,
            arcade.csscolor.YELLOW, 22,
            anchor_x="center", font_name="Arial",
        )

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.ENTER:
            from main import GameView
            game = GameView()
            game.setup()
            self.window.show_view(game)


class GameOverView(arcade.View):

    def __init__(self, final_score: int):
        super().__init__()
        self.final_score = final_score

    def on_show_view(self):
        arcade.set_background_color(arcade.csscolor.DARK_RED)

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "GAME OVER",
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50,
            arcade.csscolor.WHITE, 54,
            anchor_x="center", font_name="Arial",
        )
        arcade.draw_text(
            f"Очки: {self.final_score}",
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 20,
            arcade.csscolor.YELLOW, 24,
            anchor_x="center", font_name="Arial",
        )

        highscore = load_highscore()
        arcade.draw_text(
            f"Рекорд: {highscore}",
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 55,
            arcade.csscolor.GOLD, 20,
            anchor_x="center", font_name="Arial",
        )

        arcade.draw_text(
            "Нажми ENTER чтобы начать заново",
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 110,
            arcade.csscolor.LIGHT_GRAY, 20,
            anchor_x="center", font_name="Arial",
        )

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.ENTER:
            from main import GameView
            game = GameView()
            game.setup()
            self.window.show_view(game)


class WinView(arcade.View):

    def __init__(self, final_score: int):
        super().__init__()
        self.final_score = final_score

    def on_show_view(self):
        arcade.set_background_color(arcade.csscolor.DARK_GREEN)

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "ПОБЕДА!",
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50,
            arcade.csscolor.GOLD, 54,
            anchor_x="center", font_name="Arial",
        )
        arcade.draw_text(
            f"Финальный счёт: {self.final_score}",
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 20,
            arcade.csscolor.WHITE, 24,
            anchor_x="center", font_name="Arial",
        )

        highscore = load_highscore()
        arcade.draw_text(
            f"Рекорд: {highscore}",
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 55,
            arcade.csscolor.GOLD, 20,
            anchor_x="center", font_name="Arial",
        )

        arcade.draw_text(
            "Нажми ENTER чтобы играть снова",
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 110,
            arcade.csscolor.LIGHT_GRAY, 20,
            anchor_x="center", font_name="Arial",
        )

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.ENTER:
            from main import GameView
            game = GameView()
            game.setup()
            self.window.show_view(game)

import pyray
from raylib import colors
import random


class Object:
    def __init__(self, pos_x, pos_y, width, height, color, shift_x, shift_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.color = color
        self.shift_x = shift_x
        self.shift_y = shift_y

    def reset(self, pos_x, pos_y, shift_x, shift_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.shift_x = shift_x
        self.shift_y = shift_y

    def draw_object(self):
        pyray.draw_rectangle(self.pos_x, self.pos_y, self.width, self.height, self.color)


class Player(Object):
    def __init__(self, pos_x, pos_y, width, height, color, shift_x, shift_y, name, count_of_wins):
        super().__init__(pos_x, pos_y, width, height, color, shift_x, shift_y)
        self.name = name
        self.count_of_wins = count_of_wins

    def rendering_and_movement(self, window_height):
        self.draw_object()
        self.pressed_key(window_height)

    def pressed_key(self, window_height):
        if self.name == "Pl1: ":
            if pyray.is_key_down(pyray.KeyboardKey(87)):
                if self.pos_y >= 0:
                    self.pos_y -= self.shift_y
            if pyray.is_key_down(pyray.KeyboardKey(83)):
                if self.pos_y + self.height <= window_height:
                    self.pos_y += self.shift_y
        else:
            if pyray.is_key_down(pyray.KeyboardKey(73)):
                if self.pos_y >= 0:
                    self.pos_y -= self.shift_y
            if pyray.is_key_down(pyray.KeyboardKey(75)):
                if self.pos_y + self.height <= window_height:
                    self.pos_y += self.shift_y

    def draw_text(self, window_width):
        collision_text_format = self.name + str(self.count_of_wins)
        if self.name == "Pl1: ":
            pyray.draw_text(collision_text_format.format(), window_width // 2 - 50 - 100, self.pos_y // 6, 50, colors.BLUE)
        else:
            pyray.draw_text(collision_text_format.format(), window_width // 2 - 50 + 100, self.pos_y // 6, 50, colors.RED)

    def winner(self):
        self.count_of_wins += 1


class Ball(Object):
    def __init__(self, pos_x, pos_y, width, height, color, shift_x, shift_y):
        super().__init__(pos_x, pos_y, width, height, color, shift_x, shift_y)

    def ball_shift(self):
        self.pos_x += self.shift_x
        self.pos_y += self.shift_y

    def bounce(self):
        self.shift_x *= -1

    def collide_with_vertical_border(self, window_height):
        if self.pos_y <= 0 or self.pos_y >= window_height - self.height:
            return True
        return False

    def collide_with_horizontal_border(self, window_width):
        if self.pos_x <= 0 or self.pos_x + self.width >= window_width:
            return True

    def collide_with_plrs(self, plr1_pos_x, plr1_pos_y, plr2_pos_x, plr2_pos_y, plr_width, plr_height):
        if collide_with_plr1(plr1_pos_x, plr1_pos_y, self.pos_x, self.pos_y, plr_width, plr_height, self.height):
            return True
        if collide_with_plr2(plr2_pos_x, plr2_pos_y, self.pos_x, self.pos_y, plr_height, self.width, self.height):
            return True
        return False

    def check_collides(self, window_width, window_height, plr1_pos_x, plr1_pos_y, plr2_pos_x, plr2_pos_y, plr_width, plr_height):
        # проверка на коллизию мяча с вертикалями
        if self.collide_with_vertical_border(window_height):
            self.shift_y *= -1
            return False
        # проверка на коллизию мяча с игроками
        if self.collide_with_plrs(plr1_pos_x, plr1_pos_y, plr2_pos_x, plr2_pos_y, plr_width, plr_height):
            self.bounce()
            if self.shift_x > 0:
                self.shift_x += 1
            else:
                self.shift_x -= 1
            self.shift_y += random.choice([-window_height // 225 * 2, window_height // 225 * 2])
            return False
        # конец игры
        if self.collide_with_horizontal_border(window_width):
            return True

    def who_win(self, window_width):
        if self.pos_x <= 0:
            return "Pl2"
        elif self.pos_x + self.width >= window_width:
            return "Pl1"


class Scene:
    def __init__(self, scene):
        self.scene = scene

    def scene_changed(self, window_width, window_height, player1, player2, ball):
        if self.scene == "menu":
            self.reset_objects(window_width, window_height, player1, player2, ball)
            self.scene_menu(window_width, window_height, player1, player2)
        elif self.scene == "game":
            self.scene_game(window_width, window_height, player1, player2, ball)
        elif self.scene == "exit":
            self.exit()

    def reset_objects(self, window_width, window_height, player1, player2, ball):
        player1.reset(window_height // 30, window_height // 2 - window_height // 6, 0, window_height // 225,)
        player2.reset(window_width - window_height // 30 * 2, window_height // 2 - window_height // 6, 0, window_height // 225,)
        ball.reset(window_width // 2 - window_height // 30, window_height // 2 - window_height // 30,
            random.choice([-window_height // 225 * 2, window_height // 225 * 2]), random.choice([-window_height // 225, window_height // 225]))

    def scene_menu(self, window_width, window_height, player1, player2):
        #кнопки
        button_scene_new_game = pyray.Rectangle(window_width / 2 - 100 / 2, window_height / 2 - 10 - 50, 100, 50)
        button_scene_exit = pyray.Rectangle(window_width / 2 - 100 / 2, window_height / 2 + 10, 100, 50)

        #отрисовка менюшки
        player1.draw_text(window_width)
        player2.draw_text(window_width)
        if pyray.gui_button(button_scene_new_game, 'New game'):
            self.scene = "game"
        if pyray.gui_button(button_scene_exit, 'Exit'):
            self.scene = "exit"

    def scene_game(self, window_width, window_height, player1, player2, ball):
        # отрисовкац
        player1.rendering_and_movement(window_height)
        player2.rendering_and_movement(window_height)
        ball.draw_object()

        # движение мяча
        ball.ball_shift()

        # проверка на коллизию
        if ball.check_collides(window_width, window_height, player1.pos_x, player1.pos_y, player2.pos_x, player2.pos_y,
                               window_height // 22, window_height // 3):
            self.scene = "menu"
            if ball.who_win(window_width) == "Pl1":
                player1.winner()
            else:
                player2.winner()

    def exit(self):
        pyray.close_window()
        exit(0)


def collide_with_plr1(plr_pos_x, plr_pos_y, ball_pos_x, ball_pos_y, plr_width, plr_height, ball_height):
    if plr_pos_x + plr_width >= ball_pos_x and (plr_pos_y <= ball_pos_y + ball_height and plr_pos_y + plr_height >= ball_pos_y):
        return True
    return False


def collide_with_plr2(plr_pos_x, plr_pos_y, ball_pos_x, ball_pos_y, plr_height, ball_width, ball_height):
    if plr_pos_x <= ball_pos_x + ball_width and (plr_pos_y <= ball_pos_y + ball_height and plr_pos_y + plr_height >= ball_pos_y):
        return True
    return False


def end_game():
    pyray.close_window()
    exit(0)


def main():
    #окно
    window_width, window_height = 1920, 1080
    pyray.init_window(window_width, window_height, 'PingPong')
    pyray.set_target_fps(60)

    # инициальизация объектов
    player1 = Player(window_height // 30, window_height // 2 - window_height // 6, window_height // 30, window_height // 3, colors.BLUE, 0, window_height // 225,
                     "Pl1: ", 0)
    player2 = Player(window_width - window_height // 30 * 2, window_height // 2 - window_height // 6, window_height // 30, window_height // 3, colors.RED, 0, window_height // 225,
                     "Pl2: ", 0)
    ball = Ball(window_width // 2 - window_height // 30, window_height // 2 - window_height // 30, window_height // 30,
                window_height // 30, colors.WHITE, random.choice([-window_height // 225 * 2, window_height // 225 * 2]), random.choice([-window_height // 225, window_height // 225]))
    scene = Scene("menu")

    while not pyray.window_should_close():
        pyray.begin_drawing()
        scene.scene_changed(window_width, window_height, player1, player2, ball)
        pyray.clear_background(colors.BLACK)
        pyray.end_drawing()
    pyray.close_window()


if __name__ == '__main__':
    main()
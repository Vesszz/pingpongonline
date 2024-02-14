import pyray
from raylib import colors
import random


class Player:
    def __init__(self, pos_x, pos_y, width, height, color, shift, name, count_of_wins):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.color = color
        self.shift = shift
        self.name = name
        self.count_of_wins = count_of_wins

    def rendering_and_movement(self, window_height, ):
        self.draw_rect()
        self.pressed_key()
        self.shift_Y(window_height)
        if self.collide_with_vertical_border(window_height):
            self.shift_reset()

    def draw_rect(self):
        pyray.draw_rectangle(self.pos_x, self.pos_y, self.width, self.height, self.color)

    def pressed_key(self):
        if pyray.is_key_pressed(pyray.KeyboardKey(87)):
            self.shift = -2
        if pyray.is_key_pressed(pyray.KeyboardKey(83)):
            self.shift = 2

    def draw_text(self, window_width):
        collision_text_format = self.name + str(self.count_of_wins)
        if self.name == "Pl1: ":
            pyray.draw_text(collision_text_format.format(), 10, 10, 50, colors.BLUE)
        else:
            pyray.draw_text(collision_text_format.format(), window_width - 145, 10, 50, colors.RED)

    def collide_with_vertical_border(self, window_height):
        if self.pos_y <= 0 or self.pos_y + self.height >= window_height:
            return True

    def shift_Y(self, window_height):
        self.pos_y += self.shift

    def shift_reset(self):
        self.shift = 0


class Ball:
    def __init__(self, pos_x, pos_y, width, height, color, shift_x, shift_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.color = color
        self.shift_x = shift_x
        self.shift_y = shift_y
        self.max_shift = 10

    def draw_ball(self):
        pyray.draw_rectangle(self.pos_x, self.pos_y, self.width, self.height, self.color)

    def shift(self):
        self.pos_x += self.shift_x
        self.pos_y += self.shift_y

    def bounce(self):
        self.shift_x *= -1

    def collide_with_vertical_border(self, window_height):
        if self.pos_y <= 0 or self.pos_y >= window_height - 20:
            return True
        return False

    def collide_with_horizontal_border(self, window_width):
        if self.pos_x <= 0 or self.pos_x + 20 >= window_width:
            return True

    def collide_with_plrs(self, plr1_pos_x, plr1_pos_y, plr2_pos_x, plr2_pos_y, plr_height):
        if collide_with_plr1(plr1_pos_x, plr1_pos_y, self.pos_x, self.pos_y, plr_height):
            return True
        if collide_with_plr2(plr2_pos_x, plr2_pos_y, self.pos_x, self.pos_y, plr_height):
            return True
        return False

    def check_collides(self, window_width, window_height, plr1_pos_x, plr1_pos_y, plr2_pos_x, plr2_pos_y, plr_height):
        # проверка на коллизию мяча с вертикалями
        if self.collide_with_vertical_border(window_height):
            self.shift_y *= -1
            return False
        # проверка на коллизию мяча с игроками
        if self.collide_with_plrs(plr1_pos_x, plr1_pos_y, plr2_pos_x, plr2_pos_y, plr_height):
            self.bounce()
            self.shift_y += random.randint(-5, 5)
            if self.shift_x > 0:
                if self.shift_x != self.max_shift:
                    self.shift_x += 1
            else:
                if self.shift_x != self.max_shift:
                    self.shift_x -= 1
            return False
        # конец игры
        if self.collide_with_horizontal_border(window_width):
            return True

    def who_win(self, window_width):
        if self.pos_x <= 0:
            return "red"
        elif self.pos_x + 20 >= window_width:
            return "blue"


def collide_with_plr1(plr_pos_x, plr_pos_y, ball_pos_x, ball_pos_y, plr_height):
    if plr_pos_x + 20 >= ball_pos_x and (plr_pos_y <= ball_pos_y + 20 and plr_pos_y + plr_height >= ball_pos_y):
        return True
    return False


def collide_with_plr2(plr_pos_x, plr_pos_y, ball_pos_x, ball_pos_y, plr_height):
    if plr_pos_x <= ball_pos_x + 20 and (plr_pos_y <= ball_pos_y + 20 and plr_pos_y + plr_height >= ball_pos_y):
        return True
    return False


def scene_changed(name):
    return name


def end_game():
    pyray.close_window()
    exit(0)


def main():
    # окно
    window_width, window_height = 1050, 450
    pyray.init_window(window_width, window_height, 'PingPong')
    pyray.set_target_fps(60)

    #кнопки
    button_scene_new_game = pyray.Rectangle(window_width / 2 - 100 / 2, window_height / 2 - 10 - 50, 100, 50)
    button_scene_exit = pyray.Rectangle(window_width / 2 - 100 / 2, window_height / 2 + 10, 100, 50)

    plr_win = ""
    scene = "menu"
    player1_count_of_wins = 0
    player2_count_of_wins = 0

    while not pyray.window_should_close():
        pyray.begin_drawing()
        if scene == "menu":
            #позиции для игроков и мячей
            player1 = Player(20, window_height // 2 - 70, 20, 140, colors.BLUE, 0, "Pl1: ", player1_count_of_wins)
            player2 = Player(window_width - 40, window_height // 2 - 70, 20, 140, colors.RED, 0, "Pl2: ", player2_count_of_wins)
            ball = Ball(window_width // 2 - 20, window_height // 2 - 10, 20, 20, colors.WHITE, random.choice([-4, 4]), random.choice([-2, 2]))

            #отрисовка счета игроков и кнопок старта и вызода из игры
            player1.draw_text(window_width)
            player2.draw_text(window_width)
            if pyray.gui_button(button_scene_new_game, 'New game'):
                scene = scene_changed("game")
            if pyray.gui_button(button_scene_exit, 'Exit'):
                end_game()
        elif scene == "game":
            #отрисовка
            player1.rendering_and_movement(window_height)
            player2.rendering_and_movement(window_height)
            ball.draw_ball()

            #движение мяча
            ball.shift()

            # проверка на коллизию
            if ball.check_collides(window_width, window_height, player1.pos_x, player1.pos_y, player2.pos_x, player2.pos_y, player1.height):
                scene = scene_changed("menu")
                plr_win = ball.who_win(window_width)
                if plr_win == "blue":
                    player1_count_of_wins += 1
                else:
                    player2_count_of_wins += 1

        pyray.clear_background(colors.BLACK)
        pyray.end_drawing()
    pyray.close_window()


if __name__ == '__main__':
        main()
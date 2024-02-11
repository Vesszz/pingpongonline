import pyray
from raylib import colors
import random

class Player:
    def __init__(self, pos_x, pos_y, width, height, color, shift):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.color = color
        self.shift = shift

    def draw_rect(self):
        pyray.draw_rectangle(self.pos_x, self.pos_y, self.width, self.height, self.color)

    def pressed_key(self, window_height):
        if pyray.is_key_down(pyray.KeyboardKey(87)):
            if self.pos_y >= 0:
                self.pos_y -= self.shift
        if pyray.is_key_down(pyray.KeyboardKey(83)):
            if self.pos_y + 135 <= window_height:
                self.pos_y += self.shift


class Ball:
    def __init__(self, pos_x, pos_y, width, height, color, shift_x, shift_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.color = color
        self.shift_x = shift_x
        self.shift_y = shift_y

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

    def who_win(self, window_width):
        if self.pos_x <= 0:
            return "red"
        elif self.pos_x + 20 >= window_width:
            return "blue"

    def collide_with_plrs(self, plr1_pos_x, plr1_pos_y, plr2_pos_x, plr2_pos_y):
        if collide_with_plr1(plr1_pos_x, plr1_pos_y, self.pos_x, self.pos_y):
            return True
        if collide_with_plr2(plr2_pos_x, plr2_pos_y, self.pos_x, self.pos_y):
            return True
        return False


def collide_with_plr1(plr_pos_x, plr_pos_y, ball_pos_x, ball_pos_y):
    if plr_pos_x + 20 >= ball_pos_x and (plr_pos_y <= ball_pos_y + 20 and plr_pos_y + 135 >= ball_pos_y):
        return True
    return False


def collide_with_plr2(plr_pos_x, plr_pos_y, ball_pos_x, ball_pos_y):
    if plr_pos_x <= ball_pos_x + 20 and (plr_pos_y <= ball_pos_y + 20 and plr_pos_y + 135 >= ball_pos_y):
        return True
    return False

def end_game(plr_win):
    if plr_win == "red":
        pyray.draw_rectangle(100, 100, 100, 100, colors.RED)
    elif plr_win == "blue":
        pyray.draw_rectangle(100, 100, 100, 100, colors.BLUE)


def main():
    #сцена
    plr_win = ""
    scene = "game"

    # объекты
    player1 = Player(0, 135, 20, 135, colors.BLUE, 2)
    player2 = Player(980, 135, 20, 135, colors.RED, 2)
    ball = Ball(480, 180, 20, 20, colors.WHITE, random.choice([-4, 4]), random.choice([-2, 2]))

    #окно
    window_width, window_height = 1000, 400
    pyray.init_window(window_width, window_height, 'PingPong')
    pyray.set_target_fps(60)

    while not pyray.window_should_close():
        pyray.begin_drawing()
        #Отрисовка
        if scene == "game":
            player1.draw_rect()
            player2.draw_rect()
            player1.pressed_key(window_height)
            player2.pressed_key(window_height)
            ball.draw_ball()

            #движение мяча
            ball.shift()
            # проверка на коллизию мяча с вертикалями
            if ball.collide_with_vertical_border(window_height):
                ball.shift_y *= -1
            #проверка на коллизию мяча с игроками
            if ball.collide_with_plrs(player1.pos_x, player1.pos_y, player2.pos_x, player2.pos_y):
                ball.bounce()
                if ball.shift_x > 0:
                    ball.shift_x += 1
                else:
                    ball.shift_x -= 1
             
            #конец игры
            if ball.collide_with_horizontal_border(window_width):
                scene = "end_game"
                plr_win = ball.who_win(window_width)

        elif scene == "end_game":
            end_game(plr_win)

        pyray.clear_background(colors.BLACK)
        pyray.end_drawing()
    pyray.close_window()


if __name__ == '__main__':
        main()
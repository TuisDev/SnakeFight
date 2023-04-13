import sys
import pygame as pg
from pygame.locals import *
import random
import os
import socket

class Color:
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    grey = (15, 15, 15)
    cyan = (0, 255, 255)
    white = (255, 255, 255)
    purple = (100, 0, 100)
    black = (0, 0, 0)
    orange = (255, 127, 0)
    grey_blue = (20, 20, 100)
    grey_green = (20, 100, 20)

class player_color:
    blue = (0, 0, 255)
    green = (0, 255, 0)
    red = (255, 0, 0)
    yellow = (255, 255, 0)
    purple = (255, 0, 255)
    orange = (255, 128, 0)
    cyan = (0, 255, 255)
    
    translate = {
        blue: 'blue', green: 'green', yellow: 'yellow', red: 'red', cyan: 'cyan', orange: 'orange', purple: 'purple'
    }

class Snake:
    def __init__(self, input_direction: str, key: tuple, color: tuple, size: int, start_pos: tuple):
        self.direction = input_direction[:]
        self.next_direction = input_direction[:]
        self.color = color
        self.attack = False
        self.degree = 0
        self.offset = [0, 0]
        self.animation_tick = 0
        self.north_key = key[0]
        self.east_key = key[1]
        self.south_key = key[2]
        self.west_key = key[3]
        self.pos_lst = [(start_pos[0], start_pos[1], size, size),]
        self.lst_index = 0
        self.head = Rect(start_pos[0], start_pos[1], size, size)
        self.boost = 1
        self.size = size
        self.face = (0, 0, 0, 0) 
        self.fangs = (0, 0, 0, 0)

def winscreen(input_color):
    screen = pg.display.set_mode((500, 500), pg.RESIZABLE)
    clock = pg.time.Clock()
    done = False

    
    while not done:
        size = screen.get_size()
        if size[0] < size[1]:
            length = size[0]
        else:
            length = size[1]
        vl = length / 100
        offsetx = int((size[0] - length) / 2)
        offsety = int((size[1] - length) / 2)

        font = pg.font.Font('freesansbold.ttf', int(6.4 * vl))

        text = font.render(f' {player_color.translate[input_color].upper()} WINS! ', True, input_color, Color.white)
        text_size = text.get_rect().size
    
        replay = font.render(' Play Again? ', True, input_color, Color.white)
        replay_size = replay.get_rect().size
    
        quit = font.render(' Quit? ', True, input_color, Color.white)
        quit_size = quit.get_rect().size

        screen.blit(text, (offsetx + length / 2 - text_size[0] / 2, offsety + int(65 * vl)))
        screen.blit(replay, (offsetx + length / 2 - replay_size[0] / 2, offsety + int(75 * vl)))
        screen.blit(quit, (offsetx + length / 2 - quit_size[0] / 2, offsety + int(85 * vl)))
        win_pic = pg.image.load('snakewin.png')
        win_pic = pg.transform.scale(win_pic, (int(46 * vl), int(43 * vl)))
        win_rect = win_pic.get_rect().size
        pg.draw.rect(screen, input_color, (offsetx + int(31 * vl), offsety + int(17 * vl), win_rect[0], win_rect[1]))
        screen.blit(win_pic, (offsetx + int(31 * vl), offsety + int(17 * vl)))
  
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.MOUSEBUTTONDOWN:
                if offsetx + length / 2 - replay_size[0] / 2 <= pg.mouse.get_pos()[0] <= offsetx + length / 2 + replay_size[0] / 2 and offsety + int(75 * vl) <= pg.mouse.get_pos()[1] <= offsety + int(75 * vl) + replay_size[1]:
                    return True
                elif offsetx + int(41 * vl) <= pg.mouse.get_pos()[0] <= offsetx + int(59 * vl) and offsety + int(85 * vl) <= pg.mouse.get_pos()[1] <= offsety + int(85 * vl) + quit_size[1]:
                    os.system('python titlescreen.py')
            
        pg.display.flip()
        clock.tick(100)

    pg.quit()
    sys.exit() 
        
def main():
    green_snake = Snake('south', (pg.K_w, pg.K_d, pg.K_s, pg.K_a), player_color.green, 20, (80, 80))
    yellow_snake = Snake('south', (pg.K_t, pg.K_h, pg.K_g, pg.K_f), player_color.yellow, 20, (20, 20))
    red_snake = Snake('south', (pg.K_i, pg.K_l, pg.K_k, pg.K_j), player_color.red, 20, (40, 40))
    blue_snake = Snake('south', (pg.K_UP, pg.K_RIGHT, pg.K_DOWN, pg.K_LEFT), player_color.blue, 20, (40, 60))
    
    snakes = [green_snake, blue_snake]

    
    total_length, total_height = 700, 700
    total_screen = pg.Surface((700, 700))
    length, height = 500, 500
    screen = pg.Surface((500, 500))
    snake_window = pg.display.set_mode((400, 400), pg.RESIZABLE)
    rand1 = random.randint(100, 400), random.randint(100, 400)
    rand2 = random.randint(100, 400), random.randint(100, 400)
    clock = pg.time.Clock()
    done = False
    husk = list()
    with open('map.txt', 'rb') as map_file:
        map_info = map_file.readline()
    brick_img = pg.image.load('brick.png')
    brick_img = pg.transform.scale(brick_img, (20, 20))
    
    fang_bite = [
        pg.image.load('fang1.png'), pg.image.load('fang2.png'),
        pg.image.load('fang3.png'), pg.image.load('fang4.png'),
        pg.image.load('fang4.png'), pg.image.load('fang4.png'),
        pg.image.load('fang4.png'), pg.image.load('fang4.png'),
        pg.image.load('fang3.png'), pg.image.load('fang2.png'), 
    ]

    for snake in snakes:
        for i in range(4):
            if snake.direction == "east":
                snake.head.x += 2
                snake.degree = 0
                snake.face = Rect(snake.head.x + snake.size - 1, snake.head.y + 1, 1, snake.size - 2)
                if snake.attack:
                    snake.fangs = Rect(snake.head.x + snake.size - 1, snake.head.y + 1, 20, snake.size - 2)
            elif snake.direction == "west":
                snake.head.x -= 2
                snake.degree = 180
                snake.face = Rect(snake.head.x - 1, snake.head.y + 1, 1, snake.size - 2)
                if snake.attack:
                    snake.fangs = Rect(snake.head.x - 20, snake.head.y - 1, 20, snake.size - 2)
            elif snake.direction == "north":
                snake.head.y -= 2
                snake.degree = 90
                snake.face = Rect(snake.head.x + 0, snake.head.y - 1, snake.size - 2, 1)
                if snake.attack:
                    snake.fangs = Rect(snake.head.x + 0, snake.head.y - 20, snake.size - 2, 20)
            elif snake.direction == "south":
                snake.head.y += 2
                snake.degree = 270
                snake.face = Rect(snake.head.x + 1, snake.head.y + snake.size - 1, snake.size - 2, 1)
                if snake.attack:
                    snake.fangs = Rect(snake.head.x + 1, snake.head.y + snake.size - 1, snake.size - 2, 20)



                snake.pos_lst.insert(0, snake.head[:])



    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.KEYDOWN:
                for snake in snakes:
                    if event.key == snake.north_key:
                        if snake.direction != "south":
                            if snake.direction == 'north':
                                snake.boost = 6
                            snake.next_direction = "north"
                        else:
                            snake.attack = True
                    if event.key == snake.east_key:
                        if snake.direction != "west":
                            if snake.direction == 'east':
                                snake.boost = 6
                            snake.next_direction = "east"
                        else:
                            snake.attack = True
                    if event.key == snake.south_key:
                        if snake.direction != "north":
                            if snake.direction == 'south':
                                snake.boost = 6
                            snake.next_direction = "south"
                        else:
                            snake.attack = True
                    if event.key == snake.west_key:
                        if snake.direction != "east":
                            if snake.direction == 'west':
                                snake.boost = 6
                            snake.next_direction = "west"
                        else:
                            snake.attack = True

        for snake in snakes:
            if snake.head.x % 20 == 0 and snake.head.y % 20 == 0:
                snake.direction = snake.next_direction

        # Move the player
        for snake in snakes:
            

            for i in range(snake.boost):
                
                if i == 1:
                    if len(snake.pos_lst) <= 4:
                        break
                    for i in range(4):
                        snake.pos_lst.pop(snake.lst_index)
                        if snake.lst_index >= len(snake.pos_lst):
                            snake.lst_index = 0


                if snake.direction == "east":
                    snake.head.x += 2
                    snake.degree = 0
                    snake.face = Rect(snake.head.x + snake.size - 1, snake.head.y + 1, 1, snake.size - 2)
                    if snake.attack:
                        snake.fangs = Rect(snake.head.x + snake.size - 1, snake.head.y + 1, 20, snake.size - 2)
                elif snake.direction == "west":
                    snake.head.x -= 2
                    snake.degree = 180
                    snake.face = Rect(snake.head.x + 0, snake.head.y + 1, 1, snake.size - 2)
                    if snake.attack:
                        snake.fangs = Rect(snake.head.x - 20, snake.head.y - 1, 20, snake.size - 2)
                elif snake.direction == "north":
                    snake.head.y -= 2
                    snake.degree = 90
                    snake.face = Rect(snake.head.x + 1, snake.head.y + 0, snake.size - 2, 1)
                    if snake.attack:
                        snake.fangs = Rect(snake.head.x + 0, snake.head.y - 20, snake.size - 2, 20)
                elif snake.direction == "south":
                    snake.head.y += 2
                    snake.degree = 270
                    snake.face = Rect(snake.head.x + 1, snake.head.y + snake.size - 1, snake.size - 2, 1)
                    if snake.attack:
                        snake.fangs = Rect(snake.head.x + 1, snake.head.y + snake.size - 1, snake.size - 2, 20)

                


                snake.pos_lst.insert(0, snake.head[:])
                snake.pos_lst.pop(-1)
                    
                snake.boost = 1


            # Check if the player is out of bounds
            if (
                snake.face.x < -1
                or snake.face.x > length + 1
                or snake.face.y < -1
                or snake.face.y > length + 1
            ):
                snakes.remove(snake)

            for test_snake in snakes:
                if snake.attack and test_snake.pos_lst[3:]:
                    collide_index = snake.fangs.collidelist(test_snake.pos_lst[3:])
                    if collide_index != -1:
                        collide_lst = [test_snake.pos_lst[i] for i in snake.fangs.collidelistall(test_snake.pos_lst[3:])]
                        if collide_index + 20 < len(test_snake.pos_lst):
                            new_husk = [i for i in test_snake.pos_lst[collide_index + 20:] if not snake.fangs.colliderect(i)]
                            husk.extend(new_husk)
                        test_snake.pos_lst = [i for i in test_snake.pos_lst[:collide_index] if not i in collide_lst]
                
                elif test_snake.pos_lst[3:]:
                    if snake.face.collidelist(test_snake.pos_lst[3:]) != -1:
                        snakes.remove(snake)
                

            if len(snake.pos_lst) == 0 or snake.face.collidelist(husk) != -1:
                snakes.remove(snake)

            for i in range(625):
                if snake.attack:
                    snake_pos_one = int(snake.fangs.x / 20) + 25 * int(snake.fangs.y / 20)
                    snake_pos_two = int((snake.fangs.x + snake.fangs.size[0]) / 20) + 25 * int((snake.fangs.y + snake.fangs.size[1]) / 20)
                    if i == snake_pos_one or i == snake_pos_two:
                        byte = int(i / 4)
                        bit = 2 * (i % 4)
                        tile = (map_info[byte] << bit & 255) >> 6
                        if tile == 2:
                            map_byte = map_info[byte]
                            index = 6 - bit
                            map_byte = 0b11 << index | map_byte
                            map_byte = ((0b11 << index) ^ 0xFF) & map_byte
                            map_info = map_info[:byte] + map_byte.to_bytes(1, 'little') + map_info[byte + 1:]
                        if tile == 3:
                            for i in range(25):
                                snake.pos_lst.append(snake.pos_lst[-1][:])
                            map_byte = map_info[byte]
                            index = 6 - bit
                            map_byte = 0b11 << index | map_byte
                            map_byte = ((0b11 << index) ^ 0xFF) & map_byte
                            map_info = map_info[:byte] + map_byte.to_bytes(1, 'little') + map_info[byte + 1:]

                snake_pos = int(snake.face.x / 20) + 25 * int(snake.face.y / 20)
                if i == snake_pos:
                    byte = int(i / 4)
                    bit = 2 * (i % 4)
                    tile = (map_info[byte] << bit & 255) >> 6
                    if  tile == 1:
                        snakes.remove(snake)
                    elif tile == 2:
                        snakes.remove(snake)
                    elif tile == 3:
                        for i in range(25):
                            snake.pos_lst.append(snake.pos_lst[-1])
                        map_byte = map_info[byte]
                        index = 6 - bit
                        map_byte = 0b11 << index | map_byte
                        map_byte = ((0b11 << index) ^ 0xFF) & map_byte
                        map_info = map_info[:byte] + map_byte.to_bytes(1, 'little') + map_info[byte + 1:]

        ## Send Data to Client ##
        



        if len(snakes) > 1:
            screen.fill(Color.grey)

            for i in range(625):
                color_alternate = {0: (174, 247, 119), 1:(134, 189, 92)}
                pg.draw.rect(screen, color_alternate[(i % 25 + int(i / 25)) % 2], ((i % 25) * 20, int(i / 25) * 20, 20, 20))

            for snake in snakes:
                if snake.attack:
                    print(snake.animation_tick)
                    if snake.animation_tick > len(fang_bite) - 1:
                        snake.animation_tick = -1
                        snake.attack = False
                    if snake.degree == 270 or snake.degree == 0:
                        snake.offset = 0, 0
                    elif snake.degree == 90:
                        snake.offset = 0, snake.size
                    else:
                        snake.offset = snake.size, 0
                    screen.blit(pg.transform.rotate(fang_bite[snake.animation_tick], snake.degree), (snake.head.x - snake.offset[0], snake.head.y - snake.offset[1]))
                    snake.animation_tick += 1
            
            for rect in husk:
                pg.draw.rect(screen, Color.purple, Rect(rect))
            
            print(husk)
                

            for i in range(625):
                byte = int(i / 4)
                bit = 2 * (i % 4)
                binary_to_image = {0b01: 'brick.png', 0b10: 'wood.png', 0b11: 'apple.png', 0b00: 'blank'}
                image = binary_to_image[(map_info[byte] << bit & 255) >> 6]
                if image != 'blank':
                    image = pg.image.load(image)
                    image = pg.transform.scale(image, (20, 20))
                    screen.blit(image, ((i % 25) * 20, int(i / 25) * 20))



            for snake in snakes:
                for rect in snake.pos_lst:
                    pg.draw.rect(screen, snake.color, rect)                                                                                   
                # pg.draw.rect(screen, Color.red, snake.face, 1)
                # pg.draw.rect(screen, Color.green, snake.fangs, 1)
                
        else:
            print(snakes[0].color)
            return snakes[0].color

        

        total_screen.blit(screen, (100, 100))
        snake_num = [snake.color for snake in snakes].index(Color.blue)
        size = snake_window.get_size()
        if size[0] < size[1]:
            window_length = size[0]
        else:
            window_length = size[1]
        offsetx = size[0] / 2 - window_length / 2
        offsety = size[1] / 2 - window_length / 2
        sub = total_screen.subsurface((snakes[snake_num].head.x, snakes[snake_num].head.y, 200, 200)).copy()
        sub = pg.transform.scale(sub, (window_length, window_length))
        pg.display.set_caption(player_color.translate[snakes[snake_num].color])
        snake_window.blit(sub, (offsetx, offsety))




        pg.display.flip()
        clock.tick(40)

    pg.quit()
    sys.exit()

if __name__ == '__main__':
    pg.init()
    while winscreen(main()): pass
    pg.quit()
    sys.exit()

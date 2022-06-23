import pygame as pg
from pygame.locals import *

pg.init()
screen = pg.display.set_mode((500, 500))
done = False
map = 0b0
brush = 0b00
all_ones = 0x3FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
encoded_map = 0x0
while not done:
    try:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_0:
                    brush = 0b00
                    print(brush)
                elif event.key == pg.K_1:
                    brush = 0b01
                    print(brush)
                elif event.key == pg.K_2:
                    brush = 0b10
                    print(brush)
                elif event.key == pg.K_3:
                    brush = 0b11
                    print(brush)
            if event.type == pg.MOUSEBUTTONDOWN:
                index = int(pg.mouse.get_pos()[0] / 20) * 2 + 25 * int(pg.mouse.get_pos()[1] / 20) * 2
                map = 0b11 << index | map
                map = (((~brush & 255) << index) ^ all_ones) & map
                encoded_map = map.to_bytes(157, 'big')


            for i in range(625):
                color_alternate = {0: (174, 247, 119), 1:(134, 189, 92)}
                pg.draw.rect(screen, color_alternate[(i % 25 + int(i / 25)) % 2], ((i % 25) * 20, int(i / 25) * 20, 20, 20))
            if encoded_map:
                for i in range(625):
                    byte = int(i / 4)
                    bit = 2 * (i % 4)
                    binary_to_image = {0b01: 'brick.png', 0b10: 'goldapple.png', 0b11: 'apple.png', 0b00: 'blank'}
                    image = binary_to_image[(encoded_map[byte] << bit & 255) >> 6]
                    if image != 'blank':
                        image = pg.image.load(image)
                        image = pg.transform.scale(image, (20, 20))
                        screen.blit(image, ((i % 25) * 20, int(i / 25) * 20))

        pg.display.flip() 
    except:
        print(encoded_map)
pg.quit()

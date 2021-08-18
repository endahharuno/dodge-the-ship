import random  # untuk random number
import sys  # untuk exit the program
import pygame
from pygame.locals import *  # Basic pygame imports

FPS = 32
lebar_screen = 868
tinggi_screen = 635
display_screen = pygame.display.set_mode((lebar_screen, tinggi_screen))
base_position = lebar_screen * 0.58
game_image = {}
game_audio_sound = {}
nemo_image = 'assets/images/nemo.png'
bg_image = 'assets/images/bg_screen.png'
ship_image = 'assets/images/kapal.png'


def screen_utama():
    player_x = int(lebar_screen / 5)
    player_y = int((tinggi_screen - game_image['nemo_image'].get_height()) / 2)

    base_x = 0
    while True:
        for event in pygame.event.get():
           # jika press key down atau esc maka exit
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # jika press key up atau space, game start
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                display_screen.blit(game_image['background'], (0, 0))
                display_screen.blit(game_image['nemo_image'], (player_x, player_y))
                display_screen.blit(game_image['base'], (base_x, base_position))
                pygame.display.update()
                time_clock.tick(FPS)


def main_gameplay():
    score = 0
    player_x = int(lebar_screen / 5)
    player_y = int(lebar_screen / 2)
    base_x = 0

    ship1 = get_Random_Ships()
    ship2 = get_Random_Ships()


    up_ships = [
        {'x': lebar_screen + 200, 'y': ship1[0]['y']},
        {'x': lebar_screen + 200 + (lebar_screen / 2), 'y': ship2[0]['y']},
    ]

    low_ships = [
        {'x': lebar_screen + 200, 'y': ship1[1]['y']},
        {'x': lebar_screen + 200 + (lebar_screen / 2), 'y': ship2[1]['y']},
    ]

    ship_Vx = -4
    p_vx = -9
    p_mvx = 10
    p_mvy = -8
    p_accuracy = 1

    p_flap_accuracy = -8
    p_flap = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if player_y > 0:
                    p_vx = p_flap_accuracy
                    p_flap = True
                    game_audio_sound['swim'].play()

        cr_tst = is_Colliding(player_x, player_y, up_ships,
                              low_ships)
        if cr_tst:
            return


        p_middle_positions = player_x + game_image['nemo_image'].get_width() / 2
        for ship in up_ships:
            pip_middle_positions = ship['x'] + game_image['ship'][0].get_width() / 2
            if pip_middle_positions <= p_middle_positions < pip_middle_positions + 4:
                score += 1
                print(f"Your score is {score}")
                game_audio_sound['point'].play()

        if p_vx < p_mvx and not p_flap:
            p_vx += p_accuracy

        if p_flap:
            p_flap = False
        p_height = game_image['nemo_image'].get_height()
        player_y = player_y + min(p_vx, base_position - player_y - p_height)


        for ship_upper, ship_lower in zip(up_ships, low_ships):
            ship_upper['x'] += ship_Vx
            ship_lower['x'] += ship_Vx


        if 0 < up_ships[0]['x'] < 5:
            new_pip = get_Random_Ships()
            up_ships.append(new_pip[0])
            low_ships.append(new_pip[1])


        if up_ships[0]['x'] < -game_image['ship'][0].get_width():
            up_ships.pop(0)
            low_ships.pop(0)


        display_screen.blit(game_image['background'], (0, 0))
        for ship_upper, ship_lower in zip(up_ships, low_ships):
            display_screen.blit(game_image['ship'][0], (ship_upper['x'], ship_upper['y']))
            display_screen.blit(game_image['ship'][1], (ship_lower['x'], ship_lower['y']))

        display_screen.blit(game_image['base'], (base_x, base_position))
        display_screen.blit(game_image['nemo_image'], (player_x, player_y))
        d = [int(x) for x in list(str(score))]
        w = 0
        for digit in d:
            w += game_image['numbers'][digit].get_width()
        Xoffset = (lebar_screen - w) / 2

        for digit in d:
            display_screen.blit(game_image['numbers'][digit], (Xoffset, tinggi_screen * 0.12))
            Xoffset += game_image['numbers'][digit].get_width()
        pygame.display.update()
        time_clock.tick(FPS)

def is_Colliding(player_x, player_y, up_ships, low_ships):
    if player_y > base_position - 25 or player_y < 0:
        game_audio_sound['splash'].play()
        return True

    for ship in up_ships:
        ship_h = game_image['ship'][0].get_height()
        if (player_y < ship_h + ship['y'] and abs(player_x - ship['x']) < game_image['ship'][0].get_width()):
            game_audio_sound['splash'].play()
            return True

    for ship in low_ships:
        if (player_y + game_image['nemo_image'].get_height() > ship['y']) and abs(player_x - ship['x']) < \
                game_image['ship'][0].get_width():
            game_audio_sound['splash'].play()
            return True

    return False


def get_Random_Ships():
    """
    Posisi dua kapal selam
    """
    ship_h = game_image['ship'][0].get_height()
    off_s = tinggi_screen / 3
    yes2 = off_s + random.randrange(0, int(tinggi_screen - game_image['base'].get_height() - 1.2 * off_s))
    shipX = lebar_screen + 10
    y1 = ship_h - yes2 + off_s
    ship = [
        {'x': shipX, 'y': -y1},  # upper ship
        {'x': shipX, 'y': yes2}  # lower ship
    ]
    return ship


if __name__ == "__main__":

    pygame.init()
    time_clock = pygame.time.Clock()
    pygame.display.set_caption('Nemo Game')
    pygame.display.set_icon(pygame.image.load('assets/images/icon.png'))
    game_image['numbers'] = (
        pygame.image.load('assets/images/0.png').convert_alpha(),
        pygame.image.load('assets/images/1.png').convert_alpha(),
        pygame.image.load('assets/images/2.png').convert_alpha(),
        pygame.image.load('assets/images/3.png').convert_alpha(),
        pygame.image.load('assets/images/4.png').convert_alpha(),
        pygame.image.load('assets/images/5.png').convert_alpha(),
        pygame.image.load('assets/images/6.png').convert_alpha(),
        pygame.image.load('assets/images/7.png').convert_alpha(),
        pygame.image.load('assets/images/8.png').convert_alpha(),
        pygame.image.load('assets/images/9.png').convert_alpha(),
    )

    game_image['message'] = pygame.image.load('assets/images/bg_screen.png').convert_alpha()
    game_image['base'] = pygame.image.load('assets/images/base_cp.png').convert_alpha()
    game_image['ship'] = (pygame.image.load(ship_image).convert_alpha(),
                          pygame.image.load(ship_image).convert_alpha()
                          )
    # game_image['ship'] = (pygame.transform.rotate(pygame.image.load(ship_image).convert_alpha(), 180), pygame.image.load(ship_image).convert_alpha())

    # Game sounds
    game_audio_sound['die'] = pygame.mixer.Sound('assets/sounds/die.wav')
    game_audio_sound['splash'] = pygame.mixer.Sound('assets/sounds/splash.wav')
    game_audio_sound['point'] = pygame.mixer.Sound('assets/sounds/point_special.wav')
    game_audio_sound['swim'] = pygame.mixer.Sound('assets/sounds/bloop.wav')

    game_image['background'] = pygame.image.load(bg_image).convert()
    game_image['nemo_image'] = pygame.image.load(nemo_image).convert_alpha()

    while True:
        screen_utama()  # Menampilkan screen utama
        main_gameplay()  # Ini fungsi untuk permainan utama
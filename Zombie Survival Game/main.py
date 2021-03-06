import pickle
import pygame
import random
from classes import *
from asset_load import *

pygame.font.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(35)

# Loads and sets volume of the music.
pygame.mixer.music.load(os.path.join('assets\\music', 'feelgood.ogg'))
pygame.mixer.music.set_volume(0.2)

# Loads and sets volume of the sounds.
GUNSHOTSOUND = pygame.mixer.Sound(os.path.join('assets\\sounds\\gunshot.ogg'))
GUNSHOTSOUND.set_volume(0.7)
ZOMBIE_HIT_SOUND_1 = pygame.mixer.Sound(
    os.path.join('assets\\sounds\\zombie_hit_1.ogg'))
ZOMBIE_HIT_SOUND_2 = pygame.mixer.Sound(
    os.path.join('assets\\sounds\\zombie_hit_2.ogg'))
ZOMBIE_HIT_SOUND_1.set_volume(0.5)
ZOMBIE_HIT_SOUND_2.set_volume(0.5)
PLAYER_HIT_SOUND_1 = pygame.mixer.Sound(
    os.path.join('assets\\sounds\\player_hit.ogg'))
PLAYER_HIT_SOUND_1.set_volume(0.7)

# Creates a display window with imported variables, also sets the caption.
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Game")


def main():
    # Local main function variables.
    clock = pygame.time.Clock()
    FPS = 60
    run = True

    run_away = False
    font = pygame.font.SysFont('comicsans', 36)
    pygame.mixer.music.play()

    score = 0
    first_spawn = True
    wave = 1
    lost = False

    player = Player(400, 400)
    player_vel = 3
    entities = []
    entities.append(player)
    hit_player = False
    player_hit_counter = 20

    zombie_vel = 1
    zombies_more = 5
    zombies = []
    dead_zombies = []
    despawn_dead_zombies = True
    spawn_zombies = 15
    zombie_spawn_distance = 250

    to_player_damage = 50
    to_enemy_damage = 15

    ammo_boxes = []
    ammo_in_box_amount = 20
    spawn_ammo = 3
    bullets = []
    bullet_vel = 20
    shoot_cooldown = 30
    shoot_cooldown_charge = 20

    damage_cooldown_seconds = 1
    heal_charge_seconds = 3
    damage_cooldown = FPS * damage_cooldown_seconds
    heal_counter = FPS * heal_charge_seconds

    wave_cooldown = FPS * 2

    def new_wave():
        for i in range(wave_cooldown):
            draw_window(a_new_wave=True)
            pygame.display.update()

    def lost(score):
        save(score)
        player.current_img = PLAYER_DEAD
        pygame.mixer.music.stop()
        for i in range(FPS * 5):
            draw_window(lost=True)
            pygame.display.update()
        main()

    def load():
        try:
            high_score_file = open('high_score.pydata', 'rb')
            HIGH_SCORE = pickle.load(high_score_file)
            high_score_file.close()
        except Exception as e:
            print('couldn\'t load file')
            print(e)
            HIGH_SCORE = 0
        return HIGH_SCORE

    def save(HIGH_SCORE):
        try:
            high_score_file = open('high_score.pydata', 'wb')
            pickle.dump(HIGH_SCORE, high_score_file)
            high_score_file.close()
        except Exception as e:
            print('couldn\'t save file')
            print(e)

    # Everything that is either drawn/blitted to the window.
    def draw_window(hit_counter=20, a_new_wave=False, lost=False, hit_player=False,):
        WIN.blit(BG, (0, 0))
        for dead_zombie in dead_zombies[:]:
            WIN.blit(ZOMBIE_DEAD, (dead_zombie.x, dead_zombie.y))
        for bullet in bullets[:]:
            bullet.draw(WIN)
        for ammo in ammo_boxes[:]:
            ammo.draw(WIN)
        player.draw(WIN)
        for zombie in zombies[:]:
            zombie.draw(WIN)
        health_label = font.render(
            f'Health: {player.health}', 1, (214, 44, 44))
        ammo_label = font.render(f'Ammo: {player.ammo}', 1, (224, 204, 72))
        wave_label = font.render(f'Wave: {wave}', 1, (214, 204, 72))
        score_label = font.render(f'Score: {score}', 1, (0, 0, 0))
        high_score_label = font.render(
            f'High Score: {high_score}', 1, (0, 0, 0))
        WIN.blit(high_score_label, (WIDTH - 200, 50))
        WIN.blit(score_label, (WIDTH - 150, 10))
        WIN.blit(health_label, (10, 10))
        WIN.blit(ammo_label, (10, 50))
        WIN.blit(wave_label, (10, 100))
        if lost:
            game_over_label = font.render(f'GAME OVER', 1, (0, 0, 0))
            WIN.blit(PLAYER_HIT_OVERLAY, (0, 0))
            WIN.blit(game_over_label, (WIDTH // 2 - 90, HEIGHT // 2))
        if a_new_wave:
            wave_label = font.render(f'Wave: {wave}', 1, (214, 204, 72))
            WIN.blit(wave_label, (WIDTH // 2 - 100, HEIGHT // 2))

        if hit_player == True:
            hit_counter -= 1
            WIN.blit(PLAYER_HIT_OVERLAY, (0, 0))
        if hit_counter < 0:
            hit_player = False
            hit_counter = 20
        pygame.display.update()
        return hit_counter, hit_player

    def zombie_random_move():
        if zombie.x <= 0:
            zombie.randy = 0
            zombie.randd = zombie_vel
        if zombie.x >= WIDTH - zombie.get_width():
            zombie.randy = 0
            zombie.randd = -zombie_vel
        if zombie.y <= 0:
            zombie.randy = 1
            zombie.randd = zombie_vel
        if zombie.y >= HEIGHT - zombie.get_height():
            zombie.randy = 1
            zombie.randd = -zombie_vel
        if zombie.walk_count > 0:
            zombie.walk_count -= 1
            zombie.move(zombie.randy, zombie.randd)
        elif zombie.walk_count <= 0:
            zombie.randy = random.randint(0, 4)
            zombie.randd = random.choice((-zombie_vel, zombie_vel))
            zombie.walk_count += 120

    high_score = load()
    # Main game while run loop.
    while run:
        # Main clock and draw window callback function.
        clock.tick(FPS)
        player_hit_counter, hit_player = draw_window(
            hit_player=hit_player, hit_counter=player_hit_counter)
        player.update()
        player.is_moving = False
        # Zombie spawner when theres no more zombies
        if len(zombies) <= 0 and not first_spawn:
            if despawn_dead_zombies == True:
                dead_zombies = []
            spawn_zombies += zombies_more
            for zombie in range(spawn_zombies):
                on_player = True
                while on_player:
                    rand_x = random.randint(0, WIDTH - 100)
                    rand_y = random.randint(0, HEIGHT - 100)
                    if get_distance_cords(rand_x, rand_y, player.x, player.y) > zombie_spawn_distance:
                        on_player = False
                zombie = Zombie(rand_x, rand_y, health=30)
                zombies.append(zombie)
            wave += 1
            new_wave()
        if len(zombies) <= 0 and first_spawn is True:
            for zombie in range(spawn_zombies):
                on_player = True
                while on_player:
                    rand_x = random.randint(0, WIDTH - 100)
                    rand_y = random.randint(0, HEIGHT - 100)
                    if get_distance_cords(rand_x, rand_y, player.x, player.y) > 200:
                        on_player = False
                zombie = Zombie(rand_x, rand_y, health=30)
                zombies.append(zombie)
            first_spawn = False

        # Zombie movement and collide checker for each Zombie
        for index, zombie in enumerate(zombies[:]):
            for bullet in bullets[:]:
                if collide(zombie, bullet):
                    hit_random_sound = random.randint(0, 1)
                    if hit_random_sound == 0:
                        ZOMBIE_HIT_SOUND_1.play()
                    elif hit_random_sound == 1:
                        ZOMBIE_HIT_SOUND_2.play()
                    if score > high_score:
                        high_score += 1
                    zombie.health -= to_enemy_damage
                    bullets.remove(bullet)
                    if zombie.health < 20:
                        zombie.current_img = ZOMBIE_HURT
                    if zombie.health <= 0:
                        dead_zombies.append(zombie)
                        score += 1
                        zombies.remove(zombie)
            if collide(zombie, player):
                if damage_cooldown <= 0:
                    hit_player = True
                    PLAYER_HIT_SOUND_1.play()
                    player.health -= to_player_damage
                    if player.health <= 0:
                        lost(high_score)
                    damage_cooldown += FPS * damage_cooldown_seconds
                    heal_counter += FPS * heal_charge_seconds
                continue
            if get_distance(zombie, player) < 750:
                # Checks all other zombies in the list's distance from current zombie, if too close while chasing the player,
                # it will randomly walk.
                for other_zombie in zombies[:index]:
                    if get_distance(other_zombie, zombie) > 0 and get_distance(other_zombie, zombie) < 15:
                        run_away = True
                for other_zombie in zombies[index + 1:]:
                    if get_distance(other_zombie, zombie) > 0 and get_distance(other_zombie, zombie) < 15:
                        run_away = True
                if run_away == False:
                    zombie.walk_count = 0
                    zombie.attack_move(zombie_vel, player)
            # If a zombie is too close to another zombie
            if run_away == True:
                zombie_random_move()
            elif get_distance(zombie, player) > 450:
                zombie_random_move()
            run_away = False
        if damage_cooldown > 0:
            damage_cooldown -= 1

        # Creating Ammo Boxes
        if len(ammo_boxes) == 0:
            for ammo in range(spawn_ammo):
                ammo = Ammo((random.randint(AMMO.get_width(), WIDTH - AMMO.get_width())),
                            random.randint(AMMO.get_height(), HEIGHT - AMMO.get_height()))
                ammo_boxes.append(ammo)

        for ammo in ammo_boxes[:]:
            if collide(ammo, player):
                player.ammo += ammo_in_box_amount
                ammo_boxes.remove(ammo)

        # Bullet behavior
        for bullet in bullets[:]:
            if 0 < bullet.x < WIDTH and 0 < bullet.y < HEIGHT:
                bullet.move(bullet_vel)
            else:
                bullets.remove(bullet)
        # Healing
        if heal_counter == 0 and player.health < player.max_health:
            player.health += 10
            heal_counter += 30
        if heal_counter > 0:
            heal_counter -= 1

        # IMPORTANT FOR LOOP, CONTROLS WONT WORK WITHOUT IT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # This var gets list of keys, while checking to see what was pressed.
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player.y > 0:
            player.y -= player_vel
            player.direction = 'up'
            player.is_moving = True
        if keys[pygame.K_s] and player.y < HEIGHT - player.get_height():
            player.y += player_vel
            player.direction = 'down'
            player.is_moving = True
        if keys[pygame.K_a] and player.x > 0:
            player.x -= player_vel
            player.direction = 'left'
            player.is_moving = True
        if keys[pygame.K_d] and player.x < WIDTH - player.get_width():
            player.x += player_vel
            player.direction = 'right'
            player.is_moving = True
        if keys[pygame.K_w] and keys[pygame.K_d]:
            player.direction = 'up_right'
        elif keys[pygame.K_d] and keys[pygame.K_s]:
            player.direction = 'down_right'
        elif keys[pygame.K_w] and keys[pygame.K_a]:
            player.direction = 'up_left'
        elif keys[pygame.K_s] and keys[pygame.K_a]:
            player.direction = 'down_left'

        if keys[pygame.K_SPACE] and shoot_cooldown <= 0 and player.ammo > 0:
            bullet = Bullet(player.x + 20, player.y + 30, player.direction)
            bullets.append(bullet)
            GUNSHOTSOUND.play()
            player.ammo -= 1
            shoot_cooldown += shoot_cooldown_charge
        if shoot_cooldown > 0:
            shoot_cooldown -= 1

# Main function will run the game.
main()

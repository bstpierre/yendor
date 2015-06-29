#!/usr/bin/python

import sys

import pygame

from . import (
    bullet,
    coord,
    monster,
    tower,
    velocity,
    )

def main(args=None):
    """The main routine."""
    # if args is None:
    #     args = sys.argv[1:]
    # XXX - arg parsing

    WHITE = (255, 255, 255)

    size = (600, 480)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Yendor Defender")

    clock = pygame.time.Clock()

    bullets = pygame.sprite.Group()

    towers = pygame.sprite.Group()
    t = tower.Tower(bullet.Bullet)
    towers.add(t)

    monsters = pygame.sprite.Group()

    def spawn_monster():
        monsters.add(monster.Monster())

    ticks = 0

    pygame.init()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_q, pygame.K_ESCAPE]:
                    running = False
                elif event.key in [pygame.K_m]:
                    spawn_monster()
            elif event.type == pygame.MOUSEBUTTONUP:
                click = coord.Coord(event.pos[0], event.pos[1])
                bearing = t.center.bearing(click)
                print(bearing)
                v = velocity.Velocity(3, bearing)
                b = bullet.Bullet(v, t.center)
                b.rect.x = t.center.x
                b.rect.y = t.center.y
                bullets.add(b)

        ticks += 1
        bullets.update(ticks)
        monsters.update(ticks)
        towers.update(ticks)

        # Injure monsters with bullets.
        hits = pygame.sprite.groupcollide(bullets, monsters,
                                          True, False)
        for b, ms in hits.items():
            for m in ms:
                m.injure(b.damage)
                # XXX - bullet only one hits one monster
                break

        # Fire the towers.
        in_range = pygame.sprite.groupcollide(
            towers, monsters, False, False,
            collided=pygame.sprite.collide_circle)
        for t, ms in in_range.items():
            # FIXME: only check 'ready' tower group for collisions
            if not t.loaded:
                continue
            for m in ms:
                b = t.fire(m, ticks)
                bullets.add(b)
                # XXX tower only fires at one monster
                break

        # 30fps
        clock.tick(30)

        screen.fill(WHITE)
        bullets.draw(screen)
        towers.draw(screen)
        monsters.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

import pygame
import bodies

pygame.init()

def main():
    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(60)
        bodies.WINDOW.fill((0, 0, 0))

        for planet in bodies.planets:
            planet.update_position(bodies.planets)
            planet.draw(bodies.WINDOW)

        for satellite in bodies.moons:
            satellite.draw(bodies.WINDOW, satellite.planet)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()
    pygame.quit()

main()
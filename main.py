import pygame
import bodies

pygame.init()

WINDOW = pygame.display.set_mode((bodies.WIDTH, bodies.HEIGHT))
pygame.display.set_caption("The Planetary System")

def main():
    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(60)
        WINDOW.fill((0, 0, 0))

        for planet in bodies.planets:
            planet.update_position(bodies.planets)
            planet.draw(WINDOW)

        for satellite in bodies.moons:
            satellite.draw(WINDOW, satellite.planet)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()
    pygame.quit()

main()
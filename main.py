import pygame
import bodies
import shared_resources as sr

pygame.init()

WINDOW = pygame.display.set_mode((sr.WIDTH, sr.HEIGHT))
pygame.display.set_caption("The Planetary System")


def main():
    running = True
    clock = pygame.time.Clock()
    selected_body = None  # Track the currently selected body
    zoom_scale = 2  # Adjust this value to set zoom level

    while running:
        clock.tick(60)
        WINDOW.fill((0, 0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                for planet in bodies.planets + bodies.moons:
                    if (planet.curr_x - mouse_x) ** 2 + (planet.curr_y - mouse_y) ** 2 <= planet.radius ** 2:
                        selected_body = planet
                        break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    selected_body = None

        # Draw the planetary system
        if selected_body:
            for planet in bodies.planets:
                planet.update_position(bodies.planets)
                planet.draw_zoomed(WINDOW, selected_body, zoom_scale)

            for satellite in bodies.moons:
                satellite.draw_zoomed(WINDOW, satellite.planet, zoom_scale)
        else:
            for planet in bodies.planets:
                planet.update_position(bodies.planets)
                planet.draw(WINDOW)

            for satellite in bodies.moons:
                satellite.draw(WINDOW, satellite.planet)

        pygame.display.update()

    pygame.quit()


main()

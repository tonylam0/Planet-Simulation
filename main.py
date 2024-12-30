import pygame
import bodies
import shared_resources as sr
import math

pygame.init()

WINDOW = pygame.display.set_mode((sr.WIDTH, sr.HEIGHT))
pygame.display.set_caption("The Planetary System")

def event_handling(event, selected_body, key_to_body):
    if event.type == pygame.QUIT:
        return False

    elif event.type == pygame.KEYDOWN:  # Checks for key press
        if event.key in key_to_body:
            selected_body = key_to_body[event.key]

    # Checks for left mouse button
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        mouse_x, mouse_y = event.pos
        for body in bodies.planets + bodies.moons:
            # Calculates if the mouseclick is within the planet's sprite 
            # Based off of circle formula
            mouse_inside_body = (body.scaled_x - mouse_x) ** 2 + (
                body.scaled_y - mouse_y) ** 2 <= body.radius ** 2
            if mouse_inside_body and selected_body == None:
                selected_body = body
                break
            # Checks for qualifed mouseclick while already zoomed in
            elif (body.zoomed_x - mouse_x) ** 2 + (
                body.zoomed_y - mouse_y) ** 2 <= body.zoomed_radius ** 2:
                selected_body = body
                break

    return True, selected_body

def simulation_speed(keys, fps):
    if keys[pygame.K_RIGHT] and fps < 180:
        fps += .7
    elif keys[pygame.K_LEFT] and fps > 30:
        fps -= .7
    elif keys[pygame.K_SPACE]:
        fps = 60
    return fps

def display_bodies(selected_body):
    if selected_body:
        if not selected_body.moon:
            sr.zoom_scale = 2  # Less zoom-in for bigger sprites
        else:
            sr.zoom_scale = 4  # More zoom-in for smaller sprites

        # Updates all bodies before scaling to ensure correct zoom placement
        for body in bodies.planets + bodies.moons:
            if not body.moon:
                # Updates non-scaled (x, y) position
                body.update_position(bodies.planets)
            else:
                # Updates non-scaled position & planet.angle
                body.update_moon_position(selected_body, body.planet)
        
        for body in bodies.planets + bodies.moons:
            if not body.moon:
                # Updates zoomed planet position after all moons are updated
                body.update_zoomed_position(selected_body)
                body.draw_zoomed(WINDOW, selected_body)
            else:
                body.update_moon_position(selected_body, body.planet)
                body.draw_zoomed(WINDOW, selected_body, body.planet)
    else:
        sr.zoom_scale = 1
        for planet in bodies.planets:
            planet.update_position(bodies.planets)
            planet.draw(WINDOW)

        for satellite in bodies.moons:
            satellite.draw(WINDOW, satellite.planet)

def main():
    running = True
    clock = pygame.time.Clock()
    selected_body = None  # Track the currently selected body
    fps = 60  # Simulation speed

    key_to_body = {  # Certain keybinds are set to certain planets
    pygame.K_r: None,
    pygame.K_1: bodies.sun,
    pygame.K_2: bodies.mercury,
    pygame.K_3: bodies.venus,
    pygame.K_4: bodies.earth,
    pygame.K_5: bodies.mars,
    pygame.K_6: bodies.moon,
    pygame.K_7: bodies.phobos,
    pygame.K_8: bodies.deimos,
    }

    while running:
        clock.tick(fps)
        WINDOW.fill((0, 0, 0))

        for event in pygame.event.get():
            running, selected_body = event_handling(event, selected_body, key_to_body)

        keys = pygame.key.get_pressed()
        fps = simulation_speed(keys, fps)
        
        display_bodies(selected_body)

        pygame.display.update()

    pygame.quit()

main()
import pygame
import bodies
import shared_resources as sr


pygame.init()
pygame.font.init()
text_font = pygame.font.SysFont("verdana", 10)

WINDOW = pygame.display.set_mode((sr.WIDTH, sr.HEIGHT))
pygame.display.set_caption("The Planetary System")

def event_handling(event, selected_body, key_to_body, hide):
    if event.type == pygame.QUIT:
        return False, selected_body, hide

    elif event.type == pygame.KEYDOWN:  # Checks for key press
        if event.key in key_to_body:
            selected_body = key_to_body[event.key]
        elif event.key == pygame.K_h and hide:
            hide = False
        elif event.key == pygame.K_h and not hide:
            hide = True

    # Checks for left mouse button
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        mouse_x, mouse_y = event.pos
        for body in bodies.planets + bodies.moons:
            # Calculates if the mouseclick is within the planet's sprite 
            # Based off of circle formula
            mouse_inside_body = (body.scaled_x - mouse_x) ** 2 + (
                body.scaled_y - mouse_y) ** 2 <= body.radius ** 2
            if mouse_inside_body and selected_body is None:
                selected_body = body
                break
            # Checks for qualifed mouseclick while already zoomed in
            elif (body.zoomed_x - mouse_x) ** 2 + (
                body.zoomed_y - mouse_y) ** 2 <= body.zoomed_radius ** 2:
                selected_body = body
                break

    return True, selected_body, hide

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

def body_name(selected_body, hide):  # Displays name of body when zoomed in
    if selected_body and not hide:
        if not selected_body.sun:
            font_size = 20
        else:
            font_size = 25

        object_font = pygame.font.SysFont("verdana", font_size)
        body_text = object_font.render(selected_body.name, True, selected_body.color)

        if not selected_body.sun:
            WINDOW.blit(body_text, 
                (sr.WIDTH / 2, sr.HEIGHT / 2 + selected_body.zoomed_radius))
        else:
            WINDOW.blit(body_text, 
                (sr.WIDTH / 2, sr.HEIGHT / 2 + selected_body.radius))
            
def simulation_text(fps):
    speed_font = pygame.font.SysFont("verdana", 15)
    speed = round(fps / 60, 1)
    speed_text = speed_font.render(f"SPEED: {str(speed)}x", True, (255, 255, 255))
    text_rect = speed_text.get_rect()
    text_rect.bottomright = (sr.WIDTH - 10, sr.HEIGHT - 10)
    WINDOW.blit(speed_text, text_rect)

def main():
    running = True
    clock = pygame.time.Clock()
    selected_body = None  # Track the currently selected body
    fps = 60  # Simulation speed
    hide = True  # Used to display zoomed-in planet/moon name

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

    camera_text = text_font.render(
                "PRESS 1 - 8 TO VIEW DIFFERENT CAMERAS OR CLICK CELESTIAL BODY",
                True, (255, 255, 255))
    speed_text = text_font.render(
                "LEFT ARROW TO SLOW DOWN | RIGHT ARROW TO SPEED UP | SPACE TO RESET SPEED",
                True, (255, 255, 255))
    hide_text = text_font.render(
                "PRESS h to HIDE/UNHIDE ZOOMED IN PLANET/MOON NAME",
                True, (255, 255, 255))

    while running:
        clock.tick(fps)
        WINDOW.fill((0, 0, 0))

        for event in pygame.event.get():
            running, selected_body, hide = event_handling(event, selected_body, key_to_body, hide)

        keys = pygame.key.get_pressed()
        fps = simulation_speed(keys, fps)
        
        display_bodies(selected_body)

        simulation_text(fps)

        body_name(selected_body, hide)

        # # Uncomment to display keybind controls
        # WINDOW.blit(hide_text, (10, sr.HEIGHT - 44))
        # WINDOW.blit(camera_text, (10, sr.HEIGHT - 33))
        # WINDOW.blit(speed_text, (10, sr.HEIGHT - 22))

        pygame.display.update()

    pygame.quit()

main()
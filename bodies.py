import pygame
import math
import sprites
import shared_resources as sr

WHITE = (255, 255, 255)
YELLOW = (249, 215, 28)
LIGHT_GRAY = (169, 169, 169)
PALE_YELLOW = (255, 233, 186)
BLUE = (0, 102, 204)
RED = (188, 39, 50)
OFF_WHITE = (190, 190, 190)
REDDISH_GRAY = (150, 100, 100)

class Planet(pygame.sprite.Sprite):
    AU = 149.6e6 * 1000  # Average distance from Earth to the Sun in meters
    G = 6.67428e-11  # Graviational constant = calculates gravitional force
    SCALE = 250 / AU  # 1 AU = 100 pixels
    TIMESTEP = 3600*24  # 1 day elapsed

    def __init__(self, x, y, radius, color, mass, year_to_days, sprite, revolution):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass  # In kilograms
        self.curr_x = 0
        self.curr_y = 0

        self.orbit = []
        self.sun = False
        self.moon = False
        self.distance_to_sun = 0
        self.earth = False

        self.x_vel = 0
        self.y_vel = 0

        self.sprites = sprite
        self.current_sprite = 0
        self.angle = 0
        self.year_to_days = year_to_days
        self.revolution = revolution  # Shows whether initial x coordinate was flipped or not
        self.opp_quadrant_flag = False  # Checks if planet has reached opposite planal quadrant
        self.revolution_complete = False  # Checks if a revolution has been complete

    def draw(self, win):
        # Adjusts planet size & position to fit screen from the center
        self.curr_x = self.x * Planet.SCALE + sr.WIDTH / 2
        self.curr_y = self.y * Planet.SCALE + sr.HEIGHT / 2
        
        GLOW_SURFACE = pygame.Surface((sr.WIDTH, sr.HEIGHT), pygame.SRCALPHA)
        if self.sun:
            # Glow effect: applying multiple smaller but more opaque circles on top of each other
            for i in range(0, self.radius + 1):
                fade = int(50 * (i / self.radius))  # Opacity starts off small
                pygame.draw.circle(GLOW_SURFACE, (*self.color, fade), (self.curr_x, self.curr_y), 1.05 * self.radius - i)  # Radius starts off large
            win.blit(GLOW_SURFACE, (0,0))

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + sr.WIDTH / 2
                y = y * self.SCALE + sr.HEIGHT / 2
                updated_points.append((x, y))
            
            pygame.draw.lines(win, self.color, False, updated_points, 1)

        # Gives an index & when index hits length of sprites list, index resets
        # higher number value = higher rotation speed
        self.current_sprite = (self.current_sprite + .15) % len(self.sprites)
        self.angle += 360 / self.year_to_days  # Degree per simulated day

        # Used to calculate planet quadrant
        cross_horizon_x = sr.WIDTH - self.curr_x
        cross_horizon_y = sr.HEIGHT - self.curr_y
        
        # Based on which quadrant the planet is in, the angle will reset
        if self.revolution:
            if cross_horizon_x > sr.WIDTH / 2 and cross_horizon_y > sr.HEIGHT / 2: 
                self.opp_quadrant_flag = True
            if self.opp_quadrant_flag and cross_horizon_y < sr.HEIGHT / 2:
                self.angle = 0
                self.opp_quadrant_flag = False
                self.revolution_complete = True
        else:
            if cross_horizon_x < sr.WIDTH / 2 and cross_horizon_y < sr.HEIGHT / 2:
                self.opp_quadrant_flag = True
            if self.opp_quadrant_flag and cross_horizon_y > sr.HEIGHT / 2:
                self.angle = 0
                self.opp_quadrant_flag = False
                self.revolution_complete = True

        planet_sprite = pygame.transform.rotate(self.sprites[int(self.current_sprite)], int(self.angle))
        draw_at_center(win, planet_sprite, self.curr_x, self.curr_y)

    def attraction(self, other):  # Calculate Newton's law of universal gravitation 
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x  # Represents r in newton's equation
        distance_y = other_y - self.y
        radius = math.sqrt(distance_x**2 + distance_y**2)  # Can exclude the sqrt because the equation requires r^2 anyways

        if other.sun:
            self.distance_to_sun = radius
        
        force = self.G * self.mass * other.mass / radius**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y
    
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * Planet.TIMESTEP  # Derives from Newton's law of motion
        self.y_vel += total_fy / self.mass * Planet.TIMESTEP

        self.x += self.x_vel * Planet.TIMESTEP  # Current position + displacement
        self.y += self.y_vel * Planet.TIMESTEP

        if self.revolution_complete:
            self.orbit.pop(0)
        self.orbit.append((self.x, self.y))  # Collection of positions to represent orbit path

    def draw_to_body(self, win, body):  # Draws line from one body to another
        pygame.draw.line(win, WHITE, (body.curr_x, body.curr_y), (self.curr_x, self.curr_y))

    def draw_zoomed(self, win, focus_body, zoom_scale):
        # Adjust position and size for zoom
        self.zoomed_x = sr.WIDTH / 2 + (self.x - focus_body.x) * Planet.SCALE * zoom_scale
        self.zoomed_y = sr.HEIGHT / 2 + (self.y - focus_body.y) * Planet.SCALE * zoom_scale
        self.zoomed_radius = self.radius * zoom_scale

        GLOW_SURFACE = pygame.Surface((sr.WIDTH, sr.HEIGHT), pygame.SRCALPHA)
        if self.sun:
            # Glow effect: applying multiple smaller but more opaque circles on top of each other
            for i in range(0, self.radius + 1):
                fade = int(50 * (i / self.radius))  # Opacity starts off small
                pygame.draw.circle(GLOW_SURFACE, (*self.color, fade), (self.zoomed_x, self.zoomed_y), 1.05 * self.zoomed_radius - i)  # Radius starts off large
            win.blit(GLOW_SURFACE, (0,0))

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = sr.WIDTH / 2 + (x - focus_body.x) * Planet.SCALE * zoom_scale
                y = sr.HEIGHT / 2 + (y - focus_body.y) * Planet.SCALE * zoom_scale
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        self.current_sprite = (self.current_sprite + .15) % len(self.sprites)
        self.angle += 360 / self.year_to_days  # Degree per simulated day

        # Used to calculate planet quadrant
        cross_horizon_x = sr.WIDTH - self.x
        cross_horizon_y = sr.HEIGHT - self.y
        
        # Based on which quadrant the planet is in, the angle will reset
        if self.revolution:
            if cross_horizon_x > sr.WIDTH / 2 and cross_horizon_y > sr.HEIGHT / 2: 
                self.opp_quadrant_flag = True
            if self.opp_quadrant_flag and cross_horizon_y < sr.HEIGHT / 2:
                self.angle = 0
                self.opp_quadrant_flag = False
                self.revolution_complete = True
        else:
            if cross_horizon_x < sr.WIDTH / 2 and cross_horizon_y < sr.HEIGHT / 2:
                self.opp_quadrant_flag = True
            if self.opp_quadrant_flag and cross_horizon_y > sr.HEIGHT / 2:
                self.angle = 0
                self.opp_quadrant_flag = False
                self.revolution_complete = True

        planet_sprite = pygame.transform.scale(self.sprites[int(self.current_sprite)], (2 * int(self.zoomed_radius), 2 * int(self.zoomed_radius)))
        planet_sprite = pygame.transform.rotate(planet_sprite, int(self.angle))
        draw_at_center(win, planet_sprite, self.zoomed_x, self.zoomed_y)


class Moon(Planet):
    def __init__(self, x, y, radius, color, mass, year_to_days, sprite, revolution, orbit_speed, planet, distance_to_planet, angle):
        super().__init__(x, y, radius, color, mass, year_to_days, sprite, revolution)
        self.orbit = []
        self.angle = angle
        self.orbit_speed = orbit_speed
        self.planet = planet
        self.distance_to_planet = distance_to_planet

    def draw(self, win, planet):
        self.angle -= self.orbit_speed  # Increasing value increases the speed of moon revolution
        self.curr_x = planet.curr_x + (self.distance_to_planet * math.cos(self.angle))  # Adjusts moon's position based on planet
        self.curr_y = planet.curr_y + (self.distance_to_planet * math.sin(self.angle))

        # self.orbit.append((self.curr_x, self.curr_y))  # Uncomment if you want to draw the orbit of the moon
        # if len(self.orbit) > 2:
        #     pygame.draw.lines(win, self.color, False, self.orbit, 1)

        self.current_sprite = (self.current_sprite + .15) % len(self.sprites)
        moon_sprite = pygame.transform.scale(self.sprites[int(self.current_sprite)], (2*self.radius, 2*self.radius))
        moon_sprite = pygame.transform.rotate(moon_sprite, int(planet.angle))
        draw_at_center(win, moon_sprite, self.curr_x, self.curr_y)

    def draw_zoomed(self, win, planet, zoom_scale):
        self.angle -= self.orbit_speed
        self.curr_x = planet.zoomed_x + (self.distance_to_planet * math.cos(self.angle)) * zoom_scale
        self.curr_y = planet.zoomed_y + (self.distance_to_planet * math.sin(self.angle)) * zoom_scale
        zoomed_radius = self.radius * zoom_scale

        self.current_sprite = (self.current_sprite + .15) % len(self.sprites)
        moon_sprite = pygame.transform.scale(self.sprites[int(self.current_sprite)], (2 * int(zoomed_radius), 2 * int(zoomed_radius)))
        moon_sprite = pygame.transform.rotate(moon_sprite, int(planet.angle))
        draw_at_center(win, moon_sprite, self.curr_x, self.curr_y)


def draw_at_center(win, image, x, y):  # Centers the image being placed on screen
    image_rect = image.get_rect(center=(x, y))
    win.blit(image, image_rect.topleft)

sun = Planet(0, 0, sr.sun_radius, YELLOW, 1.9882 * 10**30, 365, sprites.sun_sprites, True)
sun.sun = True

mercury = Planet(1 * 0.4*Planet.AU, 0, sr.mercury_radius, LIGHT_GRAY, 3.3 * 10**2, 87.969, sprites.mercury_sprites, False)
mercury.y_vel = -47.4 * 1000

venus = Planet(1 * 0.72*Planet.AU, 0, sr.venus_radius, PALE_YELLOW, 4.8675 * 10**24, 225, sprites.venus_sprites, False)
venus.y_vel = -35.02 * 1000

earth = Planet(-1 * Planet.AU, 0, sr.earth_radius, BLUE, 5.9742 * 10**24, 365.242374, sprites.earth_sprites, True)
earth.y_vel = 29.793 * 1000
earth.earth = True

mars = Planet(-1 * 1.5*Planet.AU, 0, sr.mars_radius, RED, 6.4171 * 10**23, 687, sprites.mars_sprites, True)
mars.y_vel = 24.077 * 1000

moon = Moon(earth.x + 0.00257 * Planet.AU, 0, sr.moon_radius, OFF_WHITE, 7.34767309 * 10**22, earth.year_to_days, sprites.moon_sprites, True, .069, earth, 30, 0)
moon.moon = True

phobos = Moon(mars.x + 0.00257 * Planet.AU, 0, sr.phobos_radius, LIGHT_GRAY, 1.060 * 10**16, mars.year_to_days, sprites.phobos_sprites, True, .069, mars, 13, 0)
phobos.moon = True

deimos = Moon(mars.x + 0.00257 * Planet.AU, 0, sr.deimos_radius, REDDISH_GRAY, 1.5 * 10**15, mars.year_to_days, sprites.deimos_sprites, True, .05175, mars, 20, 5)

planets = [sun, mercury, venus, earth, mars]
moons = [moon, phobos, deimos]
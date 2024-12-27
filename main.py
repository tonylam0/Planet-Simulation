import pygame
import math
import sprites

pygame.init()

WIDTH, HEIGHT = 800, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Planetary System")

# colors
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
        self.revolution_flag = False

    def draw(self, win):
        self.curr_x = self.x * Planet.SCALE + WIDTH / 2  # Adjusts planet position from the center of the screen
        self.curr_y = self.y * Planet.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))
            
            pygame.draw.lines(win, self.color, False, updated_points, 1)
        
        GLOW_SURFACE = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        if self.sun:
            # Glow effect: applying multiple smaller but more opaque circles on top of each other
            for i in range(0, self.radius + 1):
                fade = int(50 * (i / self.radius))  # Opacity starts off small
                pygame.draw.circle(GLOW_SURFACE, (*self.color, fade), (self.curr_x, self.curr_y), 1.05 * self.radius - i)  # Radius starts off large

            WINDOW.blit(GLOW_SURFACE, (0,0))

        # Gives an index & when index hits length of sprites list, index resets
        self.current_sprite = (self.current_sprite + .15) % len(self.sprites)
        self.angle += 360 / self.year_to_days  # Degree per simulated day

        # Used to calculate planet quadrant
        cross_horizon_x = WIDTH - self.curr_x
        cross_horizon_y = HEIGHT - self.curr_y
        
        # Based on which quadrant planet is in, the angle will reset
        if self.revolution:
            if cross_horizon_x > WIDTH / 2 and cross_horizon_y > HEIGHT / 2: 
                self.revolution_flag = True
            if self.revolution_flag and cross_horizon_y < HEIGHT / 2:
                self.angle = 0
                self.revolution_flag = False
        else:
            if cross_horizon_x < WIDTH / 2 and cross_horizon_y < HEIGHT / 2:
                self.revolution_flag = True
            if self.revolution_flag and cross_horizon_y > HEIGHT / 2:
                self.angle = 0
                self.revolution_flag = False

        planet_sprite = pygame.transform.scale(self.sprites[int(self.current_sprite)], (2*self.radius, 2*self.radius))
        planet_sprite = pygame.transform.rotate(planet_sprite, int(self.angle))
        draw_at_center(WINDOW, planet_sprite, self.curr_x, self.curr_y)

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
        self.orbit.append((self.x, self.y))  # Collection of positions to represent orbit path

    def draw_to_body(self, body): # Draws line from one body to another
        pygame.draw.line(WINDOW, WHITE, (body.curr_x, body.curr_y), (self.curr_x, self.curr_y))


class Moon(Planet):
    def __init__(self, x, y, radius, color, mass, year_to_days, sprite, revolution, orbit_speed, planet, distance_to_planet, angle):
        super().__init__(x, y, radius, color, mass, year_to_days, sprite, revolution)
        self.orbit = []
        self.angle = angle
        self.orbit_speed = orbit_speed
        self.planet = planet
        self.distance_to_planet = distance_to_planet

    def draw(self, win, planet):
        self.angle -= self.orbit_speed # Increasing value increases the speed of moon revolution
        self.curr_x = planet.curr_x + (self.distance_to_planet * math.cos(self.angle)) # Adjusts moon's position based on planet
        self.curr_y = planet.curr_y + (self.distance_to_planet * math.sin(self.angle))

        # self.orbit.append((self.x, self.y)) # Uncomment if you want to draw the orbit of the moon

        if len(self.orbit) > 2:
            pygame.draw.lines(win, self.color, False, self.orbit, 1)
        pygame.draw.circle(win, self.color, (self.curr_x, self.curr_y), self.radius)


def draw_at_center(win, image, x, y): # Centers the image being placed on screen
    image_rect = image.get_rect(center=(x, y))
    win.blit(image, image_rect.topleft)

def main():
    running = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 100, YELLOW, 1.9882 * 10**30, 365, sprites.sun_sprites, True)
    sun.sun = True

    mercury = Planet(1 * 0.4*Planet.AU, 0, 6, LIGHT_GRAY, 3.3 * 10**2, 88, sprites.mercury_sprites, False)
    mercury.y_vel = -47.4 * 1000
    
    venus = Planet(1 * 0.72*Planet.AU, 0, 13, PALE_YELLOW, 4.8675 * 10**24, 225, sprites.venus_sprites, False)
    venus.y_vel = -35.02 * 1000

    earth = Planet(-1 * Planet.AU, 0, 18, BLUE, 5.9742 * 10**24, 365.242374, sprites.earth_sprites, True)
    earth.y_vel = 29.793 * 1000
    earth.earth = True

    mars = Planet(-1 * 1.5*Planet.AU, 0, 9, RED, 6.4171 * 10**23, 687, sprites.mars_sprites, True)
    mars.y_vel = 24.077 * 1000

    # moon = Moon(earth.x + 0.00257 * Planet.AU, 0, (18/4), OFF_WHITE, 7.34767309 * 10**22, None, None, .069, earth, 30, 0)
    # moon.moon = True

    # phobos = Moon(mars.x + 0.00257 * Planet.AU, 0, 3, LIGHT_GRAY, 1.060 * 10**16, None, None, .069, mars, 13, 0)
    # phobos.moon = True

    # deimos = Moon(mars.x + 0.00257 * Planet.AU, 0, 3, REDDISH_GRAY, 1.5 * 10**15, None, None, .05175, mars, 20, 5)

    planets = [sun, mercury, venus, earth, mars]
    # moons = [moon, phobos, deimos]

    while running:
        clock.tick(60)
        WINDOW.fill((0, 0, 0))

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WINDOW)

        # for satellite in moons:
            # satellite.draw(WINDOW, satellite.planet)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()
    pygame.quit()

main()
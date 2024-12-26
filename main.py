import pygame
import math
import numpy as np

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


class Planet:
    AU = 149.6e6 * 1000  # average distance from Earth to the Sun in meters
    G = 6.67428e-11  # graviational constant = calculates gravitional force
    SCALE = 250 / AU  # 1 AU = 100 pixels
    TIMESTEP = 3600*24  # 1 day elapsed

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass  # in kilograms
        self.curr_x = 0
        self.curr_y = 0

        self.orbit = []
        self.sun = False
        self.moon = False
        self.distance_to_sun = 0
        self.earth = False

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        self.curr_x = self.x * Planet.SCALE + WIDTH / 2  # adjusts planet position from the center of the screen
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

        for i in range(0, self.radius + 1):
            fade = int(255 * (i / self.radius))
            pygame.draw.circle(GLOW_SURFACE, (*self.color, fade), (self.curr_x, self.curr_y), 2 * self.radius - i) # add glow

        WINDOW.blit(GLOW_SURFACE, (0,0))
        
        pygame.draw.circle(win, self.color, (self.curr_x, self.curr_y), self.radius) 

    def attraction(self, other):  # calculate Newton's law of universal gravitation 
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x  # represents r in newton's equation
        distance_y = other_y - self.y
        radius = math.sqrt(distance_x**2 + distance_y**2)  # can exclude the sqrt because the equation requires r^2 anyways

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

        self.x_vel += total_fx / self.mass * Planet.TIMESTEP  # derives from Newton's law of motion
        self.y_vel += total_fy / self.mass * Planet.TIMESTEP

        self.x += self.x_vel * Planet.TIMESTEP  # current position + displacement
        self.y += self.y_vel * Planet.TIMESTEP
        self.orbit.append((self.x, self.y))  # collection of positions to represent orbit path

class Moon(Planet):
    def __init__(self, x, y, radius, color, mass):
        super().__init__(x, y, radius, color, mass)
        self.orbit = []
        self.angle = 0

    def draw(self, win, planet):
        self.angle -= .069 # increasing value increases the speed of moon revolution
        self.x = planet.curr_x + (25 * math.cos(self.angle)) # adjusts moon's position based on planet
        self.y = planet.curr_y + (25 * math.sin(self.angle))

        # self.orbit.append((self.x, self.y)) # if you want to draw the orbit of the moon

        if len(self.orbit) > 2:
            pygame.draw.lines(win, self.color, False, self.orbit, 1)
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class Glow:
    def __init__(self):
        pass

def main():
    running = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 50, YELLOW, 1.9882 * 10**30)
    sun.sun = True

    mercury = Planet(1 * 0.4*Planet.AU, 0, 6, LIGHT_GRAY, 3.3 * 10**23)
    mercury.y_vel = -47.4 * 1000
    
    venus = Planet(1 * 0.72*Planet.AU, 0, 13, PALE_YELLOW, 4.8675 * 10**24)
    venus.y_vel = -35.02 * 1000

    earth = Planet(-1 * Planet.AU, 0, 18, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.793 * 1000
    earth.earth = True

    mars = Planet(-1 * 1.5*Planet.AU, 0, 9, RED, 6.4171 * 10**23)
    mars.y_vel = 24.077 * 1000

    moon = Moon(earth.x + 0.00257 * Planet.AU, 0, (18/4), OFF_WHITE, 7.34767309 * 10**22)
    moon.moon = True

    planets = [sun, mercury, venus, earth, mars]

    while running:
        clock.tick(60)
        WINDOW.fill((0, 0, 0))

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WINDOW)

        moon.draw(WINDOW, earth)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()
    pygame.quit()

main()

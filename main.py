import pygame
import math

pygame.init()

WIDTH, HEIGHT = 700, 700
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
    SCALE = 225 / AU  # 1 AU = 100 pixels
    TIMESTEP = 3600*24  # 1 day elapsed


    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass  # in kilograms

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * Planet.SCALE + WIDTH / 2  # adjusts planet position from the center of the screen
        y = self.y * Planet.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))
            
            pygame.draw.lines(WINDOW, self.color, False, updated_points, 1)
        pygame.draw.circle(win, self.color, (x, y), self.radius) 

    def attraction(self, other):  # calculate Newton's law of universal gravition 
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
 

def main():
    running = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 50, YELLOW, 1.9882 * 10**30)
    sun.sun = True

    mercury = Planet(1 * 0.4*Planet.AU, 0, 6, LIGHT_GRAY, 3.3 * 10**23)
    mercury.y_vel = -47.4 * 1000
    
    venus = Planet(1 * 0.72*Planet.AU, 0, 15, PALE_YELLOW, 4.8675 * 10**24)
    venus.y_vel = -35.02 * 1000

    earth = Planet(-1 * Planet.AU, 0, 18, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.793 * 1000

    mars = Planet(-1 * 1.5*Planet.AU, 0, 9, RED, 6.4171 * 10**23)
    mars.y_vel = 24.077 * 1000


    planets = [sun, mercury, venus, earth, mars]

    while running:
        clock.tick(60)
        WINDOW.fill((0, 0, 0))

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WINDOW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()
    pygame.quit()

main()

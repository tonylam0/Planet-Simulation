# Variables shared between files to prevent circular importing

WIDTH, HEIGHT = 1000, 800  # Width & height of window

zoom_scale = 1  # Used for zoom-ins

# Based on zoom_scale, radii largen
sun_radius = 100 * zoom_scale
mercury_radius = 6 * zoom_scale
venus_radius = 13 * zoom_scale
earth_radius = 18 * zoom_scale
mars_radius = 9 * zoom_scale
moon_radius = 18/4 * zoom_scale
phobos_radius = 3 * zoom_scale
deimos_radius = 3 * zoom_scale
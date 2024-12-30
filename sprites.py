import pygame
import shared_resources as sr


def cut_spritesheet(image, sprite_num):
    image_width = image.get_width()
    sprite_lst = []
    sprite_width = image_width // sprite_num

    for sprite_x in range(0, image_width, sprite_width):
        sprite_lst.append(image.subsurface(pygame.Rect(sprite_x, 0, sprite_width, 100)))
    return sprite_lst

def flip_sprites(sprites):  # For the planets that have a flipped initial position
    sprite_lst = []
    for sprite in sprites:
        curr_sprite = pygame.transform.flip(sprite, True, True)
        sprite_lst.append(curr_sprite)
    return sprite_lst

def resize_sprites(sprite_lst, planet_radius):  # Resizes sprites to fit planet size
    new_sprite_lst = []
    for sprite in sprite_lst:
        sprite = pygame.transform.scale(sprite, (2*planet_radius, 2*planet_radius))
        new_sprite_lst.append(sprite)
    return new_sprite_lst

sp_directory = "./Planet Sprites/"

sun_sprites = resize_sprites([
    pygame.image.load(sp_directory + "Sun Sprites/sun_sp1.png"), 
    pygame.image.load(sp_directory + "Sun Sprites/sun_sp2.png"), 
    pygame.image.load(sp_directory + "Sun Sprites/sun_sp3.png"), 
    pygame.image.load(sp_directory + "Sun Sprites/sun_sp4.png"), 
    pygame.image.load(sp_directory + "Sun Sprites/sun_sp4.png"), 
    pygame.image.load(sp_directory + "Sun Sprites/sun_sp5.png"), 
    pygame.image.load(sp_directory + "Sun Sprites/sun_sp6.png"), 
    pygame.image.load(sp_directory + "Sun Sprites/sun_sp7.png")], sr.sun_radius)

mercury_sprites = flip_sprites(resize_sprites(cut_spritesheet(
    pygame.image.load(sp_directory + "Mercury Sprites.png"), 30), sr.mercury_radius))

venus_sprites = flip_sprites(resize_sprites(cut_spritesheet(
    pygame.image.load(sp_directory + "Venus Sprites.png"), 15), sr.venus_radius))

earth_sprites = resize_sprites(cut_spritesheet(
    pygame.image.load(sp_directory + "Earth Sprites.png"), 30), sr.earth_radius)

moon_sprites = resize_sprites(cut_spritesheet(
    pygame.image.load(sp_directory + "Mercury Sprites.png"), 30), sr.moon_radius)

mars_sprites = resize_sprites(cut_spritesheet(
    pygame.image.load(sp_directory + "Mars Sprites.png"), 30), sr.mars_radius)
    
phobos_sprites = resize_sprites(cut_spritesheet(
    pygame.image.load(sp_directory + "Phobos Sprites.png"), 15), sr.phobos_radius)

deimos_sprites = resize_sprites(cut_spritesheet(
    pygame.image.load(sp_directory + "Deimos Sprites.png"), 15), sr.deimos_radius)
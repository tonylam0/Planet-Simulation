import pygame

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

sun_sprites = [
    pygame.image.load("./Planet Skins/Sun Sprites/sun_sp1.png"), 
    pygame.image.load("./Planet Skins/Sun Sprites/sun_sp2.png"), 
    pygame.image.load("./Planet Skins/Sun Sprites/sun_sp3.png"), 
    pygame.image.load("./Planet Skins/Sun Sprites/sun_sp4.png"), 
    pygame.image.load("./Planet Skins/Sun Sprites/sun_sp4.png"), 
    pygame.image.load("./Planet Skins/Sun Sprites/sun_sp5.png"), 
    pygame.image.load("./Planet Skins/Sun Sprites/sun_sp6.png"), 
    pygame.image.load("./Planet Skins/Sun Sprites/sun_sp7.png"), 
]

sp_directory = "./Planet Skins/"

earth_sprites = cut_spritesheet(pygame.image.load(sp_directory + "Earth Sprites.png"), 30)

mercury_sprites = flip_sprites(cut_spritesheet(pygame.image.load(sp_directory + "Mercury Sprites.png"), 30))

venus_sprites = flip_sprites(cut_spritesheet(pygame.image.load(sp_directory + "Venus Sprites.png"), 15))

mars_sprites = cut_spritesheet(pygame.image.load(sp_directory + "Mars Sprites.png"), 30)
    
phobos_sprites = [
    pygame.transform.scale(pygame.image.load("./Planet Skins/Phobos Sprites/phobos_sp1.png"), (50, 50)),
    pygame.image.load("./Planet Skins/Phobos Sprites/phobos_sp2.png"),    
    pygame.image.load("./Planet Skins/Phobos Sprites/phobos_sp3.png"),    
    pygame.image.load("./Planet Skins/Phobos Sprites/phobos_sp4.png"),    
    pygame.image.load("./Planet Skins/Phobos Sprites/phobos_sp5.png"),    
    pygame.image.load("./Planet Skins/Phobos Sprites/phobos_sp6.png"),    
    pygame.image.load("./Planet Skins/Phobos Sprites/phobos_sp7.png"),    
    pygame.image.load("./Planet Skins/Phobos Sprites/phobos_sp8.png"),    
    pygame.image.load("./Planet Skins/Phobos Sprites/phobos_sp9.png"),    
    pygame.image.load("./Planet Skins/Phobos Sprites/phobos_sp10.png"),    
    pygame.image.load("./Planet Skins/Phobos Sprites/phobos_sp11.png"),    
    pygame.image.load("./Planet Skins/Phobos Sprites/phobos_sp12.png"),    
    pygame.image.load("./Planet Skins/Phobos Sprites/phobos_sp13.png"),    
    pygame.image.load("./Planet Skins/Phobos Sprites/phobos_sp14.png"),    
    pygame.image.load("./Planet Skins/Phobos Sprites/phobos_sp15.png")  
]

deimos_sprites = [
    pygame.image.load("./Planet Skins/Deimos Sprites/deimos_sp1.png"),
    pygame.image.load("./Planet Skins/Deimos Sprites/deimos_sp2.png"),
    pygame.image.load("./Planet Skins/Deimos Sprites/deimos_sp3.png"),
    pygame.image.load("./Planet Skins/Deimos Sprites/deimos_sp4.png"),
    pygame.image.load("./Planet Skins/Deimos Sprites/deimos_sp5.png"),
    pygame.image.load("./Planet Skins/Deimos Sprites/deimos_sp6.png"),
    pygame.image.load("./Planet Skins/Deimos Sprites/deimos_sp7.png"),
    pygame.image.load("./Planet Skins/Deimos Sprites/deimos_sp8.png"),
    pygame.image.load("./Planet Skins/Deimos Sprites/deimos_sp9.png"),
    pygame.image.load("./Planet Skins/Deimos Sprites/deimos_sp10.png"),
    pygame.image.load("./Planet Skins/Deimos Sprites/deimos_sp11.png"),
    pygame.image.load("./Planet Skins/Deimos Sprites/deimos_sp12.png"),
    pygame.image.load("./Planet Skins/Deimos Sprites/deimos_sp13.png"),
    pygame.image.load("./Planet Skins/Deimos Sprites/deimos_sp14.png"),
    pygame.image.load("./Planet Skins/Deimos Sprites/deimos_sp15.png"),
]



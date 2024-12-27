import pygame

def cut_spritesheet(image, sprite_num):
    image_width = image.get_width()
    sprite_lst = []
    sprite_width = image_width // sprite_num

    for sprite_x in range(0, image_width, sprite_width):
        sprite_lst.append(image.subsurface(pygame.Rect(sprite_x, 0, sprite_width, 100)))
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

earth_sprites = cut_spritesheet(pygame.image.load("./Planet Skins/Earth Sprites.png"), 30)

mercury_sprites = [ # Have to flip mercury sprite because intial x position is flipped
    pygame.transform.flip(pygame.image.load("./Planet Skins/Mercury Sprites/mercury_sp1.png"), True, True), 
    pygame.transform.flip(pygame.image.load("./Planet Skins/Mercury Sprites/mercury_sp2.png"), True, True), 
    pygame.transform.flip(pygame.image.load("./Planet Skins/Mercury Sprites/mercury_sp3.png"), True, True), 
    pygame.transform.flip(pygame.image.load("./Planet Skins/Mercury Sprites/mercury_sp4.png"), True, True), 
    pygame.transform.flip(pygame.image.load("./Planet Skins/Mercury Sprites/mercury_sp5.png"), True, True), 
    pygame.transform.flip(pygame.image.load("./Planet Skins/Mercury Sprites/mercury_sp6.png"), True, True), 
    pygame.transform.flip(pygame.image.load("./Planet Skins/Mercury Sprites/mercury_sp7.png"), True, True), 
    pygame.transform.flip(pygame.image.load("./Planet Skins/Mercury Sprites/mercury_sp8.png"), True, True), 
    pygame.transform.flip(pygame.image.load("./Planet Skins/Mercury Sprites/mercury_sp9.png"), True, True), 
    pygame.transform.flip(pygame.image.load("./Planet Skins/Mercury Sprites/mercury_sp10.png"), True, True), 
    pygame.transform.flip(pygame.image.load("./Planet Skins/Mercury Sprites/mercury_sp11.png"), True, True), 
    pygame.transform.flip(pygame.image.load("./Planet Skins/Mercury Sprites/mercury_sp12.png"), True, True), 
    pygame.transform.flip(pygame.image.load("./Planet Skins/Mercury Sprites/mercury_sp13.png"), True, True), 
    pygame.transform.flip(pygame.image.load("./Planet Skins/Mercury Sprites/mercury_sp14.png"), True, True), 
    pygame.transform.flip(pygame.image.load("./Planet Skins/Mercury Sprites/mercury_sp15.png"), True, True), 
    pygame.transform.flip(pygame.image.load("./Planet Skins/Mercury Sprites/mercury_sp16.png"), True, True), 
    pygame.transform.flip(pygame.image.load("./Planet Skins/Mercury Sprites/mercury_sp17.png"), True, True), 
    pygame.transform.flip(pygame.image.load("./Planet Skins/Mercury Sprites/mercury_sp18.png"), True, True), 
    pygame.transform.flip(pygame.image.load("./Planet Skins/Mercury Sprites/mercury_sp19.png"), True, True), 
    pygame.transform.flip(pygame.image.load("./Planet Skins/Mercury Sprites/mercury_sp20.png"), True, True), 
    pygame.transform.flip(pygame.image.load("./Planet Skins/Mercury Sprites/mercury_sp21.png"), True, True), 
    pygame.transform.flip(pygame.image.load("./Planet Skins/Mercury Sprites/mercury_sp22.png"), True, True), 
    pygame.transform.flip(pygame.image.load("./Planet Skins/Mercury Sprites/mercury_sp23.png"), True, True), 
    pygame.transform.flip(pygame.image.load("./Planet Skins/Mercury Sprites/mercury_sp24.png"), True, True), 
    pygame.transform.flip(pygame.image.load("./Planet Skins/Mercury Sprites/mercury_sp25.png"), True, True), 
    pygame.transform.flip(pygame.image.load("./Planet Skins/Mercury Sprites/mercury_sp26.png"), True, True), 
    pygame.transform.flip(pygame.image.load("./Planet Skins/Mercury Sprites/mercury_sp27.png"), True, True), 
    pygame.transform.flip(pygame.image.load("./Planet Skins/Mercury Sprites/mercury_sp28.png"), True, True), 
    pygame.transform.flip(pygame.image.load("./Planet Skins/Mercury Sprites/mercury_sp29.png"), True, True), 
    pygame.transform.flip(pygame.image.load("./Planet Skins/Mercury Sprites/mercury_sp30.png"), True, True)
]

venus_sprites = [ # Have to flip venus sprite because intial x position is flipped
    pygame.transform.flip(pygame.image.load("./Planet Skins/Venus Sprites/venus_sp1.png"), True, True), 
    pygame.transform.flip(pygame.image.load("./Planet Skins/Venus Sprites/venus_sp2.png"), True, True),
    pygame.transform.flip(pygame.image.load("./Planet Skins/Venus Sprites/venus_sp3.png"), True, True),
    pygame.transform.flip(pygame.image.load("./Planet Skins/Venus Sprites/venus_sp4.png"), True, True),
    pygame.transform.flip(pygame.image.load("./Planet Skins/Venus Sprites/venus_sp5.png"), True, True),
    pygame.transform.flip(pygame.image.load("./Planet Skins/Venus Sprites/venus_sp6.png"), True, True),
    pygame.transform.flip(pygame.image.load("./Planet Skins/Venus Sprites/venus_sp7.png"), True, True),
    pygame.transform.flip(pygame.image.load("./Planet Skins/Venus Sprites/venus_sp8.png"), True, True),
    pygame.transform.flip(pygame.image.load("./Planet Skins/Venus Sprites/venus_sp9.png"), True, True),
    pygame.transform.flip(pygame.image.load("./Planet Skins/Venus Sprites/venus_sp10.png"), True, True),
    pygame.transform.flip(pygame.image.load("./Planet Skins/Venus Sprites/venus_sp11.png"), True, True),
    pygame.transform.flip(pygame.image.load("./Planet Skins/Venus Sprites/venus_sp12.png"), True, True),
    pygame.transform.flip(pygame.image.load("./Planet Skins/Venus Sprites/venus_sp13.png"), True, True),
    pygame.transform.flip(pygame.image.load("./Planet Skins/Venus Sprites/venus_sp14.png"), True, True),
    pygame.transform.flip(pygame.image.load("./Planet Skins/Venus Sprites/venus_sp15.png"), True, True)
]

mars_sprites = cut_spritesheet(pygame.image.load("./Planet Skins/Mars Sprites.png"), 30)
    
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



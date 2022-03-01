import pgzrun

grid_width=16
grid_height=12
grid_size=50
#determines the size of each swuare in the grid

WIDTH=grid_width*grid_size
HEIGHT=grid_height*grid_size

MAP=["WWWWWWWWWWWWWWWW",
     "W              W",
     "W              W",
     "W  W  KG       W",
     "W  WWWWWWWWWW  W",
     "W              W",
     "W      P       W",
     "W  WWWWWWWWWW  W",
     "W      GK   W  W",
     "W              W",
     "W              D",
     "WWWWWWWWWWWWWWWW"]

def screen_coords(x,y):
    return (x*grid_size, y*grid_size)
#creates screen coordinates from the grid and its position

def grid_coords(actor):
    return (round(actor.x/grid_size), round(actor.y/grid_size))
#determines the actor location on the grid

def setup_game():
    global player, keys_to_collect
    player=Actor("player", anchor=("left", "top"))
    keys_to_collect=[]
    for y in range (grid_height):
        for x in range (grid_width):
            square=MAP[y][x]
            if square=="P":
                player.pos=screen_coords(x,y)
            elif square=="K":
                key=Actor("key", anchor=("left", "top"), \
                    pos=screen_coords(x,y))
                keys_to_collect.append(key)
#initializes the player and key on the screeen
#allows keys to be pickup-able

def draw_background():
    for y in range (grid_height):
        for x in range (grid_width):
            screen.blit("floor1", screen_coords(x,y))
#adds floor image to game

def draw_scenery():
    for y in range (grid_height):
        for x in range (grid_width):
            square=MAP[y][x]
            if square=="W":
                screen.blit("wall", screen_coords(x,y))
            elif square=="D":
                screen.blit("door", screen_coords(x,y))
#adds more scene images like wall and door

def draw_actors():
    player.draw()
    for key in keys_to_collect:
        key.draw()
#draws the player with player.draw and each key in the list of keys with key.draw

def draw():
    draw_background()
    draw_scenery()
    draw_actors()
#draws background first, scenery on top, and then actors on top of that

def on_key(key):
    if key==keys.LEFT:
        move_player(-1,0)
    elif key==keys.UP:
        move_player(0,-1)
    elif key==keys.RIGHT:
        move_player(1,0)
    elif key==key.DOWN:
        move_player(0,1)
#determines which direction player will move based on key pressed

def move_player(dx, dy):
    (x,y)=grid_coords(player)
    x+=dx
    y+=dy
    square=MAP[x][y]
    if square=="W":
        return
    elif square=="D":
        return
    player.pos=screen__coords(x,y)
#allows player movement but limits it based on other elements present in the scene


setup_game()
pgzrun.go()

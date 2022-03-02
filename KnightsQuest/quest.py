import pgzrun

grid_width=16
grid_height=12
grid_size=50
guard_move_interval=.5
#determines the size of each square in the grid

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
    return (round(actor.x/ grid_size), round(actor.y/ grid_size))
#determines the actor location on the grid

def setup_game():
    global game_over, player_won, player, keys_to_collect, guards
    game_over=False
    player_won=False
    player=Actor("player", anchor=("left", "top"))
    keys_to_collect=[]
    guards=[]
    for y in range (grid_height):
        for x in range (grid_width):
            square=MAP[y][x]
            if square=="P":
                player.pos=screen_coords(x,y)
            elif square=="K":
                key=Actor("key", anchor=("left", "top"), \
                    pos=screen_coords(x,y))
                keys_to_collect.append(key)
            elif square=="G":
                 guard=Actor("guard", anchor=("left", "top"), \
                    pos=screen_coords(x,y))
                 guards.append(guard)
#sets game over as false
#initializes the player and key on the screeen
#allows keys to be pickup-able
#inserts guards

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
    for guard in guards:
        guard.draw()
#draws the player with player.draw and each key in the list of keys with key.draw

def draw_game_over():
    screen_middle=(WIDTH/2,HEIGHT/2)
    screen.draw.text("game over", midbottom=screen_middle, \
        fontsize=grid_size, color="pink", owidth=1)
    if player_won:
        screen.draw.text("you won!", midtop=screen_midddle, \
            fontsize="green", owidth=1)
    else:
        screen.draw.text("try again", midtop=screen_midddle, \
            fontsize="red", owidth=1)
#defines how game over will be drawn and where 

def draw():
    draw_background()
    draw_scenery()
    draw_actors()
    if game_over:
        draw_game_over()
#draws background first, scenery on top, and then actors on top of that and will draw game over if game over

def on_key_down(key):
    if key==keys.LEFT:
        move_player(-1,0)
    elif key==keys.UP:
        move_player(0,-1)
    elif key==keys.RIGHT:
        move_player(1,0)
    elif key==keys.DOWN:
        move_player(0,1)
#determines which direction player will move based on key pressed

def move_player(dx, dy):
    global game_over, player_won
    if game_over:
        return
    (x,y)=grid_coords(player)
    x+=dx
    y+=dy
    square=MAP[y][x]
    if square=="W":
        return
    elif square=="D":
        if len(keys_to_collect)>0:
            return
        else:
            game_over=True
            player_won=True
    for key in keys_to_collect:
        (key_x, key_y)=grid_coords(key)
        if x==key_x and y==key_y:
            keys_to_collect.remove(key)
            break
    player.pos=screen_coords(x,y)
#allows player movement but limits it based on other elements present in the scene
#removes key fromm key position if the actor is in the same position

def move_guard(guard):
    global game_over
    if game_over:
        return
    (player_x,player_y)=grid_coords(player)
    (guard_x, guard_y)=grid_coords(guard)
    if player_x > guard_x and MAP[guard_y][guard_x+1]!="W":
        guard_x+=1
    elif player_x < guard_x and MAP[guard_y][guard_x-1]!="W":
        guard_x-=1
    elif player_y > guard_y and MAP[guard_y+1][guard_x]!="W":
        guard_y+=1
    elif player_y < guard_y and MAP[guard_y-1][guard_x]!="W":
        guard_y-=1
    guard.pos=screen_coords(guard_x,guard_y)
    if guard_x==player_x and guard_y==player_y:
        game_over=True
#tells the guard actors how to move towards the player. if there is no wall between them,
#move towards player and if they are in the same square game over

def move_guards():
    for guard in guards:
        move_guard(guard)


setup_game()
clock.schedule_interval(move_guards,guard_move_interval)
pgzrun.go()

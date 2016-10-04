from pico2d import *

open_canvas()
 
character = load_image('magicianAttack.png')
 
frame= 0
while(1):
    clear_canvas()
    character.clip_draw(23*frame , 16*1,23, 16, 400, 400, 400, 200)
    delay(0.2) 
    update_canvas()
    frame=(frame+1)%5

    get_events()
  
delay(2)
del(character)
close_canvas()
  
 
 

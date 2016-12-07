from pico2d import *

open_canvas()
 
character = load_image('waterEffect.png')
 
frame= 0
while(1):
    clear_canvas()
    character.clip_draw(8*frame , 8*0,8, 8, 400, 400, 50, 50)
    delay(0.2) 
    update_canvas()
    frame=(frame+1)%6

    get_events()
  
delay(2)
del(character)
close_canvas()
  
 
 

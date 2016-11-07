from pico2d import *

open_canvas()
 
character = load_image('thunderEffect.png')
 
frame= 0
while(1):
    clear_canvas()
    character.clip_draw(16*frame , 16*0,16, 16, 400, 400, 400, 200)
    delay(0.2) 
    update_canvas()
    frame=(frame+1)%6

    get_events()
  
delay(2)
del(character)
close_canvas()
  
 
 

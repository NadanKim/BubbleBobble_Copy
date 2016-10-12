from pico2d import *

open_canvas()
 
character = load_image('stagemove.png')
 
frame= 0
while(1):
    clear_canvas()
    character.clip_draw(30*frame , 32*0,30, 32, 400, 400, 400, 200)
    delay(0.2) 
    update_canvas()
    frame=(frame+1)%10

    get_events()
  
delay(2)
del(character)
close_canvas()
  
 
 

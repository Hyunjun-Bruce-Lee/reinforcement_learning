till 600 generation Fitness only went up to 1<br>
> **rewords (+)**<br>
> SHOOT_REWORD = 1<br>
> TARGET_HIT_REWORD = 20<br>
> **penalties (-)**<br>
> BULET_MISS_PENALTY = 1.2<br>
> MOVE_OUT_OF_BORD_PENALTY = 0.8<br>
> SHOOT_WHILE_RELOAD = 0.2<br>
<br>
nomatter how i fix the score using rule above Fitness is stuck at 1 <br>
<br>
it seems new design of rule set is needed<br>



bullet x location = shooters location, y moves 1pix every 1 frame
target y location = 25, x moves 1pix every 2 fram

frame = f
f/2+t == f+b

s_x -0.5t = 0

frame = f
shooters_position = (s_x, 3)
target_position = (t_x, 25)
bullet_initial_position = (s_x, 4)




frame = f
shooters_initial_location = (15, 3)
targets_initial_location = (0 or 29, 25)

shooter can move horizontally toward random location at speed of 1 pixel per frame, 
which makes shooters location(x position) after f frame = f(x).

target will move horizontally depending on its initial_location at speed of 0.5 pixel per frame,
which makes targets x position after f frame = (+ or - )0.5*f + targets_initial_location.

when shooter fires a bullet, its initial location will be (f(x), 4).



frame = f
bullets_current_location = (b_x, b_y)
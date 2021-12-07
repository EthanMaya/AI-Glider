###THIS IS PSEUDOCODE FOR SIMPLE PROGRAMS TO CONTROL PHYSICAL GLIDERS###
###WITH LITTLE EFFORT, THIS CAN BE TURNED INTO USABLE CODE###
#RateOfTurn
#NOTE: the elovater controls the speed at which the glider turns, the ailerons do not
#NOTE: might work to use roll instead of ailerons? but might not be worth it
import Pitch
import Yaw
import Roll
#x is front of aircraft
#wanted_pich = #0???
aileron = #output, control surface, servo
ROT = #(Rate Of Turn) around z axis input gyro
WROT = #(Wanted Rate Of Turn) around z axis [R or L]

#an easier way to code it
+ = right
- = left
while True:
    if WROT > ROT: # if glider isn't turning to the right enough OR is turning to much to the left
        Roll + # increase 
    if WROT < ROT: # if glider isn't turning to the left enough OR is turning to much to the right
        Roll -
    run_file(Pitch, Yaw,)

    
#a more difficult way, but good to be able to understand
L = left
R = right
while True:
    if WROT = R:        
        if WROT(R) > ROT(R)
            aileron(R +)
            run_file(pitch())
        if WROT(R) < ROT(R)
            aileron(R -)
            run_file(Pitch)
            run_file(Yaw)
    if WROT = L:        
            if WROT(L) > ROT(L)
                aileron(L +)
                run_file(pitch())
            if WROT(L) < ROT(L)
                aileron(L -)
                run_file(pitch)
                run_file(pitch)
    


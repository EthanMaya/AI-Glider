###THIS IS PSEUDOCODE FOR SIMPLE PROGRAMS TO CONTROL PHYSICAL GLIDERS###
###WITH LITTLE EFFORT, THIS CAN BE TURNED INTO USABLE CODE###
#Yaw
Aileron = #output, control surface
wanted_roll = # defined by AI, probably so that nose is pointing into airstream
actual_roll = # gyro
right = >0 aribitray units # right equals greater than zero, ie, number big. this is so we can use > instead of if R, if L, then... and lots of statements
left = <0 aribitray units#same as above

if actual_roll > wanted_roll: #if glider isn't yawed to the right enough
    Aileron -
if actual_roll < wanted_roll: #if glider isn't yawed to the right enough
    Aileron +

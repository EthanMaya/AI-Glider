###THIS IS PSEUDOCODE FOR SIMPLE PROGRAMS TO CONTROL PHYSICAL GLIDERS###
###WITH LITTLE EFFORT, THIS CAN BE TURNED INTO USABLE CODE###
#Yaw
Rudder = #output, control surface
wanted_yaw = # defined by AI, probably so that nose is pointing into airstream
actual_yaw = # gyro
right = >0 # number big. this is so we can use > instead of if R, if L, then...
left = <0 #same as above

if actual_yaw > wanted_yaw: #if glider isn't yawed to the right enough
    Rudder -
if actual_yaw < wanted_yaw: #if glider isn't yawed to the right enough
    Rudder +

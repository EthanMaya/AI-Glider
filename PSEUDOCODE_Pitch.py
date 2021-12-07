###THIS IS PSEUDOCODE FOR SIMPLE PROGRAMS TO CONTROL PHYSICAL GLIDERS###
###WITH LITTLE EFFORT, THIS CAN BE TURNED INTO USABLE CODE###
#pitch
elovater = #output, control surface
actual_pitch = #input gyro pitch of aircraft
wanted_pitch = #AI defined amount of what pitch angle it wants the glider at

if actual_pitch < wanted_pitch:
    elovater +
if actual_pitch > wanted_pitch:
    elovater -

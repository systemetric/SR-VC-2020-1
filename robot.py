from sr.robot import *
from virtual_bot import VirtualBot
R = VirtualBot()

def reverse(time):
    interval = 0.05
    x = int(time // interval)
    R.setDriveMotors(-30)
    for i in range(x):
        if R.back_left_distance < 0.25 or R.back_right_distance < 0.25:
            R.stopDriveMotors()
            break
        R.sleep(interval)
    R.stopDriveMotors()
    
def allMarkersDistances():
    visible = {}
    repeats = 30
    while repeats > 0:
        repeats -= 1
        R.turn(20,0.1)
        markers = R.see()
        for m in markers:
            if m.info.code not in list(visible.keys()) and m.info.marker_type==MARKER_ARENA and m.dist < 4:
                visible[(m.info.code-offset)%28] = m.dist
    for i in (0,27):
        if i not in list(visible.keys()):
            visible[i] = 100
    return visible
        
def findHome():
    visible = allMarkersDistances()
    while visible[0] > 1.3 and visible[27] > 1.3:
       got = R.closeGripper()
       if got == False:
           return False
           break
       sorteddist = {k: v for k, v in sorted(visible.items(), key=lambda item: item[1])}
       sortedkey = sorted(visible)
       #print(sortedkey)
       #print(sorteddist)
       closest = list(sorteddist.items())[0][0]
       print(hr,closest)
       if (closest <= 13 and closest not in sortedkey[0:3]) or (closest >= 14 and (closest in sortedkey[-3:-1])):
           print(hr,"going for",off(sortedkey[1]))
           R.seek_marker(off(sortedkey[1]), power=30)
           R.drive_to_marker(off(sortedkey[1]),dist=0.5, power=30,interval=1)
       #elif list(sorteddist.items())[0][0] >= 13:
       else:
           print(hr,"going for",off(sortedkey[-2]))
           R.seek_marker(off(sortedkey[-2]), power=30)
           R.drive_to_marker(off(sortedkey[-2]),dist=0.5,power=30,interval=1)
       
       R.shuffle(0.5)
       visible = allMarkersDistances()
    print(hr,"home")
    return True

def socialDistancing():
    distances = [R.left_distance, R.right_distance, R.back_left_distance, R.back_right_distance,R.front_left_distance,R.front_right_distance]
    while min(distances) < 0.25:
        if max(distances) == distances[2] or max(distances) == distances[3]:
            reverse(0.2)
        elif max(distances) == distances[0]:
            R.turn(-20, 0.4)
        elif max(distances) == distances[1]:
            R.turn(20, 0.4)
        elif max(distances) == distances[4] or max(distances) == distances[5]:
            R.shuffle(0.2)
        distances = [R.left_distance, R.right_distance, R.back_left_distance, R.back_right_distance,R.front_left_distance,R.front_right_distance]
        #print(distances)

def off(i):
    return (i+offset)%28

global hr
hr = "HR1 "
###########################################


R.setDriveMotors((10,-10))
R.sleep(1)
R.stopDriveMotors()
R.setDriveMotors(-50)
R.sleep(3)
R.setDriveMotors((10))
R.sleep(1)
R.setDriveMotors((60))
R.sleep(1.5)

R.turncont(-50)
# all = []
#######################SILVER shove
print (hr + "Silver shove start...")
#R.turncont(-50)
valid_markers = []
for i in range(1):
    markers = R.see()
    for m in markers:
        if m.info.marker_type == MARKER_TOKEN_SILVER and m.info.code in [47, 45, 46, 44]:
            print(hr +"Found new SILVER marker")
            valid_markers.append(m)
    R.sleep(0.1);
R.stopDriveMotors()

if not valid_markers:
    print(hr + "Could not find any valid markers")
    soken = 46 #see below (search "target" for all cases probs)
else:
    valid_markers = sorted(valid_markers, key=lambda x: x.dist)
    target = valid_markers[0]
    R.seek_marker(target.info.code)
    soken = target.info.code
print ("HR1 driving towards SILVER marker " + str(soken))

for i in range (1):
    R.seek_marker(soken)
    R.drive_to_marker(soken, power = 30, dist = 1, epsilon = 1, interval = 1)

R.sleep(1)
R.setDriveMotors((50,50))
R.sleep(2)
R.motors[1].m0.power = -5
R.stopDriveMotors()
R.setDriveMotors(-30)
R.sleep(1.5)
R.setDriveMotors((50,-50))

#######################ARENA lineup
print (hr + "Arena lineup...")
#R.turncont(-50)
valid_markers = []
for i in range(20):
    markers = R.see()
    for m in markers:
        if m.info.marker_type == MARKER_ARENA and m.info.code in [24, 3, 10, 17]:
            print(hr + "Found new ARENA marker")
            valid_markers.append(m)
    R.sleep(0.005);
R.stopDriveMotors()
print(hr + "stopped motors")

if not valid_markers:
    print(hr + "Could not find any valid markers")
    aoken = 10
else:
    valid_markers = sorted(valid_markers, key=lambda x: x.dist)
    target = valid_markers[0]
    print(hr + "Found marker {}".format(target.info.code))
    print(hr + "started seeking")
    R.seek_marker(target.info.code, power = -50)
    print(hr + "stopped seeking")
    print(valid_markers)
    aoken = target.info.code
print ("HR1 driving towards ARENA marker " + str(aoken))

for i in range (1):
    R.seek_marker(aoken, power = 30)
    R.drive_to_marker(aoken, power = 20, dist = 0.4)
    
R.setDriveMotors((20,-20))
R.sleep(2.6)
R.stopDriveMotors()
R.sleep(0.5)
R.setDriveMotors(-50)
R.sleep(3)
R.raiseGripper()
R.setDriveMotors((10))
R.sleep(1)
R.stopDriveMotors()

#######################GOLD marker drive
print (hr + "Starting towards gold marker...")
#R.turncont(-50)
valid_markers = []
for i in range(1):
    markers = R.see()
    for m in markers:
        if m.info.marker_type == MARKER_TOKEN_GOLD and m.info.code in [36,37,38,39]:
            #print("Found new GOLD marker")
            valid_markers.append(m)
    R.sleep(0.1);
R.stopDriveMotors()

if not valid_markers:
    print(hr + "Could not find any valid markers")
    goken = 38
    old = 38
else:
    valid_markers = sorted(valid_markers, key=lambda x: x.orientation.rot_y)
    target = valid_markers[0]
    R.seek_marker(target.info.code)
    goken = target.info.code
    old = target.info.code
print (hr + "HR1 driving towards GOLD marker " + str(goken))
print (goken)

#######################Checking GOLD cube
print (hr + "Checking gold cube...")
gotgoken = False
R.seek_marker(goken)
R.openGripper()
R.drive_to_marker(goken, power = 30, dist = 0.5, interval = 0.1,epsilon=1)
R.setDriveMotors(20)
R.sleep(5)
R.stopDriveMotors()

R.motors[1].m0.power = 5
R.sleep(0.1)
R.motors[1].m0.power = 0
R.sleep(0.1)
R.stopDriveMotors()
R.closeGripper()
R.motors[1].m1.power = -100

"""R.setDriveMotors(-10)
R.lowerGripper()
R.sleep(1)
#R.setDriveMotors((-20,20))
#R.sleep(1.5)
R.stopDriveMotors()

#R.closeGripper()
R.setDriveMotors(-10)
R.sleep(1.5)

R.setDriveMotors((-10,10))
#R.closeGripper()
R.sleep(3.5)
R.stopDriveMotors()
R.setDriveMotors(30)
R.sleep(5)
R.openGripper()
R.setDriveMotors(-50)
R.sleep(2)
R.setDriveMotors((10,-10))
R.sleep(2.5)
R.stopDriveMotors()
R.sleep(1)  """
R.setDriveMotors(-10)
R.sleep(2)
R.stopDriveMotors()
R.setDriveMotors((-10,10))
#R.closeGripper()
R.sleep(3.5)
R.lowerGripper()
R.stopDriveMotors()

#######################Driving back to corner
#R.turncont(-50)
print (hr + "Driving back to corner...")
valid_markers = []
for i in range(20):
    markers = R.see()
    for m in markers:
        if m.info.marker_type == MARKER_ARENA and m.info.code in [0, 7, 14, 21]:
            print(hr + "Found new ARENA marker")
            valid_markers.append(m)
    #R.sleep(0.1);
R.stopDriveMotors()

if len(valid_markers)==0:
    print(hr + "Could not find any valid markers")
    aoken = 14 #we are in corner 2 most often on sun1
else:
    valid_markers = sorted(valid_markers, key=lambda x: x.dist)
    target = valid_markers[0]
    R.seek_marker(target.info.code)
    aoken = target.info.code
print ("HR1 driving towards ARENA marker " + str(aoken))
print (aoken)
for i in range (1):
    R.seek_marker(aoken, power = 30)
    R.drive_to_marker(aoken, power = 20, dist = 0.3)
    
R.shuffle(1)

R.openGripper()
R.raiseGripper()
R.setDriveMotors((20,-20))
R.sleep(2.5)
R.stopDriveMotors()
R.lowerGripper()

homezones = {2:14, 3:21, 0:0, 1:7}
global offset
offset = homezones[R.zone]
#global hr
hr = "HR1"

collected = []
for x in range(2):
    got = False
    while got == False:
        g,goken = 0,None
        s,soken = 0,None
        a,aoken = 0,None
        while goken == None:
            repeat = 0
            while repeat < 25 and goken == None:
                markers = R.see()
                for m in markers:
                    if m.info.code in range(32,36) and m.info.code not in collected:
                        g = g+1
                        goken = m.info.code
                        gm = m
                        break
                    if m.info.marker_type == MARKER_TOKEN_SILVER:
                        s = s+1
                        soken = m.info.code
                        break
                    if m.info.marker_type == MARKER_ARENA:
                        a = a+1
                #print(goken)
                repeat += 1
                if goken == None: R.turn(10,0.4)
            if goken == None: R.shuffle(2)
        gokenrot = gm.orientation.rot_y
        gokenangle = gm.rot_y
        #print(gokenrot, gokenangle)
        if abs(gokenangle) < 20:
            #R.turn_from_marker(goken)
            R.turn(-20, 0.2)
        while abs(gokenrot) > 20:
            R.shuffle(0.3)
            R.turn(25, 0.2)
            a = R.turn_to_marker(goken,epsilon=4)
            if a == None:
                R.seek_marker(goken,power=20)
                break
            for m in R.see():
                if m.info.code == goken:
                    gokenrot = m.orientation.rot_y
                    print(hr,gokenrot)
            #R.turn_from_marker(goken, 1)
            R.turn(-13, 0.2)
        print(hr,"final")
        R.drive_to_marker(goken, power = 30, dist = 0.5,epsilon=1,interval=0.05)
        R.openGripper()
        R.lowerGripper()
        got = False
        R.setDriveMotors(30)
        time = 0
        while (R.front_right_distance > 0.2 and R.front_left_distance > 0.2) and time < 30:
            #R.front_right_distance, R.front_left_distance
            R.sleep(0.1)
            time += 1
        print(hr,R.front_right_distance, R.front_left_distance)
        R.stopDriveMotors()
        print(hr,"stopped")
        if R.front_right_distance > R.front_left_distance:
            R.setDriveMotors((0,30))
            time = 0
            while (R.front_left_distance > 0.15) and time < 10:
               # print(R.front_right_distance, R.front_left_distance)
                R.sleep(0.05)
                time += 1
        else: 
            R.setDriveMotors((30,0))
            time = 0
            while (R.front_left_distance > 0.15) and time < 10:
               # print(R.front_right_distance, R.front_left_distance)
                R.sleep(0.05)
                time += 1
        R.stopDriveMotors()
        R.lowerGripper()
        R.shuffle(0.1)
        got = R.closeGripper()
        R.raiseGripper()
        R.lowerGripper()
        reverse(0.2)
        print(hr,got)
        if got == False:
            socialDistancing()
            reverse(0.5)
 
        elif got == True:
            if x == 0:
                reverse(1.2)
                got = R.closeGripper()
            elif x == 1:
                got = findHome()
            if got == True:
                R.seek_marker(off(27),power=30,repeats=30)
                R.openGripper()
                collected.append(goken)
                got = False
                R.raiseGripper()
                R.turn(30,2.5)
                R.lowerGripper()
                if x == 0:
                    if R.find_marker(off(4)) == None:
                        R.shuffle(1)
                        R.seek_marker(code=off(4), power=-10,repeats=30)
                    R.drive_to_marker(off(4), power=30,dist=0.3, epsilon=4, interval=0.7)
                    #R.turn(30,0.3)
                    print(hr,"now again")
                break
print(hr,"end")



for i in range (100):
    #R.turncont(-50)
    # all = []
    closest = None
    dist = 5
    for i in range(10):
        to_stop = False
        markers = R.see()
        for m in markers:
            if m.info.marker_type == MARKER_TOKEN_SILVER:
                print("Found SILVER marker")
                print(m.dist)
                if m.dist < dist:
                    dist = m.dist
                    closest = m
                    R.stopDriveMotors()
                    to_stop = True
                    break

        R.sleep(0.1)
    if closest != None:
        soken = closest.info.code
        print ("HR1 driving towards SILVER marker " + str(soken))
        for i in range (1):
            R.seek_marker(soken)
            print(R.drive_to_marker(soken, power = 30, dist = 0.5, epsilon = 1, interval = 1))
        R.setDriveMotors(50)
        R.sleep(2)
        R.closeGripper()
        R.setDriveMotors(-50)
        R.setDriveMotors((20,-20))
        R.sleep(2)
        R.openGripper()
        R.setDriveMotors((-20,20))
        R.sleep(2)
        R.stopDriveMotors()
        R.sleep(1)
    else:
        print ("No silver cubes in zone")

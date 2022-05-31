import bpy
import random
import numpy as np
import time

bpy.ops.object.select_all(action='TOGGLE')
bpy.ops.object.select_all(action='TOGGLE')
bpy.ops.object.delete(use_global=False)

def initial_state(width):
    initial = np.zeros((1, width), dtype=int)
    if width % 2 == 0:
        initial = np.insert(initial, int(width / 2), values=0, axis=1)
        initial[0, int(width / 2)] = 1
        return initial
    else:
        initial[0, int(width / 2)] = 1
        return initial

def rule30(array):
    row1 = np.pad(array,[(0,0), (1,1)], mode='constant')
    next_row = array.copy()
    for x in range(1, array.shape[0]+1):
        for y in range(1, array.shape[1]+1):
            if row1[x-1][y-1] == 1 ^ (row1[x-1][y] == 1 or row1[x-1][y+1] == 1):
                next_row[x - 1, y - 1] = 1
            else:
                next_row[x - 1, y - 1] = 0
        return np.array(next_row)
def apply_rule(n):
    rv = initial_state(n)
    while rv[-1][0] == 0:
        rv = np.append(rv, rule30(rv[-1].reshape(1,-1)), axis=0)
    return rv


spacing = 1
r =0.5
scale=(r,r,r)
t_s = 100
x_array = [(0,0)]

array = apply_rule(50)
y = 0
num_objects = 0 

for i in array:
    x_l = len(i)
    x = 0
    for j in i:
        if (j == 1):
            location = (x-x_l,y,0)
            scale=(r,r, np.sin(y*0.1))
            num_objects+=1
            bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=location, scale=scale)
        x+=1
    y+=1
    print(y)


#total_time = 2*3.0 # Animation should be 2*pi seconds long
#fps = 24 # Frames per second (fps)
#bpy.context.scene.frame_start = 0
#bpy.context.scene.frame_end = int(total_time*fps*num_objects)+1
#nlast = 0
#for i in range(num_objects):
#    if i == 0:
#        myobj = bpy.data.objects['Cube']
#    elif i < 10:
#        myobj = bpy.data.objects['Cube.'+'00'+str(i)]
#    else:
#        myobj = bpy.data.objects['Cube.'+'0'+str(i)]
##    myobj.animation_data_clear()

#    # set first and last frame index


## loop of frames and insert keyframes every 10th frame
#    keyframe_freq = 10
#    nlast += int(bpy.context.scene.frame_end/(i+1))
#    for n in range(int(total_time*fps)):
#        t = total_time*n/nlast

#    # Do computations here...

#    # Check if n is a multiple of keyframe_freq
#        if n%keyframe_freq == 0:
#            # Set frame like this
#            bpy.context.scene.frame_set(n)

#            # Set current location like this
#            myobj.location.x = n
#            myobj.location.y = n
#            myobj.location.z = n
#            # Insert new keyframe for "location" like this
#            myobj.keyframe_insert(data_path="location", frame=nlast+n)      
#    print(i)

#for y in range(t_s):
#    for x in range((2*y)+1):
#        location = (x_array[x][0],x_array[x][1],0)
#        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=location, scale=scale)
#    for x in range(len(x_array)*2 -1 ):
#        if(x == 0):
#            
#        
#        item = bpy.context.object
#        if random.random() < 0.1:
#            item.data.materials.append(bpy.data.materials["Material.001"])
#        else:
#            item.data.materials.append(bpy.data.materials["Material.001"])
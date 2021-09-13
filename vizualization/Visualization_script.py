import bpy
import pickle
import os
import math
fn=r'E:\projects\RL_mini_projects\maze_solver\log2\maps_pos\pos_map_log3.pkl'
f=open(fn,'rb')
log_data=pickle.load(f)
f.close()
mp=log_data['mp']
st=log_data['st']
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
#get rws and columns
#x=rw, y=col
#rws=10
#cls=5
rws=len(mp)
cls=len(mp[0])
bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=((rws-1)/2, (cls-1)/2, 0),rotation=(0,0,0), scale=(4, 4, 1))
fl_nm=bpy.context.active_object.name
bpy.data.objects[fl_nm].data.materials.append(bpy.data.materials['floor_P_BSDF'])
bpy.ops.transform.resize(value=(rws,cls , 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
#adding ligth source
##finding height
lngth=max(rws,cls)
hght=lngth*0.5*math.tan(60*math.pi/180)
bpy.ops.object.light_add(type='POINT', align='WORLD', location=((rws-1)/2, (cls-1)/2, hght), scale=(1, 1, 1))
bpy.context.object.data.energy = hght*50
for ni,i in enumerate(mp):
    for nj,j in enumerate(i):
        if(j==False):
            bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(ni, nj, 0.5), scale=(1, 1, 1))
            cub_nm=bpy.context.active_object.name
            bpy.data.objects[cub_nm].data.materials.append(bpy.data.materials['cubes_P_BSDF'])
bpy.ops.mesh.primitive_ico_sphere_add(radius=0.5,subdivisions=4, enter_editmode=False, align='WORLD', location=(st[0], st[1], 0.5), scale=(1, 1, 1))
ag=bpy.context.active_object.name
bpy.data.objects[ag].data.materials.append(bpy.data.materials['agent_mat'])
bpy.context.scene.frame_set(1)
bpy.ops.anim.keyframe_insert_menu(type='Location')
frame=20
frm_stp=20
poss=log_data['pos']
for i in range(1,max(poss.keys())+1):
    pos=poss[i]
    #bpy.ops.transform.translate(value=(1, 0, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)    
    bpy.context.scene.frame_set(frame)
    frame+=frm_stp
    bpy.data.objects[ag].location=(pos[0],pos[1],0.5)
    bpy.ops.anim.keyframe_insert_menu(type='Location')
bpy.context.scene.frame_end=frame
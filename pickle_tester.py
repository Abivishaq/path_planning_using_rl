import pickle 
fn=r'E:\projects\RL_mini_projects\maze_solver\log2\maps_pos\pos_map_log2.pkl'
f=open(fn,'rb')
data=pickle.load(f)
f.close()
print(data)
from shortest_path_finder_func import shrt_pth_plc as sht_pth
from shortest_path_finder_func import mp_int2mp
from random import choice
from os import mkdir as md
from os.path import exists as exs
import pickle
class bot:
	def __init__(self,pos,gl,mp_dim):
		self.pos=pos
		self.gl=gl
		self.mp=self.emp_mp(mp_dim)
		self.nors=100
		self.gmma=1
		self.thrs_delta=1
		self.itr_no=1
		self.mp_log={}
		self.pos_log={}
	def scan(self,env):
		sns=env.scan(self.pos)
		self.sns=sns
		if((False in sns) or True):
			for i in range(len(sns)):
				for j in range(len(sns[0])):
					sns_pos=(i-1,j-1)
					gl_sns_pos=(self.pos[0]+sns_pos[0],self.pos[1]+sns_pos[1])
					if(gl_sns_pos[0]<0 or gl_sns_pos[0]>=len(self.mp) or gl_sns_pos[1]<0 or gl_sns_pos[1]>=len(self.mp[0])):
						continue
					self.mp[gl_sns_pos[0]][gl_sns_pos[1]]=sns[i][j]
	def mov(self,env):
		plc=sht_pth(self.mp,self.gl,self.nors,self.gmma,self.thrs_delta).act_probs
		acts=plc[self.pos[0]][self.pos[1]]
		self.acts=acts
		mx_prb=max(acts)
		ps_acts=[]
		for i in range(len(acts)):
			if(acts[i]==mx_prb):
				ps_acts.append(i)
		act=choice(ps_acts)
		self.act=act
		self.pos=env.mov(self.pos,act)
	def emp_mp(self,mp_dim):
		mp=[]
		for i in range(mp_dim[0]):
			tmp=[]
			for j in range(mp_dim[1]):
				tmp.append(True)
			mp.append(tmp)
		return(mp)
	def logger(self,fn1,fn2):
		self.mp_log[self.itr_no]=self.mp
		self.pos_log[self.itr_no]=self.pos
		with open(fn1,'a') as f:
			f.write(str(self.itr_no)+':')
			f.write(str(self.pos))
		with open(fn2,'a') as f:
			f.write(str(self.itr_no)+':')
			f.write('pos:'+str(self.pos))
			f.write('\nmap:\n')
			for i in self.mp:
				f.write(str(i))
				f.write('\n')
			
			f.write('Acts:')
			f.write(str(self.acts))
			f.write('\n')
			f.write('act:')
			f.write(str(self.act))
			f.write('\n')
			f.write('sns:\n')
			for i in self.sns:
				f.write(str(i))
				f.write('\n')
			f.write('\n')
	def driver_func(self,env,fn):
		while(True):
			print(self.itr_no)
			self.scan(env)
			self.mov(env)
			self.logger(fn[0],fn[1])
			self.itr_no+=1
			if(self.pos==self.gl):
				print("Reached goal")
				break



class environment:
	def __init__(self,mp):
		if(type(mp[0][0])==type(1)):
			mp=mp_int2mp(mp)
		self.mp=mp
		self.sns_rad=1
	def scan(self,pos):
		sns_mp=[]
		for i in range(self.sns_rad*2+1):
			tmp=[]
			for j in range(self.sns_rad*2+1):
				sns_pos=(i-1,j-1)
				gl_sns_pos=(pos[0]+sns_pos[0],pos[1]+sns_pos[1])
				if(gl_sns_pos[0]<0 or gl_sns_pos[0]>=len(self.mp) or gl_sns_pos[1]<0 or gl_sns_pos[1]>=len(self.mp[0])):
					tmp.append(True)
					continue
				tmp.append(self.mp[gl_sns_pos[0]][gl_sns_pos[1]])
			sns_mp.append(tmp)
		return(sns_mp)
	def mov(self,pos,act):
		mov_dct={0:(0,-1),1:(1,0),2:(0,1),3:(-1,0)}
		add=mov_dct[act]
		ag_pos=pos
		new_pos=(ag_pos[0]+add[0],ag_pos[1]+add[1])
		rw_max=len(self.mp)
		cl_max=len(self.mp[0])
		if(new_pos[0]>=rw_max or new_pos[0]<0 or new_pos[1]>=cl_max or new_pos[1]<0):
			new_pos=pos
		elif(self.mp[new_pos[0]][new_pos[1]]==False):
			new_pos=pos
		return(new_pos)
def dir_mk(fn):
	if(not exs(fn)):
		md(fn)

def main():
	fn_no=3
	mp=[[1,1,1,1,1,1,1,1,1,1],[1,0,1,1,1,1,1,1,1,1],[1,0,1,1,1,1,1,1,1,1],[1,0,1,1,1,1,1,1,1,1],[1,0,1,1,1,1,1,1,1,1],[1,0,1,1,1,1,1,1,1,1],[1,0,1,1,1,1,1,1,1,1],[1,0,1,1,1,1,1,1,1,1],[1,0,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,1,1]]
	gl=(9,9)
	st=(0,2)
	mp_dim=(len(mp),len(mp[0]))
	agent=bot(st,gl,mp_dim)
	env=environment(mp)
	fn='log2'
	dir_mk(fn)
	f1=fn+'\\pos'
	dir_mk(f1)
	f2=fn+'\\maps_pos'
	dir_mk(f2)
	f_bs1=f1+'\\pos_log'+str(fn_no)
	f_bs2=f2+'\\pos_map_log'+str(fn_no)
	f1=f_bs1+'.txt'
	f2=f_bs2+'.txt'
	fn=[f1,f2]
	agent.driver_func(env,fn)
	log_dict={}
	log_dict['pos']=agent.pos_log
	log_dict['ag_mps']=agent.mp_log
	log_dict['mp']=mp_int2mp(mp)
	log_dict['gl']=gl
	log_dict['st']=st

	fn_pkl=f_bs2+'.pkl'
	f=open(fn_pkl,'ab')
	pickle.dump(log_dict,f)
	f.close()


if(__name__=="__main__"):
	main()


from copy import deepcopy as dcpy
from os import listdir as ls
from os import mkdir as md
from os.path import exists as exs
class env:
	def __init__(self,gl,mp):
		#self.ag_pos=st
		self.gl=gl
		self.mp=mp
		self.rwds={'gl':10,'bl':-10,'fr':-1,'ofb':-10}
		# mp - map:
		#2d array of boolean
		#false unmovable spot, Blocked spot
		#True movable spot, Free spot
		#
		#row,column convention
		#top-left corner 0,0
		#
		self.mov_dct={0:(0,-1),1:(1,0),2:(0,1),3:(-1,0)}
		# 0:left->row+0,col-1
		# 1:down->row+1,col+0
		# 2:right->row+0,col+1
		# 3:up->row-1,col+0
		#
		# check if goal is in black spot
		#
	def run(self,st,act): # try replacing with 2 boolean variable for more memory efficiency
		mp=self.mp
		rwds=self.rwds
		add=self.mov_dct[act]
		ag_pos=st
		new_pos=(ag_pos[0]+add[0],ag_pos[1]+add[1])
		trm=False
		rw_max=len(mp)
		cl_max=len(mp[0])
		if(new_pos==self.gl):
			rw=rwds['gl']
			trm=True
		elif(new_pos[0]>=rw_max or new_pos[0]<0 or new_pos[1]>=cl_max or new_pos[1]<0):
			rw=rwds['ofb']
			new_pos=st
		elif(self.mp[new_pos[0]][new_pos[1]]):
			rw=rwds['fr']
		else:
			rw=rwds['bl']
			new_pos=st
		return([trm,rw,new_pos])

class policy:
	def __init__(self,mp):
		#assigns a uniform random policy
		rws=len(mp)
		cols=len(mp[0])
		self.act_probs=[]
		for i in range(rws):
			tmp=[]
			for j in range(cols):
				tmp.append([0.25,0.25,0.25,0.25])
			self.act_probs.append(tmp)

def init_vf(mp):
	vf=[]
	for i in range(len(mp)):
		tmp=[]
		for j in range(len(mp[0])):
			tmp.append(0)
		vf.append(tmp)
	return(vf)

def policy_eval(mp,plc,vf,en,gma,thrs_delta,gl):
	nr=len(vf)
	nc=len(vf[0])
	mx_delta=100
	while(mx_delta>thrs_delta):
		mx_delta=0
		for i in range(nr):
			for j in range(nc):
				if(mp[i][j]==False):
					continue
				if((i,j)==gl):
					continue
				new_vl=0
				st=[i,j]
				if(mp[i][j]): # Redundant checking
					for k in [0,1,2,3]:
						[trm,rw,n_pos]=en.run(st,k)
						if(trm):# Can remove this if-else block
							tmp=rw
						else:
							tmp=rw+gma*vf[n_pos[0]][n_pos[1]]
						new_vl+=plc.act_probs[i][j][k]*tmp
					delta=abs(vf[i][j]-new_vl)
					if(delta>mx_delta):
						mx_delta=delta
					vf[i][j]=new_vl
def greedify(vf,mp,en,gmma,gl):
	plc=policy(mp)
	rws=len(vf)
	cols=len(vf[0])
	for i in range(rws):
		for j in range(cols):
			if(mp[i][j]==False):
				continue
			if((i,j)==gl):
					continue
			st=(i,j)
			vls=[]
			for k in [0,1,2,3]:
				ret=en.run(st,k)
				nw_st=ret[2]
				vls.append(ret[1]+gmma*vf[nw_st[0]][nw_st[1]])
			mx_vl=max(vls)
			nooa=vls.count(mx_vl)
			pea=1/nooa
			probs=[]
			for k in range(4):
				if(vls[k]==mx_vl):
					probs.append(pea)
				else:
					probs.append(0)
			plc.act_probs[i][j]=probs
	return(plc)

def txt_log(pc,vf,no):
	pth='log'
	if(not pth in ls()):
		md(pth)
	pth2='log'
	flds=ls(pth2)
	lg_no=5 
	#if(not len(flds)==0):
	#	lg_no=int(flds[-1])+1
	pth3=pth2+'\\'+str(lg_no)
	if(not exs(pth3)):
		md(pth3)
		md(pth3+'\\vf')
		md(pth3+'\\plc')
	p_vf=pth3+'\\vf\\'+str(no)+'.txt'
	p_plc=pth3+'\\plc\\'+str(no)+'.txt'
	st_pc=str(pc.act_probs)
	st_vf=str(vf)
	with open(p_vf,'w') as f:
		f.write(st_vf)
	with open(p_plc,'w') as f:
		f.write(st_pc)

def policy_itr(nors,mp,gl,gmma,thrs_delta):
	plc=policy(mp)
	en=env(gl,mp)
	vf=init_vf(mp)
	it_no=0
	while(True):
		it_no+=1
		print(it_no)
		vf_tmp=dcpy(vf)
		policy_eval(mp,plc,vf,en,gmma,thrs_delta,gl)
		plc=greedify(vf,mp,en,gmma,gl)
		

		txt_log(plc,vf,it_no)
		if(vf_tmp==vf):
			break
		if(it_no>=nors):
			policy_eval(mp,plc,vf,en,gmma,thrs_delta,gl)
			break
	return(plc,vf)
def mp_int2mp(mp_int):
	mp=[]
	mp_dct={1:True,0:False}
	for i in mp_int:
		tmp=[]
		for j in i:
			tmp.append(mp_dct[j])
		mp.append(tmp)
	return(mp)
def main():
	#mp=[[True,True,True],[True,False,True],[True,True,True]]
	mp_int=[[1,1,0,1,1],[1,0,1,1,1],[1,0,1,0,1],[1,0,0,1,1],[1,1,1,1,1]]
	mp=mp_int2mp(mp_int)
	gl=(2,2)
	nors=1000
	gmma=1
	thrs_delta=1
	plc,vf=policy_itr(nors,mp,gl,gmma,thrs_delta)

if(__name__=='__main__'):
	main()
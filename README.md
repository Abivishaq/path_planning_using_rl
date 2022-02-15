# Path Planning Using RL
## Objective
An agent is dropped in a finite 2d discrete world. It is given a goal position. The objective is to reach the goal position. There are certain blocked spots in the map to which the agent cannot move to. The agent has knowldge of the size of the 2d discrete world. It also knows its location on the map and the goal points location. It doesn't information on the blocked spots. However it can sense 1 unit around it and find blocked spots in this range. The agent can move top, down, left or right.
## Approach
First the agent assumes the entire world is void of any blocked spots. At the start of each move step the agent scans the environment and updates it's map of the world. With this map it finds the optimal path to the goal. The optimal path is found using policy iteration. It moves forward using this optimal path.
The summarised form of the algorithm is:
>  agent's map<-intialized to be fully free\
>  iterate till goal reached
>>    scan environment\
>>    update map\
>>    find optimal path/policy with respect to agent's map\
>>    follow optimal path/policy
## Part's of the project
**maze_bot.py**  
This is the python script that runs the main concept of the code.  
**short_path_finder.py**  
This script contains the RL part of finding the optimal policy and its value function given a map. It is important to note that the policy and value function only dependend on the goal point. With the policy and value function you can find the optimal path from any free point on the map (As long as it is possible to connect that free point and the goal).  
**short_path_finder_func.py**  
The previous script is just modified a little to make it easier to import it's functions and use it in the maze_bot.py script.  
**log**  
This folder contains the log files for running short_path_finder.py.  
**log2**  
This folder contains the log files for running maze_solver.py.  
**visualization**  
This folder contains a blender file and a python script. The blender file runs the python script to generate a scene that replicates the agents perfomance. The agents perfomance is recorded in a pickle file. The pickle file is in the log2\maps_pos folder.
<p align="center">
  <img src="visualization/viz_gif.gif?raw=true" alt="animated" />
</p>


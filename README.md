# VoterModel-Thesis
####Voter Model created for my master degree.

#####Main assumptions of the model.
1. In Poland smallest administrative division is gmina
2. Within each gmina a metapopulation of agents is created.
3. Each agent has two possible political opinions:

a) conservatism - represented with value True

b) anticonservatism - represented with False

4. Within each gmina every agent is connected with every other agents.
5. Based on statistical data, a portion of people that commute to work to other gminas have also connection to agents inside the gmina they commute to.
6. Connected agents can exchange their political opinion with probability p in each step.

ModelClass is the main class of the project. It represents whole state of a simulation. Within this object a vector of opinions of every agent is contained.
Moreover it contains a dictionary of GminaClass objects.
Gmina class represents a gmina within Poland. It contains a vector of indices of gmina residents as well as a vector of people that work inside Gmina.
Aoart from that GminaClass instance contains its TERYT code - which is official polish gmina ID.
Moreover each GminaClass contains 2 vectors of Boolean values, first representing opinions of agents and the other 
representing gminas ID where they commute to.

How to run a simulation:
1. Create an instance of ModelClass. Constructor requires user to provide a file with gmina's populations with the
 format presented in the file "gminas_pops_python2005.csv" which is appended to this git project and is a default input file. 
 Apart from that, it is possible to define level of noise (parameter D of range from 0 to 1), 
 probability of interaction at home, rather than with coworkers (parameter alfa) and downscale factor (the number by which the population of each gmina is divided).
2. Next we have to create population of agents and initialise their connections using populate_agents() method.
The methond has to be fed a file in the format presented in "tabela_przeplywy2016_python.csv" which is appended to this project and is a default input file.
3. Use method model_timestep() to carry out one timestep of the simulation.

ModelClass.model_timestep() performs an asynchronous timestep which means that during simulation agents states are directly overriten in ModelClass object after interaction. 



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


GminaClass is the main class of the project. It represents the metapopulation within a Gmina.
Each instance contains its TERYT code - which is official polish gmina ID.
Moreover each GminaClass contains 2 vectors of Boolean values, first representing opinions of agents and the other 
representing gminas ID where they commute to.


To save actual state one should use function ModelClass.dump_actual_state(filename).
The function will save actual state of the system to two files: filenameopinions.txt and filenameconnections.npz

To retrieve the state from these files feed the files to the constructor of ModelClass using parameter recall_state=False.
Example:
model2005 = ModelClass("mymodelopinions.txt","mymodelconnections.npz" , recall_state=True)





Fuction ModelClass.gmina_timestep(TERYT_CODE) - is responsible for conducting synchronous simulation for whole gmina of given teryt code.
Each agent is has its interaction executed with randomly chosen other agent.  
Function returns new GminaClass object, rather than working on the instance itself.

To simulate every gmina in the model one should use ModelClass.model_timestep_synchronous() for synchronous simulation. (Working od class instance copy.)
In the other hand there is ModelClass.model_timestep_nonsynchronous() function which performs partially synchronous simulation. 
This function runs gmina_timestep() function and saves its outcomes instantly to ModelClass instance. This means that on the gmina level the simulation is synchronous, but then gmina is overwritten and another gminas use newly calculated values of that gmina.
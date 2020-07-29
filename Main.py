from ModelClass import ModelClass
from GminaClass import GminaClass
import pandas as pd
import numpy as np
from sys import getsizeof
import time

kwiatuszek = GminaClass("0700880",6900,0.5,69)
print(kwiatuszek)
winogronko = ModelClass()
winogronko.populate_agents()
print("pracusie")
print(winogronko.gminas["020202"].workers_indices)
print("mieszkancy")
print(winogronko.gminas["020202"].residents_indices)

#
# start = time.time()
#
# model2005 = ModelClass(D = 0.03)
# model2005.dump_actual_state("example")
# model2005_test = ModelClass("exampleopinions.txt","exampleconnections.npz" , recall_state=True)
# end = time.time()
# print(end - start)
#
# # print(model2005.gminas["020202"])
# print(model2005_test.gminas["020202"])
# start = time.time()
# model2005.model_timestep_nonsynchronous()
# print(model2005.gminas["020202"])
# model2005.get_sd()
# model2005.model_timestep_nonsynchronous()
# print(model2005.gminas["020202"])
# model2005.get_sd()
# model2005.model_timestep_nonsynchronous()
# print(model2005.gminas["020202"])
# model2005.get_sd()
# model2005.model_timestep_nonsynchronous()
# print(model2005.gminas["020202"])
# model2005.get_sd()
# end = time.time()
# print(end - start)
#
#

from ModelClass import ModelClass
from GminaClass import GminaClass
import pandas as pd
import numpy as np
from sys import getsizeof
import time

d_value = 0.02
start = time.time()
winogronko = ModelClass(D=d_value,)
winogronko.populate_agents()
stop = time.time()
print("inicjalizacja:")
print(stop-start)
for i in winogronko.gminas["020202"].residents_indices:
    print(winogronko.agents[i])
print(winogronko.gminas["020202"].conservatists)
konserwa = 0
for i in winogronko.gminas["020202"].residents_indices:
    if winogronko.agents[i].opinion:
        konserwa = konserwa + 1
print(konserwa)

winogronko.model_timestep()

print(winogronko.gminas["020202"].conservatists)
konserwa = 0
for i in winogronko.gminas["020202"].residents_indices:
    if winogronko.agents[i].opinion:
        konserwa = konserwa + 1
print(konserwa)


# odchylenia = []
# srednie = []
# srednie_na_poziomie_gminy =[]
#
#
# for i in range(100):
#     start = time.time()
#     winogronko.model_timestep()
#     stop = time.time()
#     print("statystyki")
#     print(stop-start)
#     print()
#     print(winogronko.gminas["020202"])
#     odchylenia.append(winogronko.std_dev)
#     srednie.append(winogronko.overall_conservatism_support)
#     srednie_na_poziomie_gminy.append(winogronko.mean_conservatism_in_gminas)
#
#
# rozklad_poparc_w_gminach = winogronko.conservatism_in_gminas
# file_out = open('d_'+str(d_value)+'_sdev.txt', 'w')
# print(odchylenia, file=file_out)
# file_out2 = open('opinions_' + str(d_value) + '.txt', 'w')
# print(rozklad_poparc_w_gminach, file=file_out2)
# file_out3 = open('means_' + str(d_value) + '.txt', 'w')
# print(srednie_na_poziomie_gminy, file=file_out3)
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

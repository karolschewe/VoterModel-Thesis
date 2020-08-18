from ModelClass import ModelClass
from GminaClass import GminaClass
import pandas as pd
import numpy as np
from sys import getsizeof
import time
import matplotlib.pyplot as plt

# opinia od wielkosci
# roznice pomiedzy polaczonymi gminami
# opinie "na biezaco"
# opinie od procenta wyjezdzajacych

d_value = 0.1
zmniejszenie = 100
start = time.time()
winogronko = ModelClass(D=d_value,downscale_factor=zmniejszenie)
winogronko.populate_agents()
stop = time.time()
print("d:" + str(d_value))
print("factor:" + str(zmniejszenie))
print("czas utworzenia modelu:")
print(stop-start)
test = winogronko.opinion_of_percent_of_outgoers()
plt.scatter(x=test.x,y=test.y)
plt.show()

start = time.time()
for i in range(30):
    winogronko.model_timestep()
stop = time.time()
print("iteracja modelu trwala:")
print(stop-start)
print("liczba agentow:")
print(len(winogronko.agents))
test = winogronko.opinion_of_percent_of_outgoers()
plt.scatter(x=test.x,y=test.y)
plt.show()


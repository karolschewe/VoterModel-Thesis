from ModelClass import ModelClass
import pandas as pd
import numpy as np
from sys import getsizeof
import time

start = time.time()

model2005 = ModelClass()
model2005.dump_actual_state("example")
model2005_test = ModelClass("exampleopinions.txt","exampleconnections.npz" , recall_state=True)
end = time.time()
print(end - start)

print(model2005.gminas["020202"])
print(model2005_test.gminas["020202"])
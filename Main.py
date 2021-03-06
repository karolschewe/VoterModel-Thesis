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
# policzylem sobie srednia sigme z momentu ustabilizowania sie szeregu czasowego odchylenia standardowewgo(od 30 kroku)
# wynika z tego, ze dla wyborow 2005 (sigma 11.2%) najlepsze jest D = 0.08, gdzie sigma wyniosła: 0.1121048
# dla lat 2007-2015 (sigma 12.5% - 12.8%) najlepiej wybrac D:0.06, gdzie srednie odchylenie: 0.1241983
# dla 2019 roku sigma równa: 13.6%, wartość D = 0.05 jest za mała, a 0.04 zbyt duża, prawdopodobnie najlepiej wziąć 0.045

# jak skala zmniejszenia (factor) i d (szum) wspoldzialaja na sigme i korelacje
# zrobic wykres (dwuwymiarowy) sigmy od factora i d
# zrobic wykres (3D) wspolczynnika nachylenia prostej y = ax+b gdzie y jest korelacja, a x jest log(r)

d_value = 0.0001
zmniejszenie = 6
korelacje = []
for i in range(10):
    start = time.time()
    winogronko = ModelClass(D=d_value, downscale_factor=zmniejszenie)
    winogronko.populate_agents()
    for kkk in range(50):
        winogronko.model_timestep()
    corr = winogronko.investigate_correlation(new=True)
    korelacje.append(corr)
    print(korelacje[i])
    stop = time.time()
    print("d:" + str(d_value))
    print("factor:" + str(zmniejszenie))
    print("czas utworzenia modelu:")
    print(stop - start)
print(korelacje)
print(np.mean(korelacje,axis=0))
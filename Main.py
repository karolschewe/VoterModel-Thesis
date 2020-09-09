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

d_value = 0.01
zmniejszenie = 100
start = time.time()
winogronko = ModelClass(D=d_value,downscale_factor=zmniejszenie)
winogronko.populate_agents()
stop = time.time()
print("d:" + str(d_value))
print("factor:" + str(zmniejszenie))
print("czas utworzenia modelu:")
print(stop-start)


print("korelacje stare")
# print(winogronko.investigate_correlation())
print("funkcja nowa")
print(winogronko.investigate_correlation(new=True))

# test = winogronko.percent_of_outgoers_of_size()
# test2 = winogronko.percent_of_incomers_of_size()



# plt.scatter(x=test.x,y=test.y,s=8,alpha=0.5)
# plt.title("wykres procenta wyjezdajacych od populacji gminy")
# plt.xlabel("liczba agentow w gminie")
# plt.ylabel("ulamek wyjezdzajacych agentow")
# plt.show()
# plt.scatter(x=test2.x,y=test2.y,s=8,alpha=0.5)
# plt.title("wykres procenta przyjezdzajacych od populacji gminy")
# plt.ylabel("l.przyjezdzajacych do pracy/l.agentow w gminie")
# plt.xlabel("liczba agentow w gminie")
# plt.show()
start = time.time()
for i in range(30):
    winogronko.model_timestep(noise_type="nondefault")
stop = time.time()
print("iteracja modelu trwala:")
print(stop-start)



print(winogronko.investigate_correlation(new=True))
# print("liczba agentow:")
# print(len(winogronko.agents))
# test = winogronko.percent_of_outgoers_of_size()
# test2 = winogronko.percent_of_incomers_of_size()
# plt.scatter(x=test.x,y=test.y)
# plt.title("wykres procenta wyjezdajacych od populacji gminy")
# plt.xlabel("populacja gminy")
# plt.show()
# plt.scatter(x=test2.x,y=test2.y)
# plt.title("wykres procenta przyjezdzajacyc od populacji gminy")
# plt.xlabel("populacja gminy")
# plt.show()

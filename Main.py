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

start = time.time()
winogronko = ModelClass(D=d_value)
stop = time.time()
print("d:" + str(d_value))
print("czas utworzenia modelu:")
print(stop-start)

print(winogronko.conservatism_in_gminas())
# czy nie uwazasz ze korelacja powinna wyjsc taka sama???
start = time.time()
# print(winogronko.investigate_correlation())
print(winogronko.gminas_pops)
corr = winogronko.investigate_correlation()
print(corr)
plt.scatter(y=corr,x=winogronko.breakpoints)
plt.show()

polaczenia_dict = {}
for i in winogronko.gminas_neighbours.values():
    for odleglosc, polaczenia in i.items():
        if not odleglosc in polaczenia_dict.keys():
            polaczenia_dict[odleglosc] = 0
        polaczenia_dict[odleglosc] = polaczenia_dict[odleglosc] + len(polaczenia)

print("liczba polaczen")
print(polaczenia_dict)

stop = time.time()
print("czas korelacja:")
print(stop-start)


# korelacje cos za dlugo sie kreca :/
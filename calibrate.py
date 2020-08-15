from ModelClass import ModelClass
import time
import os
from pathlib import Path

cwd = os.getcwd()
d_values = [0,0.01,0.02,0.03,0.04,0.05,0.1,0.15,0.2,0.25]
# d_values = [0.1,0.15,0.2,0.25]
downscale_factors = [38,100]
liczba_iteracji = 100
# d_values = [0.1]

for i in d_values:
    for j in downscale_factors:
        directory = cwd + "\data\d_"+str(i) + "_scale_" + str(j)
        pth = Path(directory)
        pth.mkdir(exist_ok=True,parents=True)
        start = time.time()

        model = ModelClass(D=i,downscale_factor=j)
        model.populate_agents()

        odchylenia = []
        srednie = []
        srednie_na_poziomie_gminy = []
        new_file = open(directory + '\d_' + str(i) + '_opinion_dist_of_time.txt', 'w')

        for g in range(liczba_iteracji):
            start2 = time.time()
            model.model_timestep()
            odchylenia.append(model.std_dev)
            srednie.append(model.overall_conservatism_support)
            srednie_na_poziomie_gminy.append(model.mean_conservatism_in_gminas)
            stop2 = time.time()
            if g % 5 == 0:
                print("Iteracja modelu:" + str(g))
                print("Czas wykonania 1 iteracji:")
                print(stop2-start2)
                rozklad = model.conservatism_in_gminas
                print(g, file=new_file)
                print(rozklad,file=new_file)

        rozklad_poparc_w_gminach = model.conservatism_in_gminas


        file_out = open(directory + '\d_' + str(i) + '_sdev.txt', 'w')
        print(odchylenia, file=file_out)
        file_out2 = open(directory+'\opinions_' + str(i) + '.txt', 'w')
        print(rozklad_poparc_w_gminach, file=file_out2)
        file_out3 = open(directory+'\means_' + str(i) + '.txt', 'w')
        print(srednie_na_poziomie_gminy, file=file_out3)
        file_out4 = open(directory + '\mean_overall_' + str(i) + '.txt', 'w')
        print(srednie, file=file_out4)

        stop = time.time()
        print("Model o wspolczynniku D: " + str(i) + " oraz skali zmniejszenia: " + str(j) + " \nwykonal " +
              str(liczba_iteracji) + " iteracji w " +str(stop-start) + " sekund")



from ModelClass import ModelClass
import time
import os
from pathlib import Path

cwd = os.getcwd()
# d_values = [0,0.01,0.02,0.03,0.04,0.05,0.1,0.15,0.2,0.25]
d_values = [0,0.01,0.03,0.2]
downscale_factors = [38,100]
liczba_iteracji = 80
noise_types = ["symmetric","other"]
# d_values = [0.1]

for noise in noise_types:
    for i in d_values:
        for j in downscale_factors:
            directory = cwd + "\data\d_" + str(i) + "_scale_" + str(j)
            if noise != "symmetric":
                directory = cwd + "\data\d_" + str(i) + "_scale_" + str(j) + "noise_change"
            pth = Path(directory)
            pth.mkdir(exist_ok=True, parents=True)
            start = time.time()

            model = ModelClass(D=i, downscale_factor=j)
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
                if g % 10 == 0:
                    print("Iteracja modelu:" + str(g))
                    print("Czas wykonania 1 iteracji:")
                    print(stop2 - start2)
                    rozklad = model.conservatism_in_gminas
                    print(g, file=new_file)
                    print(rozklad, file=new_file)

            rozklad_poparc_w_gminach = model.conservatism_in_gminas
            rokzlad_roznic_opinii = model.rokzlad_roznic()
            opinia_od_wielkosci = model.opinion_of_gmina_size()
            opinia_od_procenta_wyjezdzajacych = model.opinion_of_percent_of_outgoers()


            file_out = open(directory + '\d_' + str(i) + '_sdev.txt', 'w')
            print(odchylenia, file=file_out)
            file_out2 = open(directory + '\opinions_' + str(i) + '.txt', 'w')
            print(rozklad_poparc_w_gminach, file=file_out2)
            file_out3 = open(directory + '\means_' + str(i) + '.txt', 'w')
            print(srednie_na_poziomie_gminy, file=file_out3)
            file_out4 = open(directory + '\mean_overall_' + str(i) + '.txt', 'w')
            print(srednie, file=file_out4)
            file_out5 = open(directory + '\opinion_diffs_' + str(i) + '.txt', 'w')
            print(rokzlad_roznic_opinii, file=file_out5)
            file_out6 = open(directory + '\opinion_of_size_' + str(i) + '.txt', 'w')
            print(opinia_od_wielkosci.x, file=file_out6)
            print(opinia_od_wielkosci.y, file=file_out6)
            file_out7 = open(directory + '\opinion_of_outgoers_' + str(i) + '.txt', 'w')
            print(opinia_od_procenta_wyjezdzajacych.x, file=file_out7)
            print(opinia_od_procenta_wyjezdzajacych.y, file=file_out7)

            stop = time.time()
            print("Model o wspolczynniku D: " + str(i) + " oraz skali zmniejszenia: " + str(j) + " \nwykonal " +
                  str(liczba_iteracji) + " iteracji w " + str(stop - start) + " sekund")

from ModelClass import ModelClass
import time
import os
from pathlib import Path

cwd = os.getcwd()
d_values = [0,0.01,0.03,0.08]
downscale_factors = [1]
liczba_iteracji = 5000
noise_types = ["other"]
# d_values = [0.1]

for noise in noise_types:
    for i in d_values:
        for j in downscale_factors:
            directory = cwd + "\data_mean_field_by_gmina_long\d_" + str(i)
            if noise != "symmetric":
                directory = cwd + "\data_mean_field_by_gmina_long\d_" + str(i)  + "noise_change"
            pth = Path(directory)
            pth.mkdir(exist_ok=True, parents=True)
            start = time.time()

            model = ModelClass(D=i)

            odchylenia = []
            srednie = []
            srednie_na_poziomie_gminy = []
            new_file = open(directory + '\d_' + str(i) + '_corr_of_time.txt', 'w')
            correlations = model.investigate_correlation()
            print(0, file=new_file)
            print(correlations, file=new_file)
            for g in range(liczba_iteracji):
                start2 = time.time()
                model.model_timestep()
                odchylenia.append(model.sigma_conservatism)
                srednie.append(model.actual_conservatism_support)
                srednie_na_poziomie_gminy.append(model.mean_conservatism)
                stop2 = time.time()
                if g % 10 == 9:
                    print("Iteracja modelu:" + str(g))
                    print("Czas wykonania 1 iteracji:")
                    print(stop2 - start2)
                    correlations = model.investigate_correlation()
                    print(g, file=new_file)
                    print(correlations, file=new_file)
                    if model.check_if_interrupted() == True:
                        break


            rozklad_poparc_w_gminach = model.conservatism_distribution
            correlations = model.investigate_correlation()


            file_out = open(directory + '\d_' + str(i) + '_sdev.txt', 'w')
            print(odchylenia, file=file_out)
            file_out2 = open(directory + '\opinions_' + str(i) + '.txt', 'w')
            print(rozklad_poparc_w_gminach, file=file_out2)
            file_out3 = open(directory + '\means_' + str(i) + '.txt', 'w')
            print(srednie_na_poziomie_gminy, file=file_out3)
            file_out4 = open(directory + '\mean_overall_' + str(i) + '.txt', 'w')
            print(srednie, file=file_out4)
            file_out8 = open(directory + '\spatial_correlation_' + str(i) + '.txt', 'w')
            print(correlations, file=file_out8)

            stop = time.time()
            print("Model o wspolczynniku D: " + str(i) + " oraz skali zmniejszenia: " + str(j) + " \nwykonal " +
                  str(liczba_iteracji) + " iteracji w " + str(stop - start) + " sekund")

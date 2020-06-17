from GminaClass import GminaClass
import pandas as pd
import numpy as np

class ModelClass:
    gminas = {}

    def __init__(self,initial_state_filename: str = "gminas_pops_python2005.csv", travellers_filename: str = "tabela_przeplywy2016_python.csv", recall_state =False):
        if not recall_state:
            initial_state = pd.read_csv(initial_state_filename, dtype={'TERYT': str})
            travellers = pd.read_csv(travellers_filename, dtype={'FROM': str, 'TO': str})
            for idx, row in initial_state.iterrows():
                self.gminas[row['TERYT']] = GminaClass.from_textfile(teryt_code=row['TERYT'],
                                                                     population=row['POPULACJA'],
                                                                     conservatism_support=row['APPROX_PERCENTAGE'],
                                                                     downscale_factor=38)
                self.gminas[row['TERYT']].initialize_workplaces(travellers)
        else:
            with open(initial_state_filename, "r") as file:
                downscale_factor = file.readline()
                while True:
                    teryt = file.readline().strip("\n")
                    # print(teryt)
                    if not teryt:
                        break
                    conservatives = file.readline()
                    others = file.readline()
                    self.gminas[teryt] = GminaClass(teryt, int(conservatives), int(others), int(downscale_factor))
            temp = np.load(travellers_filename)
            for index, value in self.gminas.items():
                value.working_gmina = temp[index]




    # aktualny stan modelu wyrzucany jest do 2 plikow
    # pierwszy plik -- zawiera stany agentow w formacie: TERYT \n liczba konserwatystów \n liczba pozostalych
    # drugi plik zawiera wektory polaczen ( w znanym juz formacie 'S' - dla braku polaczen agenta poza gminą i 'TERYT' dla posiadajacych takowe)

    def dump_actual_state(self, filename: str):
        first = True
        with open(filename+"opinions.txt","w") as file:
            for i in self.gminas.values():
                unique, counts = np.unique(i.voters_states, return_counts=True)
                dd = dict(zip(unique, counts))
                conservatists = dd[True]
                others = dd[False]
                if first:
                    file.write(str(i.factor)+"\n")
                    first = False
                file.write(i._teryt_ + "\n")
                file.write(str(conservatists) + "\n")
                file.write(str(others) + "\n")


        temp = {}
        for i in self.gminas.values():
            temp[i._teryt_] = i.working_gmina
        np.savez_compressed(filename+"connections.npz", **temp)







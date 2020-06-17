import random
from random import sample

from GminaClass import GminaClass
import pandas as pd
import numpy as np
from copy import deepcopy

class ModelClass:
    alfa = 0.5 # prawdopodobienstwo wybrania agenta z wlasnej gminy do interakcji w danym kroku
    D = 1 # prawdopodobienstwo zmiany zdania
    gminas = {}

    def __init__(self,initial_state_filename: str = "gminas_pops_python2005.csv", travellers_filename: str = "tabela_przeplywy2016_python.csv", recall_state=False, D = 1, alfa =0.5):
        # inicjalizacja z pliku zawierajacego stan poczatkowy
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
            # wczytywanie z sejwa
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
        self.D = D
        self.alfa = alfa




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
            true_val_first = np.concatenate((i.working_gmina[np.where(i.voters_states == True)], i.working_gmina[np.where(i.voters_states == False)]), axis=None)
            temp[i._teryt_] = true_val_first
        np.savez_compressed(filename+"connections.npz", **temp)

    # funkcja wykonujaca synchroniczna symulacje dla jednej gminy
    def gmina_timestep(self, gminas_teryt: str):
        #stworzenie kopii obiektu, aby poprzednie kontakty nie wplywaly symulacje w tym samym kroku
        temp = deepcopy(self.gminas[gminas_teryt])
        # iteracja po wszystkich agentach
        for i in range(temp.n_agents):
            # jezeli agent pracuje w tej samej gminie to mamy tylko mozliwowsc kontaktu w tej samej gminie
            if temp.working_gmina[i] == "S":
                mate_index = sample(range(temp.n_agents), 1) #losujemy jeden indeks agenta z ktorym bedziemy wchodzic w interakcje
                mate_opinion = temp.voters_states[mate_index]
                if mate_opinion != temp.voters_states[i]:
                    if random.random() < self.D: # zmiana opinii z prawdopodobienstwem D
                        temp.voters_states[i] = mate_opinion
            else:
                if random.random() > self.alfa:
                    TERYT_conn = temp.working_gmina[i] #wyciagam sobie teryt gminy polaczonej z agentem
                    mate_index = sample(range(self.gminas[TERYT_conn].n_agents), 1)
                    mate_opinion = self.gminas[TERYT_conn].voters_states[mate_index]
                    if mate_opinion != temp.voters_states[i]:
                        if random.random() < self.D:
                            temp.voters_states[i] = mate_opinion
                else: # z prawdopodobienstwem alfa agent wchodzi w interakcje z kontaktem ze swojej gminy
                    mate_index = sample(range(temp.n_agents), 1)
                    mate_opinion = temp.voters_states[mate_index]
                    if mate_opinion != temp.voters_states[i]:
                        if random.random() < self.D:
                            temp.voters_states[i] = mate_opinion


        return temp

    # funkcja wykonujaca symulacje synchronicznie na wszystkich gminach instancji model
    # funkcja nadpisuje stan modelu dopiero po tym jak wszystkie gminy zostana obliczone
    def model_timestep_synchronous(self):
        temp_gminas = {} # dzialamy na kopii
        for teryt in self.gminas.keys():
            temp_gminas[teryt] = self.gmina_timestep(teryt)

        self.gminas = temp_gminas #nadpisujemy stan modelu

    # funkcja wykonujaca symulacje czesciowo asynchronicznie na wszystkich gminach instancji model
    # funkcja nadpisuje stan modelu co kazde wykonanie funkcji gmina_timestep(teryt)
    # w rzeczywistosci oznacza to ze obliczenia wewnatrz gminy wykonuja sie synchronicznie, ale po obliczeniu jednej gminy stan modelu jest zapisywany
    # i wyedytowana gmina jest wykorzystywana w obliczeniach dla pozostalych gmin
    def model_timestep_nonsynchronous(self):
        for teryt in self.gminas.keys():
            tmp = self.gmina_timestep(teryt)
            self.gminas[teryt] = tmp

    def set_D(self,probability_of_opinion_change: float = 1):
        self.D = probability_of_opinion_change













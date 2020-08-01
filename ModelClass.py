import random
from random import sample
from statistics import stdev
from GminaClass import GminaClass
import pandas as pd
import numpy as np
from statistics import mean

# zrobic dotychczasowe symulacje
# zrobic sprawdzenie wariancji od skali zmniejszenia


class ModelClass:
    alfa = 0.5 # prawdopodobienstwo wybrania agenta z wlasnej gminy do interakcji w danym kroku
    D = 1 # prawdopodobienstwo losowej zmiany zdania
    downscale_factor = 38
    gminas = {}
    agents = []

    def populate_agents(self,travellers_df_filename = "tabela_przeplywy2016_python.csv"): # this function is intended to run only inside ModelClass constructor AFTER gimna class initialisation
        commuters = pd.read_csv(travellers_df_filename, dtype={'FROM': str, 'TO': str})
        assigned_agents = 0
        for i in self.gminas.values():
            where_to = commuters.loc[commuters['FROM'] == i.id] # wybieram wiersze dla i-tej gminy
            vector_of_workplaces = []
            for idx, row in where_to.iterrows():
                how_many_bois = round(row['n'] / self.downscale_factor) # ile ziomkow po przeskalowaniu bedzie pracowac w innych gminach
                to = [row['TO']]
                vector_of_workplaces.extend(to * how_many_bois) # append numerow gmin do wektora
            how_many_more = i.n_agents - len(vector_of_workplaces)
            vector_of_workplaces.extend([i.id] * how_many_more) # "dopelniam" reszte agentow do wektora
            vector_of_workplaces = sample(vector_of_workplaces,i.n_agents)
            vector_of_opinions = sample(i.conservatists * [True] + (i.n_agents - i.conservatists) * [False],i.n_agents) #losowo przydzielam opinie
            for iterator in range(len(vector_of_workplaces)):
                self.agents.append(vector_of_opinions[iterator])
                i.residents_indices.append(assigned_agents)
                self.gminas[vector_of_workplaces[iterator]].workers_indices.append(assigned_agents)
                assigned_agents = assigned_agents + 1

    def __init__(self,initial_state_filename: str = "gminas_pops_python2005.csv", D = 0.1, alfa =0.5):
        # inicjalizacja z pliku zawierajacego stan poczatkowy

        initial_state = pd.read_csv(initial_state_filename, dtype={'TERYT': str})
        for idx, row in initial_state.iterrows():
            self.gminas[row['TERYT']] = GminaClass(teryt_code=row['TERYT'],
                                                                 population=row['POPULACJA'],
                                                                 conservatism_support=row['APPROX_PERCENTAGE'],
                                                                 downscale_factor=self.downscale_factor)


        self.D = D
        self.alfa = alfa

    # krok modelu ansynchronicznie
    # tzn. Opinie agentow nadpisywane sa w trakcie (nie pracujemy na kopii obiektu)
    def model_timestep(self):
        for i in self.gminas.values(): #iteracja po gminach
            i.conservatists = 0
            for habitant in i.residents_indices:
                if random.random() < self.D:
                    self.agents[habitant] = not self.agents[habitant]
                if random.random() < self.alfa:  # interacja z mieszkancami
                    who_is_contacted = sample(i.residents_indices, 1)[0]
                    self.agents[habitant] = self.agents[who_is_contacted]
                else:  # interakcja w pracy
                    who_is_contacted = sample(i.workers_indices, 1)[0]
                    self.agents[habitant] = self.agents[who_is_contacted]
                if self.agents[habitant]:
                    i.conservatists = i.conservatists+1



    # aktualny stan modelu wyrzucany jest do 2 plikow
    # pierwszy plik -- zawiera stany agentow w formacie: TERYT \n liczba konserwatystów \n liczba pozostalych
    # drugi plik zawiera wektory polaczen ( w znanym juz formacie 'S' - dla braku polaczen agenta poza gminą i 'TERYT' dla posiadajacych takowe)

    # def dump_actual_state(self, filename: str):
    #     first = True
    #     with open(filename+"opinions.txt","w") as file:
    #         for i in self.gminas.values():
    #             unique, counts = np.unique(i.voters_states, return_counts=True)
    #             dd = dict(zip(unique, counts))
    #             conservatists = dd[True]
    #             others = dd[False]
    #             if first:
    #                 file.write(str(i.factor)+"\n")
    #                 first = False
    #             file.write(i._teryt_ + "\n")
    #             file.write(str(conservatists) + "\n")
    #             file.write(str(others) + "\n")
    #
    #
    #     temp = {}
    #     for i in self.gminas.values():
    #         true_val_first = np.concatenate((i.working_gmina[np.where(i.voters_states == True)], i.working_gmina[np.where(i.voters_states == False)]), axis=None)
    #         temp[i._teryt_] = true_val_first
    #     np.savez_compressed(filename+"connections.npz", **temp)
    #
    # # funkcja wykonujaca synchroniczna symulacje dla jednej gminy
    # def gmina_timestep(self, gminas_teryt: str):
    #     #stworzenie kopii obiektu, aby poprzednie kontakty nie wplywaly symulacje w tym samym kroku
    #     temp = deepcopy(self.gminas[gminas_teryt])
    #     # iteracja po wszystkich agentach
    #     for i in range(temp.n_agents):
    #
    #         if random.random() < self.D:
    #             temp.voters_states[i] = not temp.voters_states[i]
    #         # jezeli agent pracuje w tej samej gminie to mamy tylko mozliwowsc kontaktu w tej samej gminie
    #         if temp.working_gmina[i] == "S":
    #             mate_index = sample(range(temp.n_agents), 1) #losujemy jeden indeks agenta z ktorym bedziemy wchodzic w interakcje
    #             mate_opinion = temp.voters_states[mate_index]
    #             if mate_opinion != temp.voters_states[i]:
    #                 temp.voters_states[i] = mate_opinion
    #         else:
    #             if random.random() > self.alfa:
    #                 TERYT_conn = temp.working_gmina[i] #wyciagam sobie teryt gminy polaczonej z agentem
    #                 mate_index = sample(range(self.gminas[TERYT_conn].n_agents), 1)
    #                 mate_opinion = self.gminas[TERYT_conn].voters_states[mate_index]
    #                 if mate_opinion != temp.voters_states[i]:
    #                     temp.voters_states[i] = mate_opinion
    #             else: # z prawdopodobienstwem alfa agent wchodzi w interakcje z kontaktem ze swojej gminy
    #                 mate_index = sample(range(temp.n_agents), 1)
    #                 mate_opinion = temp.voters_states[mate_index]
    #                 if mate_opinion != temp.voters_states[i]:
    #                     temp.voters_states[i] = mate_opinion
    #
    #
    #     return temp
    #
    # # funkcja wykonujaca symulacje synchronicznie na wszystkich gminach instancji model
    # # funkcja nadpisuje stan modelu dopiero po tym jak wszystkie gminy zostana obliczone
    # def model_timestep_synchronous(self):
    #     temp_gminas = {} # dzialamy na kopii
    #     for teryt in self.gminas.keys():
    #         temp_gminas[teryt] = self.gmina_timestep(teryt)
    #
    #     self.gminas = temp_gminas #nadpisujemy stan modelu
    #
    # # funkcja wykonujaca symulacje czesciowo asynchronicznie na wszystkich gminach instancji model
    # # funkcja nadpisuje stan modelu co kazde wykonanie funkcji gmina_timestep(teryt)
    # # w rzeczywistosci oznacza to ze obliczenia wewnatrz gminy wykonuja sie synchronicznie, ale po obliczeniu jednej gminy stan modelu jest zapisywany
    # # i wyedytowana gmina jest wykorzystywana w obliczeniach dla pozostalych gmin
    # def model_timestep_nonsynchronous(self):
    #     for teryt in self.gminas.keys():
    #         tmp = self.gmina_timestep(teryt)
    #         self.gminas[teryt] = tmp
    #
    def set_D(self,probability_of_opinion_change: float = 1):
        self.D = probability_of_opinion_change


    #
    # def get_sd(self):
    #     tmp_support = self.get_support()
    #     sd = stdev(tmp_support)
    #     print("Odchylenie standardowe rozkladu poparc gmin:"+str(sd))
    #     return sd
    #
    #
    @property
    def conservatism_in_gminas(self):
        tmp_support = []
        for i in self.gminas.values():
            tmp_support.append(i.conservatists / i.n_agents)
        return tmp_support
    @property
    def mean_conservatism_in_gminas(self):
        return mean(self.conservatism_in_gminas)
    @property
    def overall_conservatism_support(self):
        mn = sum(self.agents)/len(self.agents)
        print("Konserwatyzm w Polsce popiera " + str(round(mn*100,2)) + "% osob")
        return mn
    @property
    def std_dev(self):
        sd = stdev(self.conservatism_in_gminas)
        print("Odchylenie standardowe rozkladu poparc gmin:" + str(sd))
        return sd
    def __str__(self):
        return "Number of conservatists: " + str(sum(self.agents))











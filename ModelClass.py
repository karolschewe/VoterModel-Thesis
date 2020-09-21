import random
from random import sample
from statistics import stdev
from GminaClass import GminaClass
import pandas as pd
import numpy as np
from statistics import mean
from AgentClass import Agent
from PocketClass import Pocket

# jak w modelu sredniopolowym ustalana byla poczatkowa opinia ludzi dojezdzajacych do innych gmin?
# prawdopodobnie taki sam procent jak dla mieszkancow w gminie w ktorej mieszkali
# biorac pod uwage zmniejszenie o factor i srednia liczbe wyjazdow z gminy a do b mozna zaryzykowac stwierdzenie,
# ze opinie dojezdzajacych nie byly reprezentatywne dla danej gminy
# czy jezeli mieszkancy byli nierozroznialni to czy po iteracji mogla byc ulamkowa liczba konserwatystow?


class ModelClass:
    alfa = 0.5 # prawdopodobienstwo wybrania agenta z wlasnej gminy do interakcji w danym kroku
    D = 1 # prawdopodobienstwo losowej zmiany zdania
    # downscale_factor = 38
    # gminas = {}
    # agents = [] # obiektow klasy agent zawierajacych miejsce opinie, miejsce zamieszkania i miejsce pracy
    class Plot:
        def __init__(self,x,y):
            if len(x) == len(y):
                self.x = x
                self.y = y
            else:
                print("x is not the same length as y")
                raise TypeError


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
            i.percent_of_outgoers = len(vector_of_workplaces)/i.n_agents # dodanie procenta kolesi pracujacych poz gmina
            vector_of_workplaces.extend([i.id] * how_many_more) # "dopelniam" reszte agentow do wektora
            vector_of_workplaces = sample(vector_of_workplaces,i.n_agents)
            vector_of_opinions = sample(i.conservatists * [True] + (i.n_agents - i.conservatists) * [False],i.n_agents) #losowo przydzielam opinie
            for iterator in range(len(vector_of_workplaces)):
                self.agents.append(Agent(vector_of_opinions[iterator], i.id, vector_of_workplaces[iterator]))
                i.residents_indices.append(assigned_agents)
                self.gminas[vector_of_workplaces[iterator]].workers_indices.append(assigned_agents)
                assigned_agents = assigned_agents + 1

    def __init__(self,initial_state_filename: str = "gminas_pops_python2005.csv", D = 0.1, alfa =0.5,
                 dist_matrix_filename : str = "macierz_odleglosci_cut_teryt.csv", include_only_workers = False,
                 travellers_df_filename = "tabela_przeplywy2016_python.csv"):
        # inicjalizacja z pliku zawierajacego stan poczatkowy

        perc_of_pop_working = 1
        if include_only_workers:
            perc_of_pop_working = 16/38

        initial_state = pd.read_csv(initial_state_filename, dtype={'TERYT': str})
        self.D = D
        self.alfa = alfa
        self.pockets = {}
        self.gminas_pops = {}
        self.gminas_workforce = {}
        self.gminas_incomers = {}
        for idx, row in initial_state.iterrows():
            self.pockets[row['TERYT']] = {}
            self.pockets[row['TERYT']][row['TERYT']] = Pocket(homeplace=row['TERYT'],
                                                              workplace = row['TERYT'],
                                                                 population=row['POPULACJA'] * perc_of_pop_working,
                                                                 conservatism=row['APPROX_PERCENTAGE'])
            self.gminas_pops[row['TERYT']] = row['POPULACJA'] * perc_of_pop_working
        commuters = pd.read_csv(travellers_df_filename, dtype={'FROM': str, 'TO': str})
        for idx, row in commuters.iterrows():
            if row['FROM'] in self.pockets.keys():
                self.pockets[row['FROM']][row['TO']] = Pocket(homeplace=row['FROM'], workplace=row['TO'],
                                                              population=row['n'],
                                                              conservatism=self.pockets[row['FROM']][row['FROM']].conservatism)
                self.pockets[row['FROM']][row['FROM']].depopulate(row['n'])
                if row['TO'] in self.gminas_workforce.keys():
                    self.gminas_workforce[row['TO']] = self.gminas_workforce[row['TO']]+row['n']
                else:
                    self.gminas_workforce[row['TO']]=row['n']
                if row['TO'] not in self.gminas_incomers.keys():
                    self.gminas_incomers[row['TO']] = [row['TO']]
                self.gminas_incomers[row['TO']].append(row['FROM'])
        for homeplaces in self.gminas_pops.keys():
            if homeplaces in self.gminas_workforce.keys():
                self.gminas_workforce[homeplaces] = self.gminas_workforce[homeplaces] + self.pockets[homeplaces][homeplaces].population
            else:
                self.gminas_workforce[homeplaces] = self.pockets[homeplaces][homeplaces].population




        tmp_df = pd.read_csv(dist_matrix_filename)
        tmp_df = tmp_df.drop("Unnamed: 0", axis=1)
        tmp_df.index = tmp_df.columns
        self.d_matr = tmp_df

# bez szumu !!!!
    def calculate_pocket_timestep(self,pocket):
        homeplace_interactions = 0
        workplace_interactions = 0
        # iteracja po wszystkich ktorzy mieszkaja w i
        for i in self.pockets[pocket.homeplace].values():
            # przyczynek = populacja populacja mieszkajacych w i oraz pracujacych gdziekolwiek / populacja gminy i
            tmp = i.population/self.gminas_pops[pocket.homeplace]
            # delta kronekera
            if i.workplace == pocket.workplace:
                tmp = tmp - 1
            # przemnozenie przez prawdopodobienstwo interakcji z mieszkancem i opinie pocketa mieszkajacego w i oraz pracujacego gdziekolwiek
            tmp = tmp * self.alfa * i.conservatism
            #sumowanie przyczynkow
            homeplace_interactions = homeplace_interactions + tmp
        # iteracja po wszystkich ktorzy pracuja w j
        for teryt in self.gminas_incomers[pocket.workplace]:
            # przyczynek = przyjezdzajacy skadkolwiek do gminy j / liczba pracujacych w gminie j
            tmp2 = self.pockets[teryt][pocket.workplace].population / self.gminas_workforce[pocket.workplace]
            if pocket.homeplace == teryt:
                tmp2 = tmp2 - 1
            tmp2 = (1 - self.alfa) * tmp2 * self.pockets[teryt][pocket.workplace].conservatism
            workplace_interactions = workplace_interactions + tmp2
        return workplace_interactions + homeplace_interactions

















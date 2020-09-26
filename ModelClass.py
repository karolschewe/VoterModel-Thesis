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




    def __init__(self,initial_state_filename: str = "gminas_pops_python2005.csv", D = 0.1, alfa =0.5,
                 dist_matrix_filename : str = "macierz_odleglosci_cut_teryt.csv", include_only_workers = False,
                 travellers_df_filename = "tabela_przeplywy2016_python.csv",test = False):
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
                                                              workplace=row['TERYT'],
                                                              population=row['POPULACJA'] * perc_of_pop_working,
                                                              conservatism=row['APPROX_PERCENTAGE'])
            self.gminas_pops[row['TERYT']] = row['POPULACJA'] * perc_of_pop_working
        commuters = pd.read_csv(travellers_df_filename, dtype={'FROM': str, 'TO': str})
        for idx, row in commuters.iterrows():
            if row['FROM'] in self.pockets.keys() and not row['FROM'] == row['TO']:
                self.pockets[row['FROM']][row['TO']] = Pocket(homeplace=row['FROM'], workplace=row['TO'],
                                                              population=row['n'],
                                                              conservatism=self.pockets[row['FROM']][
                                                                  row['FROM']].conservatism)
                self.pockets[row['FROM']][row['FROM']].depopulate(row['n'])
                if row['TO'] in self.gminas_workforce.keys():
                    self.gminas_workforce[row['TO']] = self.gminas_workforce[row['TO']] + row['n']
                else:
                    self.gminas_workforce[row['TO']] = row['n']
                if row['TO'] not in self.gminas_incomers.keys():
                    self.gminas_incomers[row['TO']] = [row['TO']]
                self.gminas_incomers[row['TO']].append(row['FROM'])
        for homeplaces in self.gminas_pops.keys():
            if homeplaces in self.gminas_workforce.keys():
                self.gminas_workforce[homeplaces] = self.gminas_workforce[homeplaces] + self.pockets[homeplaces][
                    homeplaces].population
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
        mieszkancy_i = 0
        # iteracja po wszystkich ktorzy mieszkaja w i
        for i in self.pockets[pocket.homeplace].values():
            # przyczynek = populacja populacja mieszkajacych w i oraz pracujacych gdziekolwiek / populacja gminy i
            tmp = i.population/self.gminas_pops[pocket.homeplace]
            mieszkancy_i = mieszkancy_i + i.population
            # delta kronekera
            if i.workplace == pocket.workplace:
                tmp = tmp - 1
            # przemnozenie przez prawdopodobienstwo interakcji z mieszkancem i opinie pocketa mieszkajacego w i oraz pracujacego gdziekolwiek
            tmp = tmp * self.alfa * i.conservatism
            #sumowanie przyczynkow
            homeplace_interactions = homeplace_interactions + tmp
        # iteracja po wszystkich ktorzy pracuja w j
        if pocket.workplace in self.gminas_incomers.keys():
            for teryt in self.gminas_incomers[pocket.workplace]:
                # przyczynek = przyjezdzajacy skadkolwiek do gminy j / liczba pracujacych w gminie j
                if teryt in self.pockets.keys():
                    tmp2 = self.pockets[teryt][pocket.workplace].population / self.gminas_workforce[pocket.workplace]
                    if pocket.homeplace == teryt:
                        tmp2 = tmp2 - 1
                    tmp2 = (1 - self.alfa) * tmp2 * self.pockets[teryt][pocket.workplace].conservatism
                    workplace_interactions = workplace_interactions + tmp2

        return workplace_interactions + homeplace_interactions

    def model_timestep(self):
        for homeplace in self.pockets.values():
            for pocket in homeplace.values():
                pocket.conservatism = pocket.conservatism + self.calculate_pocket_timestep(pocket)
                pocket.recalculate_conservatists()

    @property
    def conservatism_distribution(self):
        tmp = []
        for homeplace in self.pockets.values():
            for pocket in homeplace.values():
                tmp.append(pocket.conservatism)
        return tmp
    @property
    def sigma_conservatism(self):
        return np.std(self.conservatism_distribution)
    @property
    def mean_conservatism(self):
        return mean(self.conservatism_distribution)
    @property
    def actual_conservatism_support(self):
        pop = 0
        conservatists = 0
        for homeplace in self.pockets.values():
            for pocket in homeplace.values():
                pop = pop + pocket.population
                conservatists = conservatists + pocket.conservatists
        return conservatists/pop

    def calculate_spatial_correlation(self,lower_bound_km, upper_bound_km):
        mean_opinion_sq = self.mean_conservatism**2
        sigma_kwadrat = self.sigma_conservatism**2
        correlation_vec = []
        for homeplace in self.pockets.values():
            for pocket in homeplace.values():
                if pocket.homeplace in self.d_matr.columns:
                    neighbours = list(self.d_matr.loc[(self.d_matr[pocket.homeplace]) < upper_bound_km & (self.d_matr[pocket.homeplace]) > lower_bound_km].index)
                    print(neighbours)
                else:
                    continue
                if len(neighbours) > 0:
                    my_opinion = pocket.conservatism
                    opinion_multiplied = []
                    #sredni iloczyn poparc dla wszystkich komorek z zadanego obszaru
                    for teryt in neighbours:
                        if teryt in self.pockets.keys():
                            for cell in self.pockets[teryt].values():
                                tmp = my_opinion * cell.conservatism
                                opinion_multiplied.append(tmp)
                        if len(opinion_multiplied) > 0:
                            mean_in_area = mean(opinion_multiplied)
                            mean_diff = mean_in_area - mean_opinion_sq
                            correlation = mean_diff/sigma_kwadrat
                            correlation_vec.append(correlation)
                        else:
                            continue
        mean_spatial_correlation = mean(correlation_vec)
        return mean_spatial_correlation


















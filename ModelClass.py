import random
from random import sample
from statistics import stdev
from GminaClass import GminaClass
import pandas as pd
import numpy as np
from statistics import mean
from AgentClass import Agent
from PocketClass import Pocket
import keyboard
import time

# jak w modelu sredniopolowym ustalana byla poczatkowa opinia ludzi dojezdzajacych do innych gmin?
# prawdopodobnie taki sam procent jak dla mieszkancow w gminie w ktorej mieszkali
# biorac pod uwage zmniejszenie o factor i srednia liczbe wyjazdow z gminy a do b mozna zaryzykowac stwierdzenie,
# ze opinie dojezdzajacych nie byly reprezentatywne dla danej gminy
# czy jezeli mieszkancy byli nierozroznialni to czy po iteracji mogla byc ulamkowa liczba konserwatystow?


class ModelClass:
    alfa = 0.5 # prawdopodobienstwo wybrania agenta z wlasnej gminy do interakcji w danym kroku
    D = 1 # prawdopodobienstwo losowej zmiany zdania
    breakpoints = [10 ** 1, 10 ** 1.2, 10 ** 1.4, 10 ** 1.6, 10 ** 1.8, 10 ** 2, 10 ** 2.2, 10 ** 2.4, 10 ** 2.6, 10 ** 2.8]
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
                 dist_matrix_filename : str = "macierz_odleglosci_cut_teryt.csv",
                 travellers_df_filename = "tabela_przeplywy2016_python.csv",uniform_dist = False):
        # inicjalizacja z pliku zawierajacego stan poczatkowy

        perc_of_pop_working = 1

        initial_state = pd.read_csv(initial_state_filename, dtype={'TERYT': str})
        self.D = D
        self.alfa = alfa
        self.pockets = {}
        self.gminas_pops = {}
        self.gminas_workforce = {}
        self.gminas_incomers = {}
        self.gminas_neighbours = {}
        if not uniform_dist:
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
                    self.pockets[row['FROM']][row['FROM']].recalculate_conservatists()
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
        if uniform_dist:
            for idx, row in initial_state.iterrows():
                self.pockets[row['TERYT']] = {}
                self.pockets[row['TERYT']][row['TERYT']] = Pocket(homeplace=row['TERYT'],
                                                                  workplace=row['TERYT'],
                                                                  population=row['POPULACJA'] * perc_of_pop_working,
                                                                  conservatism=0.5)
                self.gminas_pops[row['TERYT']] = row['POPULACJA'] * perc_of_pop_working
            commuters = pd.read_csv(travellers_df_filename, dtype={'FROM': str, 'TO': str})
            for idx, row in commuters.iterrows():
                if row['FROM'] in self.pockets.keys() and not row['FROM'] == row['TO']:
                    self.pockets[row['FROM']][row['TO']] = Pocket(homeplace=row['FROM'], workplace=row['TO'],
                                                                  population=row['n'],
                                                                  conservatism=self.pockets[row['FROM']][
                                                                      row['FROM']].conservatism)
                    self.pockets[row['FROM']][row['FROM']].depopulate(row['n'])
                    self.pockets[row['FROM']][row['FROM']].recalculate_conservatists()
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
        for homeplace in self.pockets.keys():
            lower_bound_km = 0
            if homeplace in self.d_matr.columns:
                self.gminas_neighbours[homeplace] = {}
                for i in self.breakpoints:
                    upper_bound_km = i

                    neighbours = list(self.d_matr.loc[((self.d_matr[homeplace]) < upper_bound_km) & (
                                (self.d_matr[homeplace]) > lower_bound_km)].index)
                    self.gminas_neighbours[homeplace][round(upper_bound_km)] = neighbours
                    lower_bound_km = i



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

        return workplace_interactions + homeplace_interactions + np.random.normal()*self.D

    def model_timestep(self):
        clone = self.pockets
        for homeplace in self.pockets.keys():
            for pocket in self.pockets[homeplace].keys():
                clone[homeplace][pocket].conservatism = min(max(self.pockets[homeplace][pocket].conservatism + self.calculate_pocket_timestep(self.pockets[homeplace][pocket]),0),1)
                clone[homeplace][pocket].recalculate_conservatists()
        self.pockets = clone

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

    def conservatism_in_gminas(self):
        tmp = {}
        for teryt,gmina in self.pockets.items():
            my_conservatists = 0
            for workplace in gmina.values():
                my_conservatists = workplace.conservatists + my_conservatists
            tmp[teryt] = my_conservatists
        return tmp
    @property
    def sigma_in_gminas(self):
        conservatism_support_vec = []
        for teryt, conservatists in self.conservatism_in_gminas().items():
            tmp = conservatists/self.gminas_pops[teryt]
            conservatism_support_vec.append(tmp)
        return np.std(conservatism_support_vec)

    @property
    def mean_conservatism_in_gminas(self):
        conservatism_support_vec = []
        for teryt, conservatists in self.conservatism_in_gminas().items():
            tmp = conservatists / self.gminas_pops[teryt]
            conservatism_support_vec.append(tmp)
        return mean(conservatism_support_vec)


    def calculate_spatial_correlation(self,lower_bound_km, upper_bound_km):
        mean_opinion_sq = self.mean_conservatism_in_gminas**2
        sigma_kwadrat = self.sigma_in_gminas**2
        correlation_vec = []
        covariance_vec = []
        conservatists = self.conservatism_in_gminas()
        for teryt, homeplace in self.pockets.items():
            if teryt in self.gminas_neighbours.keys():
                neighbours = self.gminas_neighbours[teryt][round(upper_bound_km)]
                my_opinion = conservatists[teryt]/self.gminas_pops[teryt]
                opinion_multiplied = []
            else:
                continue
            if len(neighbours) > 0:
                for gmina in neighbours:
                    if gmina in self.pockets.keys():
                        tmp = my_opinion * (conservatists[gmina]/self.gminas_pops[gmina])
                        opinion_multiplied.append(tmp)
                if len(opinion_multiplied) > 0:
                    mean_in_area = np.mean(opinion_multiplied)
                    mean_diff = mean_in_area - mean_opinion_sq
                    covariance_vec.append(mean_diff)
                    correlation = mean_diff / sigma_kwadrat
                    correlation_vec.append(correlation)
                else:
                    continue
        mean_spatial_correlation = mean(correlation_vec)
        mean_covariance = mean(covariance_vec)
        return (mean_spatial_correlation,mean_covariance)

    def investigate_correlation(self, points_to_be_calculated: list=breakpoints):
        korelacje = []
        kowariancje = []
        odleglosci = []
        poczatek = 0
        for i in points_to_be_calculated:
            koniec = i
            # print(str(poczatek) + " do " + str(koniec))
            tmp = self.calculate_spatial_correlation(poczatek, koniec)
            # print(tmp)
            poczatek = i
            odleglosci.append(koniec)
            korelacje.append(tmp[0])
            kowariancje.append(tmp[1])
        return korelacje,kowariancje

    def check_if_interrupted(self):
        print("Jezeli chcesz zakonczyc zbieranie danych przytrzymaj <p>")
        if keyboard.is_pressed("p"):
            print("You pressed p")
            return True
        time.sleep(1)
        if keyboard.is_pressed("p"):
            print("You pressed p")
            return True
        time.sleep(1)
        if keyboard.is_pressed("p"):
            print("You pressed p")
            return True
        time.sleep(1)
        if keyboard.is_pressed("p"):
            print("You pressed p")
            return True
        print("za pozno")
        return False

















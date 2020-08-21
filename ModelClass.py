import random
from random import sample
from statistics import stdev
from GminaClass import GminaClass
import pandas as pd
import numpy as np
from statistics import mean
from AgentClass import Agent

# zrobic dotychczasowe symulacje
# zrobic sprawdzenie wariancji od skali zmniejszenia


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

    def __init__(self,initial_state_filename: str = "gminas_pops_python2005.csv", D = 0.1, alfa =0.5,downscale_factor = 38):
        # inicjalizacja z pliku zawierajacego stan poczatkowy

        initial_state = pd.read_csv(initial_state_filename, dtype={'TERYT': str})
        self.D = D
        self.alfa = alfa
        self.downscale_factor = downscale_factor
        self.agents = []
        self.gminas = {}
        for idx, row in initial_state.iterrows():
            self.gminas[row['TERYT']] = GminaClass(teryt_code=row['TERYT'],
                                                                 population=row['POPULACJA'],
                                                                 conservatism_support=row['APPROX_PERCENTAGE'],
                                                                 downscale_factor=self.downscale_factor)

    def recalculate_conservatism(self):
        for i in self.gminas.values():
            i.conservatists = 0
            for j in i.residents_indices:
                if self.agents[j].opinion:
                    i.conservatists += 1

    # krok modelu ansynchronicznie
    # tzn. Opinie agentow nadpisywane sa w trakcie (nie pracujemy na kopii obiektu)
    def model_timestep(self, noise_type = "symmetric"):
        how_many_agents = len(self.agents)
        random_iterators = list(range(how_many_agents))
        for i in random_iterators:
            if random.random() < self.D:
                if noise_type == "symmetric": #szum klasyczny
                    if random.random() < 0.5:
                        self.agents[i].opinion = False
                    else:
                        self.agents[i].opinion = True
                else: # szum w ktorym mamy losowanie agenta z calej populacji kraju - w ten sposob szum nie zmienia nam sredniej opinii
                    who_is_chosen = sample(self.agents,1)[0]
                    self.agents[i].opinion = who_is_chosen.opinion
            elif random.random() < self.alfa:  # interacja z mieszkancami
                who_is_contacted = sample(self.gminas[self.agents[i].homeplace].residents_indices, 1)[0]
                self.agents[i].opinion = self.agents[who_is_contacted].opinion
            else: # interakcja z pracowinikami
                who_is_contacted = sample(self.gminas[self.agents[i].workplace].workers_indices, 1)[0]
                self.agents[i].opinion = self.agents[who_is_contacted].opinion
        self.recalculate_conservatism()

    def rokzlad_roznic(self,filename = "tabela_przeplywy2016_python.csv"):
        # od nowa wczytuje sobie pliczek z commuterami
        commuters = pd.read_csv(filename, dtype={'FROM': str, 'TO': str})
        opinion_diffs = []
        # iteracja po wszystkich polaczeniach
        for idx, row in commuters.iterrows():
            if row['FROM'] in self.gminas.keys() and row['TO'] in self.gminas.keys():
                from_opinion = self.gminas[row['FROM']].conservatism_pecentage
                to_opinion = self.gminas[row['TO']].conservatism_pecentage
                opinion_diffs.append(from_opinion-to_opinion)

        return opinion_diffs
    def opinion_of_gmina_size(self):
        # zwraca zaleznosc opinii od populacji gminy
        # funkcja zwraca obiekt typu plot zawierajacy w sobie dwie listy x i y jako wspolrzedne punktow na wykresie
        opinions = []
        populations = []
        for gmina in self.gminas.values():
            opinions.append(gmina.conservatism_pecentage)
            populations.append(gmina.n_agents)
        plot = self.Plot(x = populations,y = opinions)

        return plot

    def opinion_of_percent_of_outgoers(self):
        # zwraca zaleznosc procenta konserwatyzmu w danej gminie od procenta ludnosci wyjezdzajacej do pracy poza gmine
        # funkcja zwraca obiekt typu plot zawierajacy w sobie dwie listy x i y jako wspolrzedne punktow na wykresie
        opinions = []
        outgoers_percent = []
        for gmina in self.gminas.values():
            opinions.append(gmina.conservatism_pecentage)
            outgoers_percent.append(gmina.percent_of_outgoers)
        plot = self.Plot(x=outgoers_percent, y=opinions)
        return plot

    def percent_of_outgoers_of_size(self):
        outgoers_percentages = []  # y
        populations = []  # x
        for i in self.gminas.values():
            outgoers_percentages.append(i.percent_of_outgoers)
            populations.append(i.n_agents)

        plot = self.Plot(x = populations, y = outgoers_percentages)
        return plot

    def percent_of_incomers_of_size(self):
        incomers_percentages = []
        population = []

        for i in self.gminas.values():
            no_of_incomers = 0
            for j in i.workers_indices:
                if not self.agents[j].homeplace == i.id:
                    no_of_incomers = no_of_incomers + 1

            incomers_percent = no_of_incomers/i.n_agents
            incomers_percentages.append(incomers_percent)
            population.append(i.n_agents)

        plot = self.Plot(population,incomers_percentages)
        return plot














#TODO: kalibracja do rzeczywistej sigmy (rzeczywiste wartosci (chronologicznie) odchylenia:(11.2%,12.8%,12.7%,12.5%,13.6%)
#TODO: opinia w danej gminie od czasu krok po kroku
#TODO: ZROBIC SZUM ZAMIAST INTERAKCJI -- SZUM KTORY JEST WYLOSOWANIEM TYPKA
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
    def no_of_conservatists(self):
        conservatists = 0
        for i in self.agents:
            if i.opinion:
                conservatists += 1
        return conservatists
    @property
    def overall_conservatism_support(self):
        mn = self.no_of_conservatists/len(self.agents)
        # print("Konserwatyzm w Polsce popiera " + str(round(mn*100,2)) + "% osob")
        return mn
    @property
    def std_dev(self):
        sd = stdev(self.conservatism_in_gminas)
        # print("Odchylenie standardowe rozkladu poparc gmin:" + str(sd))
        return sd


    def __str__(self):
        return "Number of conservatists: " + str(self.no_of_conservatists)













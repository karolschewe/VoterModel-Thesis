# GLOWNA KLASA W MODELU - EMULUJE POPULACJE GMINY WRAZ Z Z AGENTAMI ICH STANAMI I POLACZENIAMI
from random import sample
import numpy as np


class GminaClass:
    _teryt_ = ""
    voters_states = [] # wektor opinii glosujacych True = konserwatyzm, False = antykonserwatyzm]
    working_gmina = [] # wektor miejsca pracy glosujacych; przyjmuje on wartosc terytu gminy przyjazdu lub "S" dla tej samej gminy

    # funkcja definiujaca wektor glosujacych

    def define_voters_vec(self,size: int, cons_supp: float):
        n_conservatives = round(size*cons_supp)
        n_others = round(size - n_conservatives)
        return np.asarray([True] * n_conservatives + [False] * n_others)

    # def __init__(self, teryt_code: str, population: int, conservatism_support: float, downscale_factor: int = None):
    #     self._teryt_ = teryt_code
    #     self.factor = downscale_factor
    #     self.n_agents = round(population/downscale_factor)
    #     self.voters_states = self.define_voters_vec(size=self.n_agents, cons_supp=conservatism_support)


    def __init__(self, teryt_code: str,  n_conservatists: int, n_others: int, downscale_factor: int):
        self._teryt_ = teryt_code
        self.n_agents = n_conservatists+n_others
        self.voters_states = np.asarray([True] * n_conservatists + [False] * n_others)
        self.factor = downscale_factor

    #konstruktor na podstawie pliku dumpowanego przez klase model
    @classmethod
    def from_textfile(cls, teryt_code: str, population: int, conservatism_support: float, downscale_factor: int):
        n_agents = round(population/downscale_factor)
        n_conservatives = round(n_agents * conservatism_support)
        n_others = round(n_agents - n_conservatives)
        return cls(teryt_code,n_conservatives,n_others,downscale_factor)


    def initialize_workplaces(self,df):
        # wybranie wierszy dotyczacych naszej gminy
        our_gmina = df['FROM'] == self._teryt_
        where_to = df[our_gmina]
        # wyznaczenie po ile bedzie dojezdzalo po zeskalowaniu w sumie
        sum_commuters = 0
        # wyznaczenie po ile bedzie dojezdzalo do kazdej gminy
        how_many_commuters = {}
        for idx, row in where_to.iterrows():
            nn = round(row['n']/self.factor)
            sum_commuters = sum_commuters + nn
            how_many_commuters[row['TO']] = nn # indeks w slowniku jest oznaczeniem gminy przyjazdu, wartosc oznacza liczbe agentow
        # wylosowanie ktorzy beda dojezdzali
        indexes = sample(range(self.n_agents),sum_commuters)
        # inicjalizacja wartoscia poczatkowa
        self.working_gmina = np.asarray(['S'] * self.n_agents, dtype='|U6')

        # zamiana pojedynczych wartosci
        i = 0
        for idx, value in how_many_commuters.items():
            for j in range(value):
                self.working_gmina[indexes[i]] = idx
                i = i+1

    def get_n_conservatves(self):
        unique, counts = np.unique(self.voters_states, return_counts=True)
        dd = dict(zip(unique, counts))
        if True in dd.keys():
            konserwa = dd[True]
        else:
            konserwa = 0
        return konserwa

    def __str__(self):
        konserwa = self.get_n_conservatves()
        return "Gmina: " + self._teryt_ +"\n" + "Number of agents: " + str(self.n_agents) + "\n" +\
               "Number of conservatives: " + str(konserwa) + "\n" + "Agents states: \n" \
               # + str(self.voters_states) + "\n Agents connections: \n" + str(self.working_gmina)

































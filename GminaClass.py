# GLOWNA KLASA W MODELU - EMULUJE POPULACJE GMINY WRAZ Z Z AGENTAMI ICH STANAMI I POLACZENIAMI
from random import sample


class GminaClass:
    _teryt_ = ""
    voters_states = [] # wektor opinii glosujacych True = konserwatyzm, False = antykonserwatyzm]
    working_gmina = [] # wektor miejsca pracy glosujacych; przyjmuje on wartosc terytu gminy przyjazdu lub "S" dla tej samej gminy

    # funkcja definiujaca wektor glosujacych

    def define_voters_vec(self,size: int, cons_supp: float):
        n_conservatives = round(size*cons_supp)
        n_others = round(size - n_conservatives)
        return [True] * n_conservatives + [False] * n_others

    def __init__(self, teryt_code: str, population: int, conservatism_support: float, downscale_factor: int):
        self._teryt_ = teryt_code
        self.factor = downscale_factor
        self.n_agents = round(population/downscale_factor)
        self.voters_states = self.define_voters_vec(size=self.n_agents, cons_supp=conservatism_support)

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
        self.working_gmina = ['S'] * self.n_agents

        # zamiana pojedynczych wartosci
        i = 0
        for idx, value in how_many_commuters.items():
            for j in range(value):
                self.working_gmina[indexes[i]] = idx
                i = i+1




















# GLOWNA KLASA W MODELU - EMULUJE POPULACJE GMINY WRAZ Z Z AGENTAMI ICH STANAMI I POLACZENIAMI


class GminaClass:
    _teryt_ = ""
    voters_states = [] # wektor opinii glosujacych True = konserwatyzm, False = antykonserwatyzm]

    # funkcja definiujaca wektor glosujacych

    def define_voters_vec(self,size: int, cons_supp: float):
        n_conservatives = round(size*cons_supp)
        n_others = round(size - n_conservatives)
        return [True] * n_conservatives + [False] * n_others

    def __init__(self, teryt_code: str, population: int, conservatism_support: float, downscale_factor: int):
        self._teryt_ = teryt_code
        pop_size = round(population/downscale_factor)
        self.voters_states = self.define_voters_vec(size=pop_size, cons_supp=conservatism_support)












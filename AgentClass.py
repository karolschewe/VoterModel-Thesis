
class Agent:
    def __init__(self,opinion,homeplace,workplace):
        self.opinion = opinion
        self.homeplace = homeplace
        self.workplace = workplace
    def __str__(self):
        return "Mieszkam w gminie: " + self.homeplace + ", pracuje w gminie:" + \
               self.workplace + "\n Konserwatyzm: " + str(self.opinion)
class Pocket:

    def __init__(self,homeplace: str, workplace: str, population: int, conservatism: float):
        self.homeplace = homeplace
        self.workplace = workplace
        self.population = population
        self.conservatism = conservatism
        self.conservatists = population * conservatism

    def __str__(self):
        return "Mieszkamy w " + self.homeplace + ", pracujemy w " + self.workplace \
               + "\n Jest nas" + str(self.population) + "\nPoparcie konserwatyzmu: " + str(self.conservatism)

    def depopulate(self,n):
        if self.population-n > 0:
            self.population = self.population-n
        else:
            self.population = 1

    def recalculate_conservatists(self):
        self.conservatists = self.population*self.conservatism
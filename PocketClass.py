class Pocket:

    def __init__(self,homeplace: str, workplace: str, population: int, conservatism: float):
        self.homeplace = homeplace
        self.workplace = workplace
        self.population = population
        self.conservatism = conservatism

    def __str__(self):
        return "Mieszkamy w " + self.homeplace + ", pracujemy w " + self.workplace \
               + "\n Jest nas" + str(self.population) + "\nPoparcie konserwatyzmu: " + str(self.conservatism)

    def depopulate(self,n):
        self.population = self.population-n
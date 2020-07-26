


class Agent:

    def __init__(self,opinion, workplace):
        self.opinion = opinion
        self.__workplace = workplace

    @property
    def work(self):
        return self.__workplace



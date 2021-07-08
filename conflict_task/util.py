from numpy.random import randint

class Alternator:
    index = 0
    max = 0

    def __init__(self, max, start = 0):
        self.max = max
        self.index = start
    
    def next(self):
        self.index += 1
        
        if self.index >= self.max:
            self.index = 0

class Randomizer:
    number = 0
    max = 0

    def __init__(self, max):
        self.max = max
    
    def new_one(self):
        self.number = randint(self.max)
        return self.number
from numpy.random import randint

class Alternator:
    index = 0
    max = 0

    def __init__(self, max, start = 0):
        self.max = max

        if(start >= self.max):
            raise ValueError("'start' is out of bounds")
        self.index = start
    
    def next(self):
        self.index += 1
        
        if self.index >= self.max:
            self.index = 0

        return self.index
    
    def prev(self):
        self.index -= 1

        if self.index < 0:
            self.index = self.max_value()
        
        return self.index
    
    def max_value(self):
        return self.max - 1
    
    def what_is_next(self):
        if self.index < self.max_value():
            return self.index + 1
        else:
            return 0
    
    def what_was_prev(self):
        if self.index > 0:
            return self.index - 1
        else:
            return self.max_value()

class Randomizer:
    number = 0
    max = 0

    def __init__(self, max):
        self.max = max
    
    def new_one(self):
        self.number = randint(self.max)
        return self.number
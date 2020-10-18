class Car():
    def __init__(self):
        self.wheels = 4
        self.doors = 4
        self.windows = 4
        self.seats = 4

    def __str__(self):
        return f"Car with {self.wheels} wheels"

class Convertable(Car):
    

mini = Car()
print(mini)
class 
class Animal:

    def __init__(self, name, age):
        self.name = name
        self._age = age

    def make_sound(self):
        return 'Some generic animal sound'


class Dog(Animal):

    def __init__(self, name, age, breed):
        super().__init__(name, age)
        self.breed = breed

    def make_sound(self):
        return 'Bark!'

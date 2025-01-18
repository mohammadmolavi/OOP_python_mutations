class Animal:

    def __init__(self, name='Animal', age=0):
        self.name = name
        self.age = age

    def make_sound(self):
        return 'Some generic animal sound'

    def get_info(self):
        return f'{self.name} is {self.age} years old.'


class Dog(Animal):

    def __init__(self, name, age, breed):
        super().__init__(name, age)
        self.breed = breed

    def make_sound(self):
        return 'Bark!'

    def get_info(self):
        return f'{self.name} is a {self.breed} and {self.age} years old.'

    def get_info(self):
        return 'Hidden method in Dog'

class Animal:

    def __init__(self, name, age):
        self.name = name
        self._age = age

    def make_sound(self):
        return 'Some generic animal sound'

    def get_info(self):
        return f'{self.name} is {self._age} years old.'


class Dog(Animal):
    self.name = 'Hidden field in Dog'

    def __init__(self, name, age, breed):
        super().__init__(name, age)
        self.breed = breed

    def make_sound(self):
        return 'Bark!'

    def get_info(self):
        return f'{self.name} is a {self.breed} and {self._age} years old.'

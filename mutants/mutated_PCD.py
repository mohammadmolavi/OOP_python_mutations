class Animal:

    def make_sound(self):
        return 'Some generic animal sound'

    def get_info(self):
        return f'{self.name} is {self._age} years old.'


class Dog(Animal):

    def make_sound(self):
        return 'Bark!'

    def get_info(self):
        return f'{self.name} is a {self.breed} and {self._age} years old.'

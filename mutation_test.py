import unittest

from mutant import *

class TestAnimalBehavior(unittest.TestCase):
    def setUp(self):
        """Set up test cases with an Animal and a Dog instance."""
        self.animal = Animal("GenericAnimal", 5)
        self.dog = Dog("Buddy", 3, "Golden Retriever")

    # Test for Encapsulation (AMC)
    def test_private_attribute(self):
        try:
            _ =  self.animal._age # Should fail if encapsulation is mutated
        except:
            raise AttributeError(Exception("mutated by AMC"))

    # Test for Inheritance Mutants
    def test_inheritance_hiding_method(self):
        self.assertEqual(self.dog.make_sound(), "Bark!")  # Ensure Dog's method is used

    def test_inheritance_hiding_field(self):
        self.assertEqual(self.dog.name, "Buddy")  # Ensure name isn't overridden incorrectly

    def test_inheritance_overridden_method(self):
        self.assertEqual(self.dog.get_info(), "Buddy is a Golden Retriever and 3 years old.")

    def test_insert_super_invocation(self):
        self.assertEqual(self.dog.make_sound(), "Bark!")  # Ensure parent method isn't called unnecessarily

    def test_change_parent_class(self):
        self.assertIsInstance(self.dog, Animal)  # Ensure Dog still inherits from Animal

    # Test for Polymorphism Mutants
    def test_method_deletion(self):
        try:
            _ = self.dog.make_sound()  # Should fail if make_sound is deleted
        except:
            raise AttributeError

    def test_parameter_deletion(self):
        self.assertEqual(self.dog.get_info(), "Buddy is a Golden Retriever and 3 years old.")  # Ensure no parameters are removed

    def test_constructor_inlining(self):
        new_dog = Dog("Max", 4, "Bulldog")
        self.assertEqual(new_dog.get_info(), "Max is a Bulldog and 4 years old.")  # Ensure constructor works correctly

    def test_constructor_deletion(self):
        try:
            _ = Dog()  # Should fail if constructor is deleted
        except:
            raise TypeError(Exception("mutated by PCD"))

    def test_overriding_method_deletion(self):
        self.assertEqual(self.dog.make_sound(), "Bark!")  # Ensure overridden method exists

    def test_argument_change(self):
        self.assertEqual(self.dog.get_info(), "Buddy is a Golden Retriever and 3 years old.")  # Ensure arguments are not mutated


if __name__ == "__main__":
    package = "os"
    class1 = "Animal"
    class2 = "Dog"
    unittest.main()
    print("yess")
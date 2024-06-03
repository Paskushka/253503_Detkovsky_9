import csv
import pickle


class Person:
    """Class person with counting population"""
    population = 0  # Static attribute

    def __init__(self, surname):
        self.surname = surname
        Person.population += 1

    def __del__(self):
        Person.population -= 1

    @classmethod
    def get_population(cls):
        """Method for getting population"""
        return cls.population

    def __str__(self):
        return f"Person: {self.surname}"


class HeightMixin:
    """Mixin for work experience"""

    def __init__(self, height):
        self.height = height


class Human(Person, HeightMixin):
    """Human class"""

    def __init__(self, surname, height, gender):
        super().__init__(surname)  # Using super()
        HeightMixin.__init__(self, height)
        self.gender = gender

    @property  # Getter for surname
    def surname(self):
        return self._surname

    @surname.setter  # Setter for surname
    def surname(self, value):
        self._surname = value

    def __str__(self):  # Special method
        return f"Person: {self.surname}, {self.gender}, {self.height} cm"

    @property  # Property
    def name_and_gender(self):
        """Method for getting name and gender"""
        return f"{self.surname}  -  {self.gender}"


class HumanDataHandler:
    """Class that contains info about human"""

    def __init__(self):
        self.humans = []

    def deserialize_from_dict(self, humans_dict):
        """Method for deserializing dictionary"""
        self.humans = []
        for human_data in humans_dict.values():
            student = Human(**human_data)
            self.humans.append(student)

    def add_human(self, human):
        """Method for adding human"""
        self.humans.append(human)

    def serialize_csv(self, filename):
        """Method for serializing to csv"""
        try:
            with open(filename, 'w', newline='') as csvfile:
                fieldnames = ['Surname', 'Height', 'Gender']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for human in self.humans:
                    writer.writerow({'Surname': human.surname, 'Height': human.height, 'Gender': human.gender})
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def deserialize_csv(self, filename):
        """Method for deserializing from csv"""
        try:
            self.humans = []
            with open(filename, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    human = Human(row['Surname'], int(row['Height']),row['Gender'])
                    self.humans.append(human)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def serialize_pickle(self, filename):
        """Method for serializing to pickle"""
        try:
            with open(filename, 'wb') as file:
                pickle.dump(self.humans, file)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def deserialize_pickle(self, filename):
        """Method for deserializing from pickle"""
        try:
            with open(filename, 'rb') as file:
                self.humans = pickle.load(file)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def average_female_height(self):
        """Method to calculate the average height of females"""
        female_heights = [human.height for human in self.humans if human.gender == 'female']
        if female_heights:
            return sum(female_heights) / len(female_heights)
        else:
            return None

    def get_tallest_male_surname(self):
        """Method to get the surname of the tallest male"""
        tallest_male = max((human for human in self.humans if human.gender == 'male'), key=lambda x: x.height, default=None)
        if tallest_male:
            return tallest_male.surname
        else:
            return None

    def has_duplicate_heights(self):
        """Method to check if there are at least two people with the same height"""
        heights = [human.height for human in self.humans]
        if len(heights) > len(set(heights)):
            return True
        else:
            return False

    def get_human_info_from_user(self):
        """Method to get information about a person from the user"""
        surname = input("Enter surname: ")
        height = int(input("Enter height: "))
        gender = input("Enter gender: ")
        human = Human(surname, height, gender)
        return human

    def find_human_by_surname(self, surname):
        """Method for finding human by surname"""
        for human in self.humans:
            if human.surname == surname:
                return human
        return None

    def search_human(self):
        """Method for finding human with input"""
        surname = input("Enter human's surname to search: ")
        found_human = self.find_human_by_surname(surname)
        if found_human:
            print("Human found:")
            print(found_human)
        else:
            print("Human not found.")

    def sort_students_by_surname(self):
        """Method for sorting humans by surname"""
        sorted_humans = sorted(self.humans, key=lambda human: human.surname)
        return sorted_humans


def main():
    """Main function for task1"""
    while True:
        handler = HumanDataHandler()

        humans_dict = {
            'Bob': {'surname': 'Xot', 'height': 192, 'gender': 'male'},
            'Bib': {'surname': 'Ait', 'height': 162, 'gender': 'female'},
            'Bab': {'surname': 'Rat', 'height': 192, 'gender': 'female'}
        }

        handler.deserialize_from_dict(humans_dict)

        handler.serialize_csv("C:/Users/Lenovo/PycharmProjects/Lab4IGI/csv_humans.txt")

        handler.deserialize_csv("C:/Users/Lenovo/PycharmProjects/Lab4IGI/csv_humans.txt")

        handler.serialize_pickle("C:/Users/Lenovo/PycharmProjects/Lab4IGI/humans.txt")

        handler.deserialize_pickle("C:/Users/Lenovo/PycharmProjects/Lab4IGI/humans.txt")

        print(f"Average female height: {handler.average_female_height()}")
        print(f"Tallest male surname: {handler.get_tallest_male_surname()}")
        print(f"Has or not duplicate heights: {handler.has_duplicate_heights()}")
        print(f"Find human: {handler.find_human_by_surname('Xot')}")
        # print(handler.sort_students_by_surname())
        repeat = input("Do you want to execute program one more time? Type 'yes' if so: ")
        if repeat != 'yes':
            break


if __name__ == "__main__":
    main()
# Function
def greeting():
    print("Greetings pythonista!")


# Static Method
class Person:
    @staticmethod
    def greeting():
        print("Greetings pythonista!")

# Use Self
class Person:
    name: str = "Amelia"

    def greeting(self):
        print(f"Greetings {self.name} the pythonista!")

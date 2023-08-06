class Base(object):
    def breathe(self):
        return "breathe"


class Animal(Base):
    def run(self):
        return "run"

    def walk(self):
        return "walk"

    def sleep(self):
        return "sleep"


class FoxManager(object):
    def find_other_fox(self):
        return "find_other_fox"

    def drink(self):
        return "drink water"

    def eat(self):
        return "eat meat"


class Fox(Base):
    def __init__(self):
        self.name = "aurora fox"
        self.sex = "male"
        self.actions = FoxManager()


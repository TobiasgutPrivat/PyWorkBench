class Person():
    name: str
    age: int
    children: list

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def getOlder(self):
        self.age += 1

    def becomeChild(self, name):
        newChild = Person(name, 0)
        self.children.append(newChild)
from typing import TypedDict


class Person(TypedDict):
    name: str
    age: int


new_person: Person = {'name': 78, 'age': "67"}
print(new_person)
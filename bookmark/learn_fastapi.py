def get_full_name(first_name: str, last_name: str):
    full_name = first_name.title() + " " + last_name.title();
    return full_name

print(get_full_name("john", "doe"))

# simple types
# int
# float
# bool
# bytes

# from typing import Any

# generics
# list - sqr bracket
# tuple
# set
# dict - 2 cols

# union
# def process_item(item: int | str):
#     print(item)

# none

# def say_hi(name: str | None = None):
#     if name is not None:
#         print(f"Hey {name}!")
#     else:
#         print("Hello World")

# can declare the type as a class
# class Person:
#     def __init__(self, name: str):
#         self.name = name

# def get_person_name(one_person: Person):
#     return one_person.name
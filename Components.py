"""
Components classes without functions. They are simply data structures.
All the logic is contained within Systems, which modify the data within
Entities which are simply collections of Component instantiations
"""

class Component(type):
    """A generic component class"""
    count = 0

    def __new__(cls, name, bases, dct):
        component_class = super().__new__(cls, name, bases, dct)
        component_class.component_id = cls.count
        cls.count += 1
        return component_class

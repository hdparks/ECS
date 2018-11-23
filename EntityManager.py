import numpy as np

class Entity(dict):
    """An Entity has a unique id and a dictionary of Components"""
    def __init__(self,id):
        self.id = id;
        dict.__init__(self)

class EntityManager:
    """An EntityManager has two directives:
    1.) Maintain dictionary mapping unique ids to an Entity (set of Components)
    2.) Maintain lists of all Entities with the same set of Components (families)
    for easy retrieval by systems working on a family of similar entities.
    """
    # Fields
    entities = {}
    entity_families = {}
    total = 0

    def __init__(self, components):
        """Initialize component_id_table, which maps each component type
        to a unique int id.

        Parameters:
            components(list(Components)):
            A list of all components which entities can take on.
        """
        self.component_id_table = \
        { component:i for (i,component) in enumerate(components) }


    def add_entity(self, *args, n=1):
        """Construct new entity, incrementing self.total"""

        for _ in range(n):
            e = Entity(self.total)
            self.entities[e.id] = e
            self.total += 1
            self.add_component(e,*args)

    def add_component(self, entity, *components):
        """ Adds a component to an entity through the following steps:

        Remove entity id from current entity family,
        Add component(s) to entity,
        Add entity id to new entity family
        """
        self.remove_from_family(entity)

        for c in components:
            entity[type(c)] = c

        self.add_to_family(entity)


    def remove_component(self, entity, *componentTypes):
        """ Remove entity id from entity family of current components,
            Remove components from entity,
            Add entity id to entity family of new list of components
        """
        self.remove_from_family(entity)

        for c in componentTypes:
            entity.pop(c)

        self.add_to_family(entity)


    def add_to_family(self, entity):
        """ Adds the entity to its corresponding entity family.
            If no such family exists, a suitable family is created.
        """
        family = self.get_entity_family(entity, exact_match=True)
        family.append(entity)

        # If this is a new family, add it to the entity families map
        if len(family) == 1:
            self.entity_families[self.get_component_id(entity.keys())] = family


    def remove_from_family(self, entity):
        """Removes the entity from its entity family"""
        try:
            self.get_entity_family(entity,exact_match=True).remove(entity)
        except ValueError:
            # If the entity wasn't in the list, nothing happens
            # This may occur when the entity is first created and has no family
            pass



    def get_entity_family(self, component_list, exact_match = False):
        """Returns: a list of all entities with the supplied components.

        If exact_match = True, returns only those entities which exactly match
        the given component template.

        Parameters:
            component_list( list(int) | entity ): defines a list of components

            exact_match(boolean): If true, returns a list of Entities whose
                component list exactly matches the given component_list

        """

        # If an entity was passed in,
        if type(component_list) == Entity:
            component_list = self.get_component_id(list(component_list.keys()))

        if exact_match:

            try:
                return self.entity_families[component_list]
            except KeyError:
                # If an exact match wasn't found, return an empty list
                return []

        else:

            keys = list(self.entity_families.keys())
            relevant_keys = []
            for key in keys:
                if all([id in key for id in component_list]):
                    relevant_keys.append(key)

            return np.array([self.entity_families[key] for key in relevant_keys]).flatten().tolist()


    def get_component_id(self, componentList):
        """
        Parameters:
            component(list(Component))

        Returns (list(int)) representing the ids of the supplied components,
            sorted such that tupled list may be used as a key to an entity family

        """
        ids = [self.component_id_table[c] for c in componentList]
        ids.sort()
        return tuple(ids)

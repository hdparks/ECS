class Entity(dict):
    """An Entity has a unique id and a dictionary of Components"""
    def __init__(self,id, *args):
        self.id = id;
        dict.__init__(self)
        for a in args:
            self[type(a)] = a

    def add_component(self, *component_instances):
        for c in component_instances:
            self[type(c)] = c

    def remove_component(self, *component_types):
        for c in component_types:
            self.pop(c)

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

    def create_entity(self, *component_instances):
        """Creates a new Entity instance with the given component instances"""
        total = self.total
        self.total += 1
        return Entity(total, *component_instances)


    def add_entity(self, *component_instances):
        """Construct new entity, incrementing self.total"""

        e = self.create_entity(*component_instances)
            self.entities[e.id] = e
            self.add_to_family(e)

    def add_component(self, entity, *component_instances):
        """ Adds a component to an entity through the following steps:

        Remove entity id from current entity family,
        Add component(s) to entity,
        Add entity id to new entity family
        """
        self.remove_from_family(entity)

        entity.add_component(*component_instances)

        self.add_to_family(entity)


    def remove_component(self, entity, *component_types):
        """ Remove entity id from entity family of current components,
            Remove components from entity,
            Add entity id to entity family of new list of components
        """
        self.remove_from_family(entity)

        entity.remove_component(*component_types)

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



    def get_entity_family(self, family_key, exact_match = False):
        """Returns: a list of all entities with the supplied components.

        If exact_match = True, returns only those entities which exactly match
        the given component template.

        Parameters:
            family_key(tuple(int)): defines a family of entities with same components

            exact_match(boolean): If true, returns a list of Entities whose
                component list exactly matches the given component_list

        """

        if exact_match:

            try:
                return self.entity_families[family_key]
            except KeyError:
                # If an exact match wasn't found, return an empty list
                return []

        else:

            keys = list(self.entity_families.keys())
            entities = []
            for key in keys:
                if all([id in key for id in family_key]):
                    entities += self.entity_families[key])

            return entities


    def get_family_key(self, *component_list):
        """
        Parameters: any number of Component classes
        Returns: sorted tuple of Components' ids, used as family key
        """
        return tuple([c.component_id for c in component_list].sort())

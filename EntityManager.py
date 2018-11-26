class Entity(dict):
    """An Entity has a unique id and a dictionary of Components"""
    def __init__(self,id,EntityManager, *args):
        self.id = id;
        self.em = EntityManager
        dict.__init__(self)
        for a in args:
            self[type(a)] = a
        self.em.add_to_family(self)

    def add_component(self, *component_instances):
        self.em.remove_from_family(self)
        for c in component_instances:
            self[type(c)] = c
        self.em.add_to_family(self)

    def remove_component(self, *component_types):
        self.em.remove_from_family(self)
        for c in component_types:
            self.pop(c)
        self.em.add_to_family(self)


class EntityManager:
    """An EntityManager has two directives:
    1.) Maintain dictionary mapping unique ids to an Entity (set of Components)
    2.) Maintain lists of all Entities with the same set of Components (families)
    for easy retrieval by systems working on a family of similar entities.
    """
    # Fields
    def __init__(self):
        self.entity_families = {}
        self.total = 0

    def create_entity(self, *component_instances):
        """Creates a new Entity instance with the given component instances"""
        total = self.total
        e = Entity(total, self, *component_instances)
        self.total += 1
        return e

    def add_to_family(self, entity):
        """ Adds the entity to its corresponding entity family.
            If no such family exists, a suitable family is created.
        """
        family_key = self.get_family_key(*entity.keys())
        family = self.get_entity_family(family_key, exact_match=True)
        family.append(entity)

        # If this is a new family, add it to the entity families map
        if len(family) == 1:
            self.entity_families[family_key] = family


    def remove_from_family(self, entity):
        """Removes the entity from its entity family"""
        family_key = self.get_family_key(*entity.keys())
        family = self.get_entity_family(family_key,exact_match=True)
        try:
            family.remove(entity)
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
                    entities += self.entity_families[key]

            return entities


    def get_family_key(self, *component_list):
        """
        Parameters: any number of Component classes
        Returns: sorted tuple of Components' ids, used as family key
        """
        cid_list = [c.component_id for c in component_list]
        cid_list.sort()
        return tuple(cid_list)

    def get_entities_by_components(self, *component_list):
        """
        Parameters: any number of Component classes
        Returns: All entities contiaining the given Components
        """
        family_key = self.get_family_key(*component_list)
        return self.get_entity_family(family_key)

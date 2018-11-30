class Entity(dict):
    """An Entity has a unique id and a dictionary of Components"""
    def __init__(self,id,EntityManager, *args):
        self.id = id;
        self.em = EntityManager
        dict.__init__(self)
        self.add_component(*args)

    def handle_family_issues(func):
        def family_issues_wrapper(self,*args,**kwargs):
            self.em.remove_from_family(self)
            output = func(self,*args,**kwargs)
            self.em.add_to_family(self)
            return output
        return family_issues_wrapper


    @handle_family_issues
    def add_component(self, *component_instances):
        for c in component_instances:
            if hasattr(c,'source_component'):
                self[c.source_component] = c
            else:
                self[type(c)] = c

    @handle_family_issues
    def remove_component(self, *component_types):
        for c in component_types:
            self.pop(c)


class EntityManager:
    """An EntityManager has two directives:
    1.) Maintain dictionary mapping unique ids to an Entity (set of Components)
    2.) Maintain lists of all Entities with the same set of Components (families)
    for easy retrieval by systems working on a family of similar entities.

    Fields:

    entity_families (dict): Maps tuples to lists of Entities, where the tuples
        are the sorted family keys defined by the ids of the source components
        and pure component types in the keys of each Entity

    total (int): The total number of Entities created in the lifetime of the
        manager

    sc_index (int): "Source index", determines the next source_id to be assigned
    """
    # Fields
    def __init__(self):
        self.entity_families = {}
        self.total = 0
        self.sc_index = -1

    def create_entity(self, *component_instances):
        """Creates a new Entity instance with the given component instances"""
        e = Entity(self.total, self, *component_instances)
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
        # Takes source_id of source components, component_id of pure components
        def identify(c):
            if hasattr(c,'source_id'):
                return c.source_id
            else:
                return c.component_id

        cid_list = [identify(c) for c in component_list]
        cid_list.sort()
        return tuple(cid_list)

    def get_entities_by_components(self, *component_list):
        """
        Parameters: any number of Component classes
        Returns: All entities contiaining the given Components
        """
        family_key = self.get_family_key(*component_list)
        return self.get_entity_family(family_key)

    def register_source_component(self, component_instance):
        """
        Source components can be used as Entity keys to access component
        data within an Entity that is related to an external component instance.

        For example, a student (Entity) could be taking many
        different courses at once: instead of having a separate component
        for every possible course, a student can map an instance of a Course
        to that student's relevant data, and can map another Course instance
        to different data. The two Courses are different sources of assignments,
        grades, ect., so they could each be registered as different
        source components.

        Source components are assigned negative values beginning at -1 in order
        to prevent collisions with the nonnegative component ids in family keys.
        """
        component_instance.source_id = self.sc_index
        self.sc_index -= 1

        return

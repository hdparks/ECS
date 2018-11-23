class System:
    """ A generic System template"""
    def __init__(self, EntityManager, template):

        # Ensures that the EntityManager has ids for the Components in template
        if not all([comp in EntityManager.component_id_table.keys() for comp in template]):
            raise ValueError("The given EntityManager does not support the Components in the given template")

        self.em = EntityManager
        self.ids = EntityManager.get_component_id(template)

    def get_entities(self, *components):
        """Query the EntityManager for all entities with necessary components"""
        if components:
            return self.em.get_entity_family(self.em.get_component_id(components))
        else:
            return self.em.get_entity_family(self.ids)

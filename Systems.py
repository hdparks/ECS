class System:
    """ A generic System template"""
    def __init__(self, EntityManager, template):

        # Ensures that the EntityManager has ids for the Components in template
        if not all([comp in EntityManager.componentIdTable.keys() for comp in template]):
            raise ValueError("The given EntityManager does not support the Components in the given template")

        self.em = EntityManager
        self.ids = EntityManager.getComponentId(template)

    def get_entities(self, *components):
        """Query the EntityManager for all entities with necessary components"""
        if components:
            return self.em.get_entity_family(em.getComponentId(components))
        else:
            return self.em.get_entity_family(self.ids)

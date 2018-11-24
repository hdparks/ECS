class System:
    """ A generic System template"""
    def __init__(self, EntityManager, template):
        self.em = EntityManager

    def get_entities_by_components(self, *components):
        """Query the EntityManager for all entities with necessary components"""
        return self.em.get_entities_by_components(components)

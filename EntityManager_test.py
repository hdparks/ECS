from EntityManager import EntityManager, Entity
import pytest

def test_Entity_construction():
    e = Entity(1)
    assert e.id == 1, "Failed on Entity.id"

    d = int(2)
    e = Entity(1,d)
    assert int in e.keys(), "Failed on dictionary creation"
    assert e[int] == d, "Failed on dictionary lookup"

def test_Entity_lookup():
        e = Entity(1)
        e[EntityManager] = 1
        assert e[EntityManager] == 1, "Failed on Entity dictionary lookup"

def test_Entity_Manager_construction():
    em = EntityManager()
    assert em.entities == {}
    assert em.entity_families == {}
    assert em.total == 0

def test_EntityManager_add_entity():
    em = EntityManager()
    em.add_entity()

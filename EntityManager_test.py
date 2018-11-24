from EntityManager import EntityManager, Entity
import pytest


def test_EntityManager_construction():
    em = EntityManager()
    assert em.total == 0
    assert em.entities == {}
    assert em.entity_families == {}

def test_Entity_construction():
    em = EntityManager()
    e = em.create_entity(int(1),str('one'))
    assert e.id == 0, "Failed on Entity.id"
    assert list(e.keys()) == [int, str], "Failed on key definitions"
    assert list(e.values()) == [1,'one'], "Failed on vaule definitions"
    assert e[int] == 1, "Failed on dictionary lookup"
    assert e.em == em, "Failed on EntityManager reference"
    assert len(em.entity_families) >= 1, "Failed on adding entity to family"

def test_EntityManager_add_to_family():
    em = EntityManager()
    e = em.create_entity()

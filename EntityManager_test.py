import EntityManager as EM
import Systems as S
import Components as c
import pytest


class A(metaclass=c.Component):
    pass

class B(metaclass=c.Component):
    pass

def test_Components_Metaclass():
    assert A.component_id == 0, "Failed to initialize component_id"
    assert B.component_id == 1, "Failed to increment component_id"
    assert c.Component.count == 2, "Failed to track component count"

def test_EntityManager_construction():
    em = EM.EntityManager()
    assert em.total == 0
    assert em.entity_families == {}

def test_Entity_construction():
    em = EM.EntityManager()
    a = A()
    b = B()
    e = em.create_entity(a,b)
    assert e.id == 0, "Failed on Entity.id"
    assert list(e.keys()) == [A, B], "Failed on key definitions"
    assert list(e.values()) == [a,b], "Failed on vaule definitions"
    assert e[A] == a, "Failed on dictionary lookup"
    assert e.em == em, "Failed on EntityManager reference"
    assert len(em.entity_families) == 1, "Failed on adding one and only one entity to family"


def test_EntityManager_remove_from_family():
    em = EM.EntityManager()
    a = A()
    b = B()
    e = em.create_entity(a,b)
    family_key = em.get_family_key(*e.keys())
    family = em.get_entity_family(family_key,exact_match=True)
    print('before', family)
    assert e in family, "Failed on entity not in family"
    em.remove_from_family(e)
    family = em.get_entity_family(family_key,exact_match=True)
    print('after', family)
    assert e not in family, "Failed on removing entity from family"
    assert len(family) == 0, "Failed on emptying family"

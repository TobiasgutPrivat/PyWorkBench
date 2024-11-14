import unittest
from dataclasses import dataclass
from BasicProxy import DynamicProxy

@dataclass
class SubObject:
    value: int

@dataclass
class ParentObject:
    value: int
    sub_obj: SubObject

    def __init__(self, value):
        self.value = value
        self.sub_obj = SubObject(value * 2)
    
class SimpleTestCase(unittest.TestCase):
    parent_proxy: DynamicProxy

    def setUp(self):
        """Call before every test case."""
        parent = ParentObject(10)
        self.parent_proxy = DynamicProxy(parent)

    def testInit(self):
        assert self.parent_proxy.value == 10
        assert self.parent_proxy.sub_obj.value == 20
        assert isinstance(self.parent_proxy, DynamicProxy)# issue if there are type checks in general
        assert isinstance(self.parent_proxy.sub_obj, DynamicProxy)

    def testGet(self):
        assert self.parent_proxy.value == 10
        assert self.parent_proxy.sub_obj.value == 20
        id = self.parent_proxy._id
        del self.parent_proxy
        print(isinstance(id, str))
        self.parent_proxy = DynamicProxy(id)
        assert self.parent_proxy.value == 10
        assert self.parent_proxy.sub_obj.value == 20

    # def testSubobject(self):
    #     self.parent_proxy.new_attr = SubObject(100)

unittest.main()
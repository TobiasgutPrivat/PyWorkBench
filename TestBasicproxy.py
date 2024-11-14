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
    def testBasicProxy(self):
        parent = ParentObject(10)
        parent_proxy = DynamicProxy(parent)
        #init
        assert parent_proxy.value == 10
        assert parent_proxy.sub_obj.value == 20
        assert isinstance(parent_proxy, DynamicProxy)# issue if there are type checks in general
        assert isinstance(parent_proxy.sub_obj, DynamicProxy)

        #references
        # parent_proxy.parent = parent

        #edit
        parent_proxy.sub_obj.value = 30
        assert parent_proxy.sub_obj.value == 30

        #reload
        id = parent_proxy._id
        del parent_proxy
        parent_proxy = DynamicProxy(id)
        assert parent_proxy.value == 10
        assert parent_proxy.sub_obj.value == 30

        #delete
        assert hasattr(parent_proxy, 'value') == True
        delattr(parent_proxy, 'value')
        assert hasattr(parent_proxy, 'value') == False

        #new object
        newObj = SubObject(40)
        parent_proxy.newObj = newObj
        assert parent_proxy.newObj.value == 40
        assert isinstance(parent_proxy.newObj, DynamicProxy)

        print(str(parent_proxy)) #TODO some Error
        #list


        #dict


unittest.main()
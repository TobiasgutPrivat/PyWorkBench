import unittest
from dataclasses import dataclass
from WorkBenchProxy import DynamicProxy

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
        parent.reference = parent
        parent_proxy = DynamicProxy(parent)
        #init
        assert parent_proxy.value == 10
        assert parent_proxy.sub_obj.value == 20
        assert isinstance(parent_proxy, DynamicProxy)# issue if there are type checks in general
        assert isinstance(parent_proxy.sub_obj, DynamicProxy)

        #edit
        parent_proxy.sub_obj.value = 30
        assert parent_proxy.sub_obj.value == 30

        #reload
        id = parent_proxy._id
        parent_proxy._save()
        del parent_proxy
        parent_proxy = DynamicProxy(id)
        assert parent_proxy.value == 10
        assert parent_proxy.sub_obj.value == 30

        #delete
        assert hasattr(parent_proxy, 'value') == True
        delattr(parent_proxy, 'value')
        assert hasattr(parent_proxy, 'value') == False
        parent_proxy.value = 10

        #new object
        newObj = SubObject(40)
        parent_proxy.newObj = newObj
        assert parent_proxy.newObj.value == 40
        assert isinstance(parent_proxy.newObj, DynamicProxy)

        print(str(parent_proxy)) #TODO some Error due to attribute access of dataclass
        #list
        parent_proxy.somelist = [1,2,3]
        assert parent_proxy.somelist[0] == 1
        parent_proxy.somelist.pop(0)#TODO issue: doesn't save again after executing pop
        assert parent_proxy.somelist[0] == 2
        parent_proxy.somelist.append(4)
        assert parent_proxy.somelist[2] == 4

        #dict
        parent_proxy.somedict = {'a':1, 'b':2}
        assert parent_proxy.somedict['a'] == 1
        parent_proxy.somedict.pop('a')
        parent_proxy.somedict['c'] = 3
        assert parent_proxy.somedict['c'] == 3

        #set
        parent_proxy.someset = {1,2,3}
        assert 1 in parent_proxy.someset
        parent_proxy.someset.add(4)
        assert 4 in parent_proxy.someset
        parent_proxy.someset.discard(1)
        assert 1 not in parent_proxy.someset
        other_set = {2,3,4}
        parent_proxy.someset.update(other_set.union(parent_proxy.someset))

        #tuple
        parent_proxy.sometuple = (1,2,3)
        assert parent_proxy.sometuple[0] == 1
        parent_proxy.sometuple = (4,5,6)
        assert parent_proxy.sometuple[0] == 4

        #callables
        parent_proxy.callable = lambda x: x + 1
        assert parent_proxy.callable(1) == 2

unittest.main()
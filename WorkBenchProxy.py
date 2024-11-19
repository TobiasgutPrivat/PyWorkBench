# Probably Similair to DynamicProxy
# 
# Alternative make class extensions like 
# obj.__class__ = type("DynamicClass", (OriginalClass,), {"__str__": custom_str})
# allows to not wrap it and have better intelisense 
# requires loading/unloading attributes
# not sure how to handle dict's, iterables, sets


# wrapping behaviour
# Wrap all sub-objects for proxy handling
# not sure if include all types or just classes (__dict__)
# maybe implement unwrapping option or toggle autowrappihg

# Saving behaviour
# Save after user actions like (create, edit, delete, call function)
# needs to save subobjects as well
# also avoids issue with methods executing after saving
# proxy only saves if specificly called

# Loading behaviour
# Load when accessed

# delete behaviour
# delete in DB when not referenced (like garbage collector)

# unload behaviour
# unload after saving (user action not in _save()) 
# or just not unload
# unloads subobjects via serialization handler

# untrack behaviour
# manually untrack

from Database import createNewObject, getObject, updateObject, clearOrphans, ObjectId
# !!! Debugging can cause unintended loading !!!

#TODO think about how to handle referenced objects in memory

new_objects: dict[int,ObjectId] = {}
proxy_attrs = {"_id", "_obj", "_packages"}

def wrapProxy(value):
    """Wrap sub-objects for proxy handling."""#TODO think about other types (range)
    if isinstance(value, (DynamicProxy,type,int,str,float,complex,bool,bytes,bytearray,type(None))):
        return value
    else: # list, dict, set, normal-objects, callables
        return DynamicProxy(value)

class DynamicProxy:
    _id: int  # take from qdrant
    # _packages: list[str] # TODO track packages needed to import when loading object
    # also think about form of import, because dill references it in according scope
    _obj: object | None

    def __init__(self, obj = object | ObjectId):
        """
        :param obj: If an existing object is passed, it will be wrapped by the proxy.
        """
        if isinstance(obj, ObjectId):
            self._id = obj
            self._obj = None
            return
        if id(obj) in new_objects:
            self._id = new_objects[id(obj)]
            self._obj = None
            return
        self._id = createNewObject(obj)
        new_objects[id(obj)] = self._id
        self._obj = obj
        self._WrapSubObjects()
        #TODO check if object has some attributes with same name as DynamicProxy

    def _WrapSubObjects(self):
        if hasattr(self._obj, '__dict__'):
            for k, v in self._obj.__dict__.items():
                self._obj.__dict__[k] = wrapProxy(v)
        if isinstance(self._obj, dict):
            for k, v in self._obj.items():
                self._obj[k] = wrapProxy(v)
        if isinstance(self._obj, (set, frozenset)):
            self._obj = {wrapProxy(v) for v in self._obj}
        if isinstance(self._obj, tuple):
            self._obj = tuple(wrapProxy(v) for v in self._obj)
        if isinstance(self._obj, (list)):
            for k, v in enumerate(self._obj):
                self._obj[k] = wrapProxy(v)

    def _load(self):
        """Loads the object from disk."""
        if self._obj is None:
            self._obj = getObject(self._id)

    def _save(self, inheriting: bool = True):
        """Saves the object to disk."""
        if inheriting:
            self._saveSubProxies()
        updateObject(self._id, self._obj)

    def _saveSubProxies(self):
        for v in self._getSubProxies():
            v._save(True)

    def _getSubProxies(self):
        if hasattr(self._obj, '__dict__'):
            for v in self._obj.__dict__.values():
                if isinstance(v, DynamicProxy):
                    yield v
        if isinstance(self._obj, dict):
            for v in self._obj.values():
                if isinstance(v, DynamicProxy):
                    yield v
        if isinstance(self._obj, (list, set, tuple)):
            for v in self._obj:
                if isinstance(v, DynamicProxy):
                    yield v

    def _unload(self):
        """Unloads the object without saving."""
        self._obj = None

    def _untrack(self) -> object:
        obj = self._obj
        del self
        return obj

    def __getstate__(self): #always store subobjects unloaded
        self._unload()
        return self.__dict__.copy()

    def __setstate__(self, state):
        self.__dict__.update(state)

    def __getattr__(self, name):
        # if name in proxy_attrs:
        #     return super().__getattribute__(name)
        self._load()
        return getattr(self._obj, name)

    def __setattr__(self, name, value):
        if name in proxy_attrs:
            super().__setattr__(name, value)
        else:
            self._load()
            setattr(self._obj, name, wrapProxy(value))

    def __delattr__(self, name):
        if name in proxy_attrs:
            super().__delattr__(name)
        else:
            self._load()
            delattr(self._obj, name)

    # dunders

    def __getitem__(self, key):
        self._load()
        return self._obj[key]

    def __setitem__(self, key, value):
        self._load()
        self._obj[key] = wrapProxy(value)

    def __delitem__(self, key):
        self._load()
        del self._obj[key]

    def __contains__(self, item):
        self._load()
        return item in self._obj

    def __call__(self, *args, **kwargs):
        self._load()
        return self._obj(*args, **kwargs)

    def __str__(self):
        self._load()
        return self._obj.__str__()

    def __repr__(self):
        self._load()
        return self._obj.__repr__()
    
    def __len__(self):
        self._load()
        return self._obj.__len__()
    
    def __iter__(self):
        self._load()
        return self._obj.__iter__()
    
    def __next__(self):
        self._load()
        return self._obj.__next__()
    
    def __bool__(self):
        self._load()
        return self._obj.__bool__()
    
    def __int__(self):
        self._load()
        return self._obj.__int__()
    
    def __float__(self):
        self._load()
        return self._obj.__float__()
    
    def __complex__(self):
        self._load()
        return self._obj.__complex__()
    
    def __bytes__(self):
        self._load()
        return self._obj.__bytes__()
    
    def __bytearray__(self):
        self._load()
        return self._obj.__bytearray__()
    
    def __index__(self):
        self._load()
        return self._obj.__index__()
    
    def __round__(self):
        self._load()
        return self._obj.__round__()
    
    def __trunc__(self):
        self._load()
        return self._obj.__trunc__()
    
    def __floor__(self):
        self._load()
        return self._obj.__floor__()
    
    def __ceil__(self):
        self._load()
        return self._obj.__ceil__()
    
    def __abs__(self):
        self._load()
        return self._obj.__abs__()
    
    def __add__(self, other):
        self._load()
        return self._obj + other
    
    def __sub__(self, other):
        self._load()
        return self._obj - other
    
    def __mul__(self, other):
        self._load()
        return self._obj * other
    
    def __matmul__(self, other):
        self._load()
        return self._obj @ other
    
    def __truediv__(self, other):
        self._load()
        return self._obj / other
    
    def __floordiv__(self, other):
        self._load()
        return self._obj // other
    
    def __mod__(self, other):
        self._load()
        return self._obj % other
    
    def __pow__(self, other):
        self._load()
        return self._obj ** other
    
    def __lshift__(self, other):
        self._load()

    def __and__(self, other):
        self._load()
        return self._obj & other
        
    def __or__(self, other):
        self._load()
        return self._obj | other
        
    def __xor__(self, other):
        self._load()
        return self._obj ^ other
        
    def __rshift__(self, other):
        self._load()
        return self._obj >> other
        
    def __lshift__(self, other):
        self._load()
        return self._obj << other
        
    def __eq__(self, other):
        self._load()
        return self._obj == other
        
    def __ne__(self, other):
        self._load()
        return self._obj != other
        
    def __lt__(self, other):
        self._load()
        return self._obj < other
        
    def __le__(self, other):
        self._load()
        return self._obj <= other
        
    def __gt__(self, other):
        self._load()
        return self._obj > other
        
    def __ge__(self, other):
        self._load()
        return self._obj >= other
        
    def __neg__(self):
        self._load()
        return -self._obj
        
    def __pos__(self):
        self._load()
        return +self._obj
        
    def __invert__(self):
        self._load()
        return ~self._obj
    #TODO handle more dunders
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
        # self._WrapSubObjects()
        self._obj = obj
        #TODO check if object has some attributes with same name as DynamicProxy

    def _WrapSubObjects(self):
        for k, v in self._obj.__dict__.items():
            self._obj.__dict__[k] = wrapProxy(v)
        #TODO also wrap dict/iterable

    def _load(self):
        """Loads the object from disk."""
        if self._obj is None:
            self._obj = getObject(self._id)

    def _save(self):
        """Saves the object to disk."""
        updateObject(self._id, self._obj)

    def _unload(self):
        """Unloads the object without saving."""
        self._obj = None

    def __getstate__(self): #always store subobjects unloaded
        self._unload()
        return self.__dict__.copy()

    def __setstate__(self, state):
        self.__dict__.update(state)

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
            self._load()  # Load the object before deleting any attributes
            delattr(self._obj, name)

    # def __getitem__(self, key):#TODO potentialy unnecessary
    #     self._load()  # Load the object when an item is accessed
    #     return self._obj[key]

    # def __setitem__(self, key, value):
    #     self._load()  # Load the object before setting any item
    #     # deleteProxy(self._obj[key])
    #     self._obj[key] = wrapProxy(value)
    #     self._save()  # Automatically save after modifying

    # def __delitem__(self, key):
    #     self._load()  # Load the object before deleting an item
    #     # deleteProxy(self._obj[key])
    #     del self._obj[key]
    #     self._save()

    # def __call__(self, *args, **kwargs):#TODO potentialy unnecessary
    #     self._load()  # If the object is callable (has a __call__ method), call it
    #     return self._obj(*args, **kwargs)

    def __str__(self):#TODO potentialy unnecessary
        self._load()
        return self._obj.__str__()

    def __repr__(self):
        attrs = ', '.join(f'{k}={v!r}' for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"
    
    def _untrack(self) -> object:
        obj = self._obj
        del self
        return obj
    
    #TODO handle more dunders
    # dunders which only would require loading can be ignored because, get handled by getattr if not found

def wrapProxy(value):
    """Wrap sub-objects for proxy handling."""#TODO think about other types (range)
    if isinstance(value, (DynamicProxy,type,int,str,float,complex,bool,bytes,bytearray,type(None))):
        return value
    elif isinstance(value, (frozenset,tuple)): # potentially unnecessary
        for x in value:
            wrapProxy(x)
        return value
    else: # list, dict, set, normal-objects, callables
        return DynamicProxy(value)

#TODO delete unused proxies
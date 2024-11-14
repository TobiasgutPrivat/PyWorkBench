from Database import createNewObject, getObject, updateObject, deleteObject
from typing import Iterable
# !!! Debugging can cause unintended loading !!!

#TODO think about how to handle referenced objects in memory
#should work when already proxied, only issue when multiple references in memory and then both get proxied
#maybe solvable by using objectid assuming it's same when referenece is the same

class DynamicProxy:
    _id: str  # take from qdrant
    # _packages: list[str] # TODO track packages needed to import when loading object
    # also think about form of import, because dill references it in according scope
    _obj: object
    # _loaded: bool

    def __init__(self, obj: object|str):
        """:param obj: If an existing object is passed, it will be wrapped by the proxy."""
        if isinstance(obj, str):
            self._id = obj
        else:
            self._id = str(id(obj))
            createNewObject(self._id, obj)
            self._obj = obj
            self._WrapSubObjects()

    def _WrapSubObjects(self):
        if isinstance(self._obj, Iterable):
            for k, v in iter(self._obj):
                self._obj[k] = wrapProxy(v)
        if isinstance(self._obj, dict):
            for k, v in self._obj:
                self._obj[k] = wrapProxy(v)
        if hasattr(self._obj, '__dict__'):
            for k, v in self._obj.__dict__.items():
                self._obj.__dict__[k] = wrapProxy(v)

    def _load(self):
        """Loads the object from disk."""
        # if not self._loaded:
        self._obj = getObject(self._id)
            # self._loaded = True

    def _save(self):
        """Saves the object to disk."""
        updateObject(self._id, self._obj)
        self._obj = None
        # self._unload()

    # def _unload(self):
    #     """Unloads the object without saving."""
    #     if not self._loaded:
    #         return
        
    #     self._unloadSubObjects()
        
    #     self._obj = None
    #     self._loaded = False

    # def _unloadSubObjects(self):
    #     if isinstance(self._obj, Iterable):
    #         for attr_value in self._obj:
    #             if isinstance(attr_value, DynamicProxy):
    #                 attr_value._unload()
    #     if isinstance(self._obj, dict):
    #         for attr_value in self._obj.values():
    #             if isinstance(attr_value, DynamicProxy):
    #                 attr_value._unload()
    #     if hasattr(self._obj, '__dict__'):
    #         for attr_value in self._obj.__dict__.values():
    #             if isinstance(attr_value, DynamicProxy):
    #                 attr_value._unload()

    # def __getstate__(self): #always store subobjects unloaded
    #     # self._unload()
    #     return self.__dict__.copy() #(uses __dict__ of DynamicProxy)

    # def __setstate__(self, state): #load into __dict__
    #     self.__dict__.update(state)

    def __getattr__(self, name): #only called if attribute not found in Dynamicproxy
        self._load()
        value = getattr(self._obj, name)
        self._save()
        return value


def wrapProxy(value):
    """Wrap sub-objects for proxy handling."""
    if isinstance(value, (DynamicProxy,type,int,str,float,complex,bool,bytes,bytearray,type(None))):
        return value
    else:
        return DynamicProxy(value)

#TODO delete unused proxies
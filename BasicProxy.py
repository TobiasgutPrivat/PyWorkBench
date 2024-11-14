from Database import createNewObject, getObject, updateObject, deleteObject
from typing import Any, Iterable
# !!! Debugging can cause unintended loading !!!

#TODO think about how to handle referenced objects in memory
#should work when already proxied, only issue when multiple references in memory and then both get proxied
#maybe solvable by using objectid assuming it's same when referenece is the same

class DynamicProxy:
    new_objects: dict[int,'DynamicProxy'] = {}
    _id: str  # take from qdrant
    # _packages: list[str] # TODO track packages needed to import when loading object
    # also think about form of import, because dill references it in according scope
    _obj: object

    def __init__(self, obj: object|str):
        """:param obj: If an existing object is passed, it will be wrapped by the proxy."""
        if isinstance(obj, str):
            self._id = obj
        else:
            if id(obj) in DynamicProxy.new_objects:
                self = DynamicProxy.new_objects[id(obj)]
                return
            self._id = createNewObject(self._id, obj)
            createNewObject(self._id, obj)
            self._obj = obj
            self._WrapSubObjects()
            DynamicProxy.new_objects[id(obj)] = self

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

    def __getattr__(self, name):
        return getattr(getObject(self._id), name)
    
    def __setattr__(self, name: str, value: Any) -> None:
        obj = getObject(self._id)
        setattr(obj, name, value)
        updateObject(self._id, obj)

    def __setitem__(self, key, value):
        obj = getObject(self._id)
        obj[key] = value
        updateObject(self._id, obj)

    def __delattr__(self, name):
        obj = getObject(self._id)
        delattr(obj, name)
        updateObject(self._id, obj)

    def __delitem__(self, key):
        obj = getObject(self._id)
        del obj[key]
        updateObject(self._id, obj)

def wrapProxy(value):
    """Wrap sub-objects for proxy handling."""
    if isinstance(value, (DynamicProxy,type,int,str,float,complex,bool,bytes,bytearray,type(None))):
        return value
    else:
        return DynamicProxy(value)

#TODO delete unused proxies
from Database import createNewObject, getObject, updateObject, deleteObject
# obj.__class__ = type("DynamicClass", (OriginalClass,), {"__str__": custom_str})
# allows to not wrap it and have better intelisense 
# requires loading/unloading attributes
# not sure how to handle dict's, iterables, sets

ExtendedClasses: dict[type,type] = {}

def _load(self):
    if not self._loaded:
        self.__dict__.append(getObject(self._id))
        self._loaded = True

def _save(self):
    updateObject(self._id, {key: value for key, value in self.__dict__.items() 
                    if key not in ["_id", "_loaded"]})
    self._unload()

def _unload(self):
    if self._loaded:
        self.__dict__ = {"_id": self._id, "_loaded": False}

def _getattr(self, name):
    self._load()
    return super().__getattribute__(self, name)

def _setattr(self, name, value):
    self._load()
    return super().__setattr__(self, name, value)

def _getstate(self):
    self._unload()
    return self.__dict__.copy()

def _setstate(self, state):
    self.__dict__.update(state)

dunders: dict[str, function] = {
    "_load": _load,
    "_unload": _unload,
    "_save": _save,
    "__getstate__": _getstate,
    "__setstate__": _setstate,
    "__getattr__": _getattr,
}

def wrapProxy(value: object) -> None:
    if isinstance(value, (type,int,str,float,complex,bool,bytes,bytearray,type(None))):
        return
    if value.__class__ in ExtendedClasses.values():
        return
    if value.__class__ in ExtendedClasses:
        value.__class__ = ExtendedClasses[value.__class__]
        return
    orgType: type = value.__class__
    value.__class__ = type(
        "Extend" + orgType.__name__, 
        (orgType,), 
        dunders
    )
    ExtendedClasses[orgType] = value.__class__
    value._loaded = True
    value._id = createNewObject(value)

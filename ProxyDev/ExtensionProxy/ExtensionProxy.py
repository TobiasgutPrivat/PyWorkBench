from Database import createNewObject, getObject, updateObject, clearOrphans
# obj.__class__ = type("DynamicClass", (OriginalClass,), {"__str__": custom_str})
# allows to not wrap it and have better intelisense 
# requires loading/unloading attributes
# not sure how to handle dict's, iterables, sets
# allows dunder method access by inheritence
# maybe also no issue with isinstance

ExtendedClasses: dict[type,type] = {}

def make_dynamic_class(orgType: type) -> type:
    """Dynamically create a class with the required methods and ensure __class__ cell is available."""
    
    class ExtendDynamic(orgType):
        def _load(self):
            if not self._loaded:
                self._loaded = True
                self.__dict__.update(getObject(self._id))

        def _save(self):
            updateObject(self._id, self.getData())
            self._unload()

        def getData(self):
            return {key: value for key, value in self.__dict__.items()
                if key not in ["_id", "_loaded"]}

        def _unload(self):
            if self._loaded:
                self.__dict__ = {"_id": self._id} if hasattr(self, "_id") else {}
                self._loaded = False

        def __getattr__(self, name):
            self._load()
            return super().__getattribute__(name)

        def __setattr__(self, name, value):
            if name not in ["_id", "_loaded"]:
                self._load()
            super().__setattr__(name, value)

        def __getstate__(self):
            self._unload()
            return self.__dict__.copy()

        def __setstate__(self, state):
            self.__dict__.update(state)
    
    # Return the dynamically created class
    return ExtendDynamic

def wrapProxy(value: object) -> None:
    if isinstance(value, (type, int, str, float, complex, bool, bytes, bytearray, type(None))):
        return
    if value.__class__ in ExtendedClasses.values():
        return
    if value.__class__ in ExtendedClasses:
        value.__class__ = ExtendedClasses[value.__class__]
        return

    orgType: type = value.__class__

    # Dynamically create the extended class
    extended_class = make_dynamic_class(orgType)
    
    # Cache the extended class
    ExtendedClasses[orgType] = extended_class
    
    # Assign the extended class to the object
    value.__class__ = extended_class

    # Initialize custom attributes
    value._loaded = True
    value._id = createNewObject(value.getData())


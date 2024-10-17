from Database import createNewObject, getObject, updateObject

class DynamicProxy:
    _id: int  # take from qdrant
    # _packages: list[str] # TODO track packages needed to import when loading object
    _obj: object
    _loaded: bool

    def __init__(self, obj=None):
        """
        :param obj: If an existing object is passed, it will be wrapped by the proxy.
        """
        self._id = createNewObject(obj)
        self._loaded = True
        self._obj = obj

        for v in obj.__dict__:
            wrapProxy(v)

    def _load(self):
        """Loads the object from disk."""
        if not self._loaded:
            self._obj = getObject(self._id)
            self._loaded = True

    def _save(self):
        """Saves the object to disk."""
        updateObject(self._id, self._obj)
        self._loaded = False  # (Optionally) unload after saving
        self._obj = None

    def __getattr__(self, name):
        """Loads the object when an attribute is accessed"""
        self._load()
        return getattr(self._obj, name)

    def __setattr__(self, name, value):
        if name in ['_id', '_packages', '_obj', '_loaded']:
            super().__setattr__(name, value)
        else:
            self._load()
            setattr(self._obj, name, wrapProxy(value))
            self._save()  # Automatically save after modifying

    def __delattr__(self, name):
        if name in ['_id', '_packages', '_obj', '_loaded']:
            super().__delattr__(name)
        else:
            self._load()  # Load the object before deleting any attributes
            delattr(self._obj, name)
            self._save()

    def __getitem__(self, key):
        self._load()  # Load the object when an item is accessed
        return self._obj[key]

    def __setitem__(self, key, value):
        self._load()  # Load the object before setting any item
        self._obj[key] = wrapProxy(value)
        self._save()  # Automatically save after modifying

    def __delitem__(self, key):
        self._load()  # Load the object before deleting an item
        del self._obj[key]
        self._save()

    def __call__(self, *args, **kwargs):
        self._load()  # If the object is callable (has a __call__ method), call it
        return self._obj(*args, **kwargs)

    def __str__(self):
        return f"<{self._obj.__class__.__name__}>{self._obj}"

    def __repr__(self):
        # Use the __dict__ to dynamically capture all attributes and their values
        attrs = ', '.join(f'{k}={v!r}' for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"

def wrapProxy(value):
    """Wrap sub-objects for proxy handling."""
    if isinstance(value, (DynamicProxy,type,int,str,float,complex,bool,bytes,bytearray,type(None))):
        return value
    elif isinstance(value, (frozenset,tuple)):
        for x in value:
            wrapProxy(x)
        return value
    else:
        return DynamicProxy(value)

from Database import createNewObject, getObject, updateObject, deleteObject

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

    def __getitem__(self, key):#TODO potentialy unnecessary
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

    def __call__(self, *args, **kwargs):#TODO potentialy unnecessary
        self._load()  # If the object is callable (has a __call__ method), call it
        return self._obj(*args, **kwargs)

    def __str__(self):#TODO potentialy unnecessary
        self._load()
        return self._obj.__str__()

    def __repr__(self):
        attrs = ', '.join(f'{k}={v!r}' for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"
    
    def __del__(self):
        # TODO think about this
        # should not be deleted when application closes, or remove from memory
        # TODO handle Memory deletion without DB deletion
        # should delete when used by some unknown functionality, or active delete
        deleteObject(self._id) 
        # probably good to make DB backups

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
    elif isinstance(value, (frozenset,tuple)):
        for x in value:
            wrapProxy(x)
        return value
    else: # list, dict, set, normal-objects, callables
        return DynamicProxy(value)

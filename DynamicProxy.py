import pickle

class DynamicProxy:
    _id: int  # take from qdrant
    _name: str
    _cls: type
    _obj: object
    _loaded: bool

    def __init__(self, name, obj=None, cls=None, *args, **kwargs):
        """
        :param name: The path where the object will be serialized.
        :param obj: If an existing object is passed, it will be wrapped by the proxy.
        :param cls: If creating a new object, this is the class of the object.
        :param args, kwargs: Arguments for the class constructor if creating a new object.
        """
        self._id = id(self)
        self._name = name  # (Optional) 
        self._cls = cls  # The class type for creating new instances
        self._obj = obj  # Track if an object is passed or not
        self._loaded = bool(obj)  # Loaded if obj is passed

        if not self._loaded and cls is not None:
            self._obj = self._cls(*args, **kwargs)  # Create new instance
            self._loaded = True
        else:
            # Proxyfy subobjects if the object is a collection
            self.wrap_collection(obj)

    def wrap_collection(self, obj):
        """Wrap collections (lists, sets, dicts) in DynamicProxy."""
        if isinstance(obj, list):
            self._obj = [DynamicProxy(f"{self._name}_item_{i}", item) for i, item in enumerate(obj)]
        elif isinstance(obj, set):
            self._obj = {DynamicProxy(f"{self._name}_item_{item}", item) for item in obj}
        elif isinstance(obj, dict):
            self._obj = {key: DynamicProxy(f"{self._name}_item_{key}", value) for key, value in obj.items()}

    def _load(self):
        """Loads the object from disk."""
        if not self._loaded:
            with open(self._name + '.pkl', 'rb') as f:
                self._obj = pickle.load(f)
            self.wrap_collection(self._obj)  # Wrap subcollections
            self._loaded = True

    def _save(self):
        """Saves the object to disk."""
        # Save subproxy objects first
        with open(self._name + '.pkl', 'wb') as f:
            pickle.dump(self._obj, f)
        self._loaded = False  # (Optionally) unload after saving
        self._obj = None

    def __getattr__(self, name):
        if name in ['_id', '_name', '_cls', '_obj', '_loaded']:
            return super().__getattr__(name)
        self._load()  # Load the object when an attribute is accessed
        return getattr(self._obj, name)

    def __setattr__(self, name, value):
        if name in ['_id', '_name', '_cls', '_obj', '_loaded']:
            super().__setattr__(name, value)
        else:
            self._load()  # Load the object before setting any attributes
            setattr(self._obj, name, wrap_subobject(value))
            self._save()  # Automatically save after modifying

    def __delattr__(self, name):
        if name in ['_id', '_name', '_cls', '_obj', '_loaded']:
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
        self._obj[key] = wrap_subobject(value)
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

def wrap_subobject(value):
    """Wrap sub-objects for proxy handling."""
    if isinstance(value, (list, set, dict)):
        return DynamicProxy("wrapped_collection", value)
    return value

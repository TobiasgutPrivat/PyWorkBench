import pickle
import os

class DynamicProxy:
    def __init__(self, file_path, obj=None, cls=None, *args, **kwargs):
        """
        :param file_path: The path where the object will be serialized.
        :param obj: If an existing object is passed, it will be wrapped by the proxy.
        :param cls: If creating a new object, this is the class of the object.
        :param args, kwargs: Arguments for the class constructor if creating a new object.
        """
        self._file_path = file_path
        self._cls = cls  # The class type for creating new instances
        self._obj = obj  # Track if an object is passed or not
        self._loaded = bool(obj)  # Loaded if obj is passed

        if not self._loaded and os.path.exists(self._file_path):
            self._load()  # Load from disk if it exists
        elif not self._loaded and cls is not None:
            self._obj = self._cls(*args, **kwargs)  # Create new instance
            self._loaded = True

    def _load(self):
        """Loads the object from disk."""
        if not self._loaded:
            with open(self._file_path, 'rb') as f:
                self._obj = pickle.load(f)
            self._loaded = True

    def _save(self):
        """Saves the object to disk."""
        with open(self._file_path, 'wb') as f:
            pickle.dump(self._obj, f)
        self._loaded = False  # Optionally unload after saving

    def __getattr__(self, name):
        if name in ['_file_path', '_cls', '_obj', '_loaded']:
            # Handle proxy attributes separately
            super().__getattr__(name)
        else:
            self._load()  # Load the object when an attribute is accessed
            return getattr(self._obj, name)

    def __setattr__(self, name, value):
        if name in ['_file_path', '_cls', '_obj', '_loaded']:
            # Handle proxy attributes separately
            super().__setattr__(name, value)
        else:
            self._load()  # Load the object before setting any attributes
            
            if isinstance(value, object) and not isinstance(value, (int, float, str, bool, bytes, list, dict, set)):
                subobject_path = f"{self._file_path}_{name}.pkl"
                value = DynamicProxy(subobject_path, obj=value)  # Wrap the new object

            setattr(self._obj, name, value)
            self._save()  # Automatically save after modifying

    #TODO handle list, dict, set

    def __call__(self, *args, **kwargs):
        self._load()  # If the object is callable (has a __call__ method), call it
        return self._obj(*args, **kwargs)
    
    def __str__(self):
        return f"{type(self._obj).__name__}({self._obj})"
    
    def __repr__(self):
        return f"DynamicProxy(file_path:{self._file_path}, loaded:{self._loaded}, obj({type(self._obj).__name__}({self._obj})))"
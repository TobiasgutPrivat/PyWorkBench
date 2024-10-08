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
        self._args = args
        self._kwargs = kwargs
        self._obj = obj  # Track if an object is passed or not
        self._loaded = bool(obj)  # Loaded if obj is passed

        if not self._loaded and os.path.exists(self._file_path):
            self._load()  # Load from disk if it exists
        elif not self._loaded and cls is not None:
            self._obj = self._cls(*self._args, **self._kwargs)  # Create new instance
            self._loaded = True
            self._save()  # Immediately save the new object
        else:
            self._save()  # Immediately save the new object


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
        self._load()  # Load the object when an attribute is accessed
        attr = getattr(self._obj, name)

        # If the attribute is a complex subobject, wrap it in a proxy
        if isinstance(attr, object) and not isinstance(attr, (int, float, str, bool, bytes, list, dict, set)):
            # Create a file for the subobject to be saved independently
            subobject_path = f"{self._file_path}_{name}.pkl"
            return DynamicProxy(subobject_path, obj=attr)

        return attr

    def __setattr__(self, name, value):
        if name in ['_file_path', '_cls', '_args', '_kwargs', '_obj', '_loaded']:
            # Handle proxy attributes separately
            super().__setattr__(name, value)
        else:
            self._load()  # Load the object before setting any attributes
            setattr(self._obj, name, value)
            self._save()  # Automatically save after modifying

    def __call__(self, *args, **kwargs):
        self._load()  # If the object is callable (has a __call__ method), call it
        return self._obj(*args, **kwargs)

    def save(self):
        """Explicitly save the object if needed."""
        self._save()
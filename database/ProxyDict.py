class ProxyDict(dict):
    def __init__(self, wrapped_dict, proxy):
        super().__init__(wrapped_dict)
        self.proxy = proxy

    def __setitem__(self, key, value):
        if isinstance(value, object) and not isinstance(value, (int, float, str, bool, bytes, list, dict, set)):
            value = self.proxy._wrap_subobject(value, f"dict_item_{key}")
        super().__setitem__(key, value)
        self.proxy._save()  # Save the modified dictionary

    def pop(self, key):
        value = super().pop(key)
        self.proxy._save()  # Save the modified dictionary
        return value

    # Add other dict operations similarly...

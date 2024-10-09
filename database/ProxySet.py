class ProxySet(set):
    def __init__(self, wrapped_set, proxy):
        super().__init__(wrapped_set)
        self.proxy = proxy

    def add(self, item):
        if isinstance(item, object) and not isinstance(item, (int, float, str, bool, bytes, list, dict, set)):
            item = self.proxy._wrap_subobject(item, 'set_item')
        super().add(item)
        self.proxy._save()  # Save the modified set

    def remove(self, item):
        super().remove(item)
        self.proxy._save()

    # Add other set operations similarly...

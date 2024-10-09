class ProxyList(list):
    def __init__(self, wrapped_list, proxy):
        super().__init__(wrapped_list)
        self.proxy = proxy  # Reference to parent proxy

    def append(self, item):
        # Automatically wrap new complex objects if necessary
        if isinstance(item, object) and not isinstance(item, (int, float, str, bool, bytes, list, dict, set)):
            item = self.proxy._wrap_subobject(item, 'list_item')
        super().append(item)
        self.proxy._save()  # Save the modified list

    def remove(self, item):
        super().remove(item)
        self.proxy._save()  # Save the modified list

    # Add other list operations (extend, insert, pop, etc.) similarly...

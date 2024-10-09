from DynamicProxy import wrap_subobject
class ProxySet(set):
    def __init__(self, original_set):
        super().__init__(original_set)

    def add(self, item):
        super().add(wrap_subobject(item))

    # def remove(self, item):#TODO maybe change to delete in database
    #     super().remove(item)
    #     self.proxy._save()

    # Add other set operations similarly...

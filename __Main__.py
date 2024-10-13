import ttkbootstrap as ttk # type: ignore
from json import dumps
from DynamicProxy import DynamicProxy
from dataclasses import dataclass

# Step 1: Define your classes
@dataclass
class SubObject:
    sub_val: int
    def __init__(self, sub_val):
        self.sub_val = sub_val

    def __repr__(self):
        # Use the __dict__ to dynamically capture all attributes and their values
        attrs = ', '.join(f'{k}={v!r}' for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"

@dataclass
class ParentObject:
    value: int
    sub_obj: SubObject

    def __init__(self, value):
        self.value = value
        self.sub_obj = SubObject(value * 2)

    def __repr__(self):
        # Use the __dict__ to dynamically capture all attributes and their values
        attrs = ', '.join(f'{k}={v!r}' for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"

# Step 1: Create and wrap the parent object
# parent = ParentObject(10)
# parent_proxy = DynamicProxy(parent)

# # Step 2: Add a new subobject (it will be automatically wrapped and tracked)

# parent_proxy.new_attr = SubObject(100)
# print("saved:")
# print(parent_proxy.__repr__())
# print("")
# print("get: ", parent_proxy.new_attr.sub_val)
# print("loaded")
# print(parent_proxy.__repr__())
# parent_proxy._save()
# print("")
# print("saved")
# print(parent_proxy.__repr__())

# # Example usage
# my_list = [1, 2, 3]
# my_proxy = DynamicProxy(my_list)

# # Accessing an element
# print(my_proxy[0])  # This will trigger loading if not already loaded

# # Modifying the collection
# my_proxy[1] = 5  # This will also trigger loading and save the updated state

# print(my_proxy)
# # Saving the collection
# my_proxy._save()  # Save the current state to disk


from WeaviateDB import is_live
print(is_live())
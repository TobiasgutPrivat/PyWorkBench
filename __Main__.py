import ttkbootstrap as ttk # type: ignore
from DynamicProxy import DynamicProxy
from dataclasses import dataclass

# Step 1: Define your classes
@dataclass
class SubObject:
    sub_val: int
    def __init__(self, sub_val):
        self.sub_val = sub_val

@dataclass
class ParentObject:
    value: int
    sub_obj: SubObject

    def __init__(self, value):
        self.value = value
        self.sub_obj = SubObject(value * 2)

# Step 1: Create and wrap the parent object
parent = ParentObject(10)
parent_proxy = DynamicProxy('parent_object.pkl', obj=parent)

# Step 2: Add a new subobject (it will be automatically wrapped and tracked)
parent_proxy.new_attr = SubObject(100)
print(parent_proxy)

# Access and modify the new attribute
print(parent_proxy.new_attr.sub_val)  # Output: 100

print(parent_proxy)#TODO check why still returns sub_val 20

# Change the value (it will be saved automatically)
parent_proxy.new_attr.sub_val = 200

print(parent_proxy.new_attr.sub_val)  # Output: 100

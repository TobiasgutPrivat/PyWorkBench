import ttkbootstrap as ttk
from DynamicProxy import DynamicProxy

# Step 1: Define your classes
class SubObject:
    def __init__(self, sub_val):
        self.sub_val = sub_val

    def __str__(self):
        return f"sub_val: {self.sub_val}"

class ParentObject:
    def __init__(self, value):
        self.value = value
        self.sub_obj = SubObject(value * 2)

    def __str__(self):
        return f"value: {self.value}, SubObject({self.sub_obj})"

# Step 1: Create and wrap the parent object
parent = ParentObject(10)
parent_proxy = DynamicProxy('parent_object.pkl', obj=parent)

# Step 2: Add a new subobject (it will be automatically wrapped and tracked)
parent_proxy.new_attr = SubObject(100)

# Access and modify the new attribute
print(parent_proxy.new_attr.sub_val)  # Output: 100

print(parent_proxy)#TODO check why still returns sub_val 20

# Change the value (it will be saved automatically)
parent_proxy.new_attr.sub_val = 200

print(parent_proxy.new_attr.sub_val)  # Output: 100

import ttkbootstrap as ttk
from DynamicProxy import DynamicProxy

# Step 1: Define your classes
class SubObject:
    def __init__(self, sub_val):
        self.sub_val = sub_val

class ParentObject:
    def __init__(self, value):
        self.value = value
        self.sub_obj = SubObject(value * 2)

# Create the object normally
parent = ParentObject(10)

# Wrap the object in the proxy
parent_proxy = DynamicProxy('parent_object.pkl', obj=parent)

# Add a new attribute or modify an existing one
parent_proxy.new_attr = SubObject(100)  # Adding a new subobject
print(parent_proxy.new_attr.sub_val)  # Output: 100
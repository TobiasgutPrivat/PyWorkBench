import ttkbootstrap as ttk # type: ignore
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
parent = ParentObject(10)
parent_proxy = DynamicProxy('parent_object.pkl', obj=parent)

# Step 2: Add a new subobject (it will be automatically wrapped and tracked)
parent_proxy.new_attr = SubObject(100)

# Access and modify the new attribute
print(parent_proxy.new_attr.sub_val)  # Output: 100

# Change the value (it will be saved automatically)
parent_proxy.new_attr.sub_val = 200

print(parent_proxy.new_attr.sub_val)  # Output: 100

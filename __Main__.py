import ttkbootstrap as ttk # type: ignore

# Step 1: Define your classes


# Step 1: Create and wrap the parent object


# Step 2: Add a new subobject (it will be automatically wrapped and tracked)

print("saved:")
print(parent_proxy.__repr__())
print("")
print("get: ", parent_proxy.new_attr.name)
print("loaded")
print(parent_proxy.__repr__())
parent_proxy._save()
print("")
print("saved")
print(parent_proxy.__repr__())

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

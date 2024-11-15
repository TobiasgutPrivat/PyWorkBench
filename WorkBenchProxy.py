# Probably Similair to DynamicProxy
# 
# Alternative make class extensions like 
# obj.__class__ = type("DynamicClass", (OriginalClass,), {"__str__": custom_str})
# allows to not wrap it and have better intelisense 
# requires loading/unloading attributes
# not sure how to handle dict's, iterables, sets


# wrapping behaviour
# Wrap all sub-objects for proxy handling
# not sure if include all types or just classes (__dict__)

# Saving behaviour
# Save after user actions like (create, edit, delete, call function)
# needs to include subobjects

# Loading behaviour
# Load when accessed

# delete behaviour
# delete in DB when not referenced (like garbage collector)

# unload behaviour
# unload when saved / not unload
# unloads subobjects via serialization handler

# untrack behaviour
# manually untrack
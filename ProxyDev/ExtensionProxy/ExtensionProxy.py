from Database import createNewObject, getObject, updateObject, deleteObject
# obj.__class__ = type("DynamicClass", (OriginalClass,), {"__str__": custom_str})
# allows to not wrap it and have better intelisense 
# requires loading/unloading attributes
# not sure how to handle dict's, iterables, sets

ExtendedClasses: dict[type,type] = {}

dunders: dict[str, function] = {}

def wrapProxy(value: object) -> None:
    if isinstance(value, (type,int,str,float,complex,bool,bytes,bytearray,type(None))):
        return
    if value.__class__ in ExtendedClasses.values():
        return
    if value.__class__ in ExtendedClasses:
        value.__class__ = ExtendedClasses[value.__class__]
        return
    orgType: type = value.__class__
    value.__class__ = type(
        "Extend" + orgType.__name__, 
        (orgType,), 
        dunders
    )
    ExtendedClasses[orgType] = value.__class__

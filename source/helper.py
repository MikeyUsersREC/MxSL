########################################
# HELPER FUNCTIONS
########################################

def create(fieldname, attr_to_access, instify=False):
    if instify:
        def _selfref(cls):
            setattr(cls, fieldname, cls(attr_to_access))
            return cls
    else:
        def _selfref(cls):
            setattr(cls, fieldname, getattr(cls, attr_to_access))
            return cls

    return _selfref

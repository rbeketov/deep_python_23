class CustomMeta(type):
    @staticmethod
    def _place_valid_names(classdict, name):
        valid_classdict = {}
        for attr_name, attr_value in classdict.items():
            if attr_name.startswith(f"_{name}__"):
                real_name = attr_name[1+len(name)+2:]
                valid_classdict[f"_{name}__custom_{real_name}"] = attr_value
            elif attr_name.startswith("_") and not attr_name.endswith("__"):
                valid_classdict[f"_custom{attr_name}"] = attr_value
            elif not attr_name.startswith("__") and not attr_name.endswith("__"):
                valid_classdict[f"custom_{attr_name}"] = attr_value
            else:
                valid_classdict[attr_name] = attr_value

        return valid_classdict

    def __new__(mcs, name, bases, classdict, **kwargs):
        def custom_setattr(self, name_input, value_input):
            valid = mcs._place_valid_names({name_input: value_input}, name)
            for attr_name, attr_value in valid.items():
                super(type(self), self).__setattr__(attr_name, attr_value)

        valid_classdict = mcs._place_valid_names(classdict, name)
        valid_classdict['__setattr__'] = custom_setattr
        cls = super().__new__(mcs, name, bases, valid_classdict)
        return cls

    def __init__(cls, name, bases, classdict, **kwargs):
        super().__init__(name, bases, classdict, **kwargs)

    def __call__(cls, *args, **kwargs):
        return super().__call__(*args, **kwargs)

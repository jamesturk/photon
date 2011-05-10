""" CEnum & supporting classes, based on idea from Mike Bayer
    see http://techspot.zzzeek.org/2011/01/14/the-enum-recipe/
"""

class CEnumSymbol(int):
    def __new__(cls, name, value, description, **kwargs):
        val = super(CEnumSymbol, cls).__new__(cls, value)
        val.name = name
        val.description = description
        return val

    def __repr__(self):
        return "<%s>" % self.name

class CEnumMeta(type):
    def __init__(cls, classname, bases, dict_):
        cls._reg = reg = cls._reg.copy()
        for k, v in dict_.items():
            if isinstance(v, tuple):
                sym = reg[v[0]] = CEnumSymbol(k, *v)
                setattr(cls, k, sym)
            elif isinstance(v, int):
                sym = reg[v] = CEnumSymbol(k, v, k)
                setattr(cls, k, sym)
        return type.__init__(cls, classname, bases, dict_)

    def __iter__(cls):
        return iter(cls._reg.values())

class CEnum(object):
    __metaclass__ = CEnumMeta
    _reg = {}

    @classmethod
    def from_int(cls, value):
        try:
            return cls._reg[value]
        except KeyError:
            raise ValueError(
                    "Invalid value for %r: %r" %
                    (cls.__name__, value)
                )

    @classmethod
    def values(cls):
        return cls._reg.keys()

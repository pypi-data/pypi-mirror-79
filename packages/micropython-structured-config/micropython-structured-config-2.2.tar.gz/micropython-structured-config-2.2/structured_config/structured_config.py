# Micropython structured_config based on https://gitlab.com/alelec/structured_config
import errno
import ujson
import copy
from pathlib import Path
from collections import OrderedDict

try:
    import copy
    copy.dispatch_table
except AttributeError:
    copy.dispatch_table = {}

_deepcopy_dispatch = getattr(copy, "_deepcopy_dispatch")
if OrderedDict not in _deepcopy_dispatch:
    _deepcopy_dispatch[OrderedDict] = _deepcopy_dispatch[dict]

from copy import copy, deepcopy

OMIT_VALUE = object()

class Structure:

    def __new__(cls, *args, **kwargs):
        __template = "__" + cls.__name__
        if not hasattr(cls, __template):
            # Copy the attributes from the class def to a new
            # template dict so we can delete the (shared) class
            # attributes
            __data__ = OrderedDict()

            if cls is not Structure and Structure not in cls.__bases__:
                # Ensure base classes have been correctly templated first
                for c in cls.__bases__:
                    if issubclass(c, Structure):
                        __data__.update(c().__template__())

            if hasattr(cls, '__dict__'):
                # preserves proper field ordering in micropython
                keys = cls.__dict__.keys()
            else:
                keys = dir(cls)
            for key in keys:
                if key.startswith('_'):
                    continue
                value = getattr(cls, key)
                __data__[key] = _instantiated(value)
                delattr(cls, key)
            setattr(cls, __template, __data__)
            for field in __data__.values():
                if hasattr(field, '_fields_registered'):
                    field._fields_registered(__data__)

        # Create instance
        self = object.__new__(cls)
        _inst = OrderedDict()

        # Ensure instance has copy of attributes and defaults from definition
        template = getattr(cls, __template)
        for key, value in template.items():
            field_initialiser = getattr(value, "_field_initialiser", lambda: deepcopy(value))
            value = field_initialiser()
            if value != OMIT_VALUE:
                _inst[key] = value

        self.__keys__ = _inst.keys()
        self.__group__ = ""
        self._configfile = None
        self._readonly = False
        self._inst = _inst
        self._isset = set()
        return self

    @classmethod
    def __template__(cls):
        return getattr(cls, "__" + cls.__name__)

    def __call__(self, *args, **kwargs):
        return self

    def __init__(self, *args, **kwargs):
        if args:
            if not isinstance(args[0], (str, Path)):
                raise ValueError("%s: arg[0] should be config file, not %s" % (self.__class__.__name__, args[0]))
            self._configfile = ConfigFile(args[0], self)

        for key, val in kwargs.items():
            self[key] = val

    def __items__(self):
        for key in self.__keys__:
            if key.startswith('_'):
                continue
            yield key, getattr(self, key)

    def __len__(self):
        return len(self._inst)

    __iter__ = __items__

    def __contains__(self, item):
        return item in self.__keys__

    def __setattr__(self, key, value):
        """
        This function is replaced by __setitem__ once the structure object is created
        """
        object.__setattr__(self, key, value)
        if key == '_inst':
            object.__setattr__(self, '__setattr__', self.__setitem__)

    def __setitem__(self, key, value):
        if self._readonly:
            raise AttributeError("Cannot change values of readonly", self.__class__.__name__)
        try:
            field = self.__template__()[key]
            self._isset.add(key)
            update_field = getattr(field, '_update_field', None)
            if update_field:
                update_field(self._inst.get(key, None), value, parent=self)
            else:
                convert_value = getattr(field or value, 'converter', None)
                if convert_value:
                    value = convert_value(value)
                if value is not OMIT_VALUE:
                    self._inst[key] = value
                else:
                    self._isset.remove(key)
                    del self._inst[key]
        except KeyError:
            if key.startswith("_"):
                object.__setattr__(self, key, value)
            else:
                raise

    def __dir__(self):
        return self.__keys__

    def __getattr__(self, item):
        try:
            return self.__getitem__(item)
        except KeyError as ex:
            raise AttributeError(ex.args[0])

    def __getitem__(self, item):
        return self._inst[item]

    def __repr__(self):
        return "<%s:{%s}>" % (self.__class__.__name__, ', '.join(("%s:%s" % i for i in self)))

    def __eq__(self, other):
        if type(other).__name__ == type(self).__name__:
            for key, ival in self._inst.items():
                try:
                    oval = other[key]
                except KeyError:
                    return False
                if ival != oval:
                    return False
            return True

    def __deepcopy__(self, memo):
        n = self.__class__(
            **deepcopy(
                {key: self._inst[key] for key in self.__keys__}, memo
            )
        )
        n.__group__ = self.__group__
        return n

    def __save__(self, checksum=False):
        conf = self._configfile
        if not conf:
            raise ValueError("No config file set")
        conf.dump(checksum=checksum)
        return self

    @property
    def __validated__(self):
        if self._configfile:
            return self._configfile.validated
        return None

    def __fgroup__(self, field):
        """
        Returns the __group__ for the given field
        :param str field: structure field to get doc for
        :return: str
        """
        return self.__template__().get(field).__group__

    def __fdoc__(self, field=None):
        """
        Returns the __doc__ for the given field
        :param str field: structure field to get doc for
        :return: str
        """
        return self.__template__().get(field).__doc__

    def __serialise__(self, raw=False):
        ret = OrderedDict()
        for key, val in self._inst.items():
            field = self.__template__()[key]
            if hasattr(val, '__serialise__'):
                val = val.__serialise__(raw=True)
            elif hasattr(field, '__serialise__'):
                if isinstance(field, Field):
                    # TODO fields should have static serialise accessor
                    new_val = deepcopy(field)
                    new_val.value = val
                    val = new_val
                val = val.__serialise__(raw=True)
            else:
                val = OrderedDict(type=type(val).__name__, value=[val])
            ret[key] = val

        ret = OrderedDict(
            type="Structure",
            name=self.__class__.__name__,
            fields=ret
        )
        if self.__group__:
            ret["group"] = self.__group__
        return ret if raw else ujson.dumps(ret)

    def _field_initialiser(self):
        return deepcopy(self)

    @staticmethod
    def _update_field(_structure, conf, parent=None, ignore_errors=False):
        if conf is None:
            return

        if type(conf) not in (type(_structure), dict, OrderedDict):
            raise TypeError("conf be either a matching type or a dict: %s" % type(conf))

        warn = []
        set_keys = 0
        num_keys = len(conf)
        _structure._isset = set()
        for key, field in _structure.__template__().items():
            if key not in _structure and key not in conf:
                # A deprecated field not have a value in either structure or incoming
                continue

            if key not in conf and key in _structure._isset:
                print("Skipping key '%s': absent in incoming structure and has already been set" % key)
                continue

            update_field = getattr(field, '_update_field', None)
            if update_field:
                update_field(_structure._inst.get(key, None), conf.get(key, None),
                                parent=_structure, ignore_errors=ignore_errors)
                set_keys += 1 if key in conf else 0
            else:
                if key in conf:
                    _structure[key] = conf[key]
                    set_keys += 1
                else:
                    warn.append("WARN: Config file does not contain %s, default will be used" % key)

        if not ignore_errors:
            extra = []
            if set_keys != num_keys:
                # There are extra keys in the config file, it's probably the incorrect structure
                for key in conf:
                    if key not in _structure:
                        extra.append(key)

                raise AttributeError("Config file has extra keys: %s" % extra)

            for msg in warn:
                print(msg)

    @staticmethod
    def _unwrap_value(structure):
        fields = structure.__template__()
        return { key: maybe_unwrap_value(value, fields[key]) for key, value in structure._inst.items() }


def _instantiated(cls):
    if type(cls) == type and issubclass(cls, (Structure, List, Dict)):
        return cls()
    return cls


def maybe_unwrap_value(val, field=None):
    unwrap_field = getattr(field or val, '_unwrap_value', None)
    if unwrap_field:
        val = unwrap_field(val)
    elif isinstance(val, list):
        val = List._unwrap_value(val)
    elif isinstance(val, dict):
        val = Dict._unwrap_value(val)
    return val

def __deserialise__(ser):
    def _issubclass(cls, t):
        try:
            return issubclass(cls, t)
        except TypeError:
            return False

    types = OrderedDict(str=str, int=int, float=float, bool=bool, Field=Field, NoneType= lambda *_:None, **{
        k: t for k, t in globals().items() if _issubclass(t, Field)
    })

    if isinstance(ser, str):
        ser = ujson.loads(ser)

    def new_structure(defs):
        fields = OrderedDict()
        for k, v in defs['fields'].items():
            fields[k] = decode(v)
        return type(defs['name'], (Structure,), fields)

    def decode(item):
        if item['type'] == 'Structure':
            t = new_structure(item)
            cls = types.get(item['name'], t)
            types[item['name']] = cls
            obj = cls(**OrderedDict(t().__items__()))
        elif item['type'] == 'List':
            obj = List(*(decode(v) for v in item['value']), type=decode(item['element_type']).__class__)
        elif item['type'] == 'Dict':
            obj = Dict(type=decode(item['element_type']).__class__)
            obj.update(OrderedDict(((k, decode(v)) for k, v in item['value'].items())))
        else:
            obj = types[item['type']](*item['value'])

        if hasattr(obj, "__doc__"):
            obj.__doc__ = item.get("doc", "")

        if hasattr(obj, "__group__"):
            obj.__group__ = item.get("group", "")
        return obj

    return decode(ser).__class__


class List(list):
    """
    Overridden list to allow us to wrap functions for automatic write.
    This is required as we can't wrap/replace the builtin list functions
    """

    def __init__(self, *args, type=None, **kwargs):
        self.type = type
        self.__doc__ = ""
        self.__group__ = ""
        items = []
        if len(args) == 1 and isinstance(args[0], (list, tuple, set, )):  # todo: GeneratorType
            args = args[0]
        super(List, self).__init__(items, **kwargs)
        self._update_field(self, args)

    def append(self, elem):
        if self.type and not isinstance(elem, self.type):
            raise ValueError("%s must be of type %s" % (elem, self.type))
        super(List, self).append(elem)

    def extend(self, elems):
        if self.type and any((not isinstance(elem, self.type) for elem in elems)):
            raise ValueError("%s must all be of type %s" % (elems, self.type))
        super(List, self).extend(elems)

    def insert(self, index, obj):
        if self.type and not isinstance(obj, self.type):
            raise ValueError("%s must be of type %s" % (obj, self.type))
        super(List, self).insert(index, obj)

    def __eq__(self, other):
        if type(other).__name__ == self.__class__.__name__:
            return list(self) == list(other)

    def __deepcopy__(self, memo):
        n = List(*deepcopy(list(self), memo), type=self.type)
        n.__doc__ = self.__doc__
        n.__group__ = self.__group__
        return n

    def __or__(self, other):
        self.__doc__ = other
        return self

    def __serialise__(self, raw=False):
        def encode(val):
            if hasattr(val, '__serialise__'):
                val = _instantiated(val)
                return val.__serialise__(raw=True)
            elif type(val) is type:
                return OrderedDict(type=val.__name__, value=[])
            else:
                return OrderedDict(type=type(val).__name__, value=[val])

        obj = OrderedDict(
            type=self.__class__.__name__,
            value=[encode(v) for v in self],
            element_type=encode(self.type),
            doc=self.__doc__
        )
        if self.__group__:
            obj["group"] = self.__group__
        return obj if raw else ujson.dumps(obj)

    @staticmethod
    def _update_field(_list, conf, parent=None, ignore_errors=False):
        if conf is not None and type(conf) not in (type(_list), list, set, tuple):
            raise TypeError("conf be either a matching type or a list: %s" % type(conf))

        _list.clear()
        if conf is None:
            return
        conv = _list.type
        for item in conf:
            if not conv:
                _list.append(item)
            else:
                if isinstance(item, dict):
                    _list.append(conv(**item))
                elif isinstance(item, (list, tuple)):
                    _list.append(conv(*item))
                else:
                    try:
                        if isinstance(item, conv):
                            _list.append(item)
                        elif not ignore_errors:
                            raise ValueError("%s must be of type %s" % (item, conv))
                    except TypeError:
                        _list.append(conv(item))

    @staticmethod
    def _unwrap_value(val):
        return [maybe_unwrap_value(v) for v in val]


class Dict(OrderedDict):
    """
    Overridden dict to allow us to wrap functions for automatic write.
    Wrapping the builtins the same way as List didn't work, __setitem__
    would not fire the config writer
    """

    def __init__(self, *args, type=None):
        self.type = type
        self.__doc__ = ""
        self.__group__ = ""
        super(Dict, self).__init__(*args)
        if self.type:
            for key, value in self.items():
                if not isinstance(value, self.type):
                    raise ValueError("%s must be of type %s (key: %s)" % (value, self.type, key))

    def __setitem__(self, key, value):
        if self.type and not isinstance(value, self.type):
            raise ValueError("%s must be of type %s (key: %s)" % (value, self.type, key))
        return super(Dict, self).__setitem__(key, value)

    def __eq__(self, other):
        if type(other).__name__ == self.__class__.__name__:
            return dict(self.items()) == dict(other.items())

    def __deepcopy__(self, memo):
        n = Dict(deepcopy(OrderedDict(self.items()), memo), type=self.type)
        n.__doc__ = self.__doc__
        n.__group__ = self.__group__
        return n

    def __or__(self, other):
        self.__doc__ = other
        return self

    def __serialise__(self, raw=False):
        def encode(val):
            if hasattr(val, '__serialise__'):
                val = _instantiated(val)
                return val.__serialise__(raw=True)
            elif type(val) is type:
                return OrderedDict(type=val.__name__, value=[])
            else:
                return OrderedDict(type=type(val).__name__, value=[val])

        obj = OrderedDict(
            type=self.__class__.__name__,
            value={k: encode(v) for k, v in self.items()},
            element_type=encode(self.type),
            doc=self.__doc__
        )
        if self.__group__:
            obj["group"] = self.__group__
        return obj if raw else ujson.dumps(obj)

    @staticmethod
    def _update_field(_dict, conf, parent=None, ignore_errors=False):
        if conf is None:
            _dict.clear()
            return

        if type(conf) not in (type(_dict), dict, OrderedDict):
            raise TypeError("conf be either a matching type or a dict: %s" % type(conf))

        conv = _dict.type
        for key, value in conf.items():
            existing = _dict.get(key, None)

            if conv:
                if isinstance(value, dict):
                    _dict[key] = conv(**value)
                elif isinstance(value, (list, tuple)):
                    _dict[key] = conv(*value)
                elif isinstance(value, conv):
                    _dict[key] = value
                elif not ignore_errors:
                    raise ValueError("%s must be of type %s (key: %s)" % (value, conv, key))
            elif existing is not None:
                update_field = getattr(existing, '_update_field', None)
                if update_field:
                    update_field(existing, value, parent=_dict, ignore_errors=ignore_errors)
                else:
                    _dict[key] = value
            else:
                _dict[key] = value

        for key in list(_dict.keys()):
            if key not in conf:
                del _dict[key]

    @staticmethod
    def _unwrap_value(structure):
        return {key: maybe_unwrap_value(val) for key, val in structure.items()}


class ConfigFile:
    def __init__(self, configfile, structure, load=True, validate='auto'):
        self._configfile = Path(configfile)
        self._structure = structure
        self.validated = None
        if load:
            try:
                self.load(validate)
            except OSError as ex:
                if ex.args[0] != errno.ENOENT:
                    raise

    def load(self, validate='auto', ignore_errors=False):
        """
        Load config from pre-configured file
        :param str|bool validate: set to true to force validation, false to ignore, auto otherwise
        :return:
        """
        with self._configfile.open('r') as fh:
            data = fh.read()
            lastline = data.split('\n')[-1]
            if validate is True or (lastline.startswith('#') and 'crc' in lastline.lower()):
                if self.crc32_xfer(memoryview(data)) != 0:
                    self.validated = False
                    if validate:
                        raise ValueError("Checksum Failure")
                # Strip crc line off end
                data = data[0:-len(lastline)]
                self.validated = True
            try:
                conf = ujson.loads(data)
            except:
                print("Invalid json data could not be loaded:", data)
                raise

        Structure._update_field(self._structure, conf, ignore_errors=ignore_errors)

    def dump(self, checksum=False):
        _dict = Structure._unwrap_value(self._structure)
        # Pre-convert to json to avoid deleting file if there are errors
        _json = ujson.dumps(_dict)
        if checksum:
            _json += "\n# CRC-32/XFER: "
            _json = bytearray(_json)
            # crc = ubinascii.crc32(_json, 0x000000AF)
            crc = self.crc32_xfer(_json)

            # Why we find 0x0a (new line):
            # Because we use eol to find length of CRC,
            # if CRC itself has new line we fail to determine length of CRC
            while 0x0a in crc.to_bytes(4, 'big'):
                _json.extend(b' ')
                crc = self.crc32_xfer(_json)

            _json.extend(crc.to_bytes(4, 'big'))
        if not self._configfile.parent.exists():
            self._configfile.parent.mkdir(parents=True)
        with self._configfile.open('w') as fh:
            fh.write(_json)

    @staticmethod
    def crc32_xfer(data):
        """
        Returns the 32 bit CRC (XFER algorithm) of the provided bytes

        Compatible with CRC-32/XFER from https://crccalc.com/?method=crc32
        If the returned crc is appended to the original data and run back through
        this function the result will be 0.
        :param bytes,bytearray data: bytes to calculate crc on
        :return int: crc of input data
        """
        _poly = 0x000000AF
        crc = 0x00000000
        highbit = 1 << (32 - 1)
        mask = ((highbit - 1) << 1) | 0x1
        poly = _poly
        shift = 32 - 8
        diff8 = -shift
        if diff8 > 0:
            mask = 0xFF
            crc <<= diff8
            shift = 0
            highbit = 0x80
            poly = _poly << diff8

        for byte in data:
            crc ^= (byte << shift)
            for i in range(8):
                if crc & highbit:
                    crc = (crc << 1) ^ poly
                else:
                    crc = (crc << 1)
            crc &= mask
        if diff8 > 0:
            crc >>= diff8
        return crc


##########
# Fields #
##########


class Field(object):
    """
    Base class for fields that allows capturing of comments or'ed with the field
    """
    def __init__(self, value):
        self.value = value
        self.__doc__ = ''
        self.__group__ = ''

    def __or__(self, other):
        self.__doc__ = other
        return self

    def __getstate__(self) -> tuple:
        return self.value,

    def __setstate__(self, state: tuple):
        self.value, = state

    def __deepcopy__(self, memodict=None):
        n = self.__class__(deepcopy(self.value, memodict or {}))
        n.__doc__ = self.__doc__
        n.__group__ = self.__group__
        return n

    def __str__(self):
        return "<%s>(%s)|%s" % (self.__class__.__name__, ",".join((repr(a) for a in self.__getstate__())), self.__doc__)

    def __serialise__(self, raw=False):
        ret = OrderedDict(
            type=self.__class__.__name__,
            value=self.__getstate__(),
            doc=self.__doc__
        )
        if self.__group__:
            ret["group"] = self.__group__
        return ret if raw else ujson.dumps(ret)

    def _field_initialiser(self):
        return self.value


class TypedField(Field):
    def __init__(self, value, converter, writer=None, **kwargs):
        self.converter = converter
        self.writer = writer if writer else converter
        super(TypedField, self).__init__(value=converter(value))

        # cls = self.__class__
        # self._yaml_tag = '!' + cls.__name__
        #
        # yaml.add_constructor(self._yaml_tag, self._from_yaml)

    def __deepcopy__(self, memodict=None):
        if self.__class__ is TypedField:
            n = self.__class__(deepcopy(self.value, memodict or {}), self.converter, self.writer)
        else:
            n = self.__class__(deepcopy(self.value, memodict or {}))
        n.__doc__ = self.__doc__
        n.__group__ = self.__group__
        return n

    def _unwrap_value(self, val):
        return self.writer(val)

    # @classmethod
    # def _from_yaml(cls, loader, node):
    #     return loader.construct_yaml_object(node, cls)


class IntField(TypedField):
    def __init__(self, value):
        super(IntField, self).__init__(value, lambda v: None if v is None else int(v))


class StrField(TypedField):
    def __init__(self, value):
        super(StrField, self).__init__(value, lambda v: None if v is None else str(v))


class FloatField(TypedField):
    def __init__(self, value):
        super(FloatField, self).__init__(value, self.__check__)

    @staticmethod
    def __check__(value):
        if value is None:
            return None
        if (value * 0) != 0:  # test for nan/inf:
            return "nan"
        return float(value)


class PathField(TypedField):
    def __init__(self, value):
        super(PathField, self).__init__(value, Path)


class RangedNumber(TypedField):
    def __init__(self, value, min, max):
        self.min = min
        self.max = max
        super(RangedNumber, self).__init__(value, self.__check__)

    def __check__(self, value):
        if self.min <= value <= self.max:
            return value
        raise ValueError("%s out of range (%s - %s)" % (value, self.min, self.max))

    def update_range(self, min, max):
        self.min = min
        self.max = max

    def __deepcopy__(self, memodict=None):
        n = self.__class__(*deepcopy((self.value, self.min, self.max), memodict or {}))
        n.__doc__ = self.__doc__
        n.__group__ = self.__group__
        return n

    def __getstate__(self):
        return self.value, self.min, self.max

    def __setstate__(self, *args):
        self.value, self.min, self.max = args


class RangedFloat(RangedNumber):
    def __check__(self, value):
        try:
            return super(RangedFloat, self).__check__(float(value))
        except TypeError:
            raise ValueError("%s out of range (%s - %s)" % (value, self.min, self.max))


class RangedInt(RangedNumber):
    def __check__(self, value):
        try:
            return super(RangedInt, self).__check__(int(value))
        except TypeError:
            raise ValueError("%s out of range (%s - %s)" % (value, self.min, self.max))


class RangedInts(RangedInt):
    def __check__(self, values):
        return [super(RangedInts, self).__check__(value) for value in values]


class BoolField(TypedField):
    def __init__(self, value):
        super(BoolField, self).__init__(value, self.to_bool)

    @staticmethod
    def to_bool(val):
        if isinstance(val, str):
            val = val.lower() in ['yes', 'true']
        else:
            val = True if val else False
        return val


class Selection(Structure):
    def __init__(self, *args, **kwargs):
        super(Selection, self).__init__(*args, **kwargs)
        for key in self.__keys__:
            self.__setitem__(key, key)
            setattr(self.__class__, key, key)
        self._readonly = True


class SelectionField(TypedField):
    def __init__(self, value, allowed_values):
        """
        Enforces the value to be one of the allowed values
        :param str|property value:
        :param List[str] | Type[Selection] allowed_values: the list of allowed values
        """
        try:
            if issubclass(allowed_values, Structure):
                allowed_values = allowed_values()
        except TypeError:
            pass
        if isinstance(allowed_values, Structure):
            allowed_values = list(allowed_values.__keys__)

        self.allowed_values = allowed_values
        super(SelectionField, self).__init__(value, self.check)

    def check(self, val):
        if val in self.allowed_values:
            return val
        raise KeyError("'%s' is not an allowed value" % val)

    def __deepcopy__(self, memodict=None):
        n = self.__class__(copy(self.value), copy(self.allowed_values))
        n.__doc__ = self.__doc__
        n.__group__ = self.__group__
        return n

    def __getstate__(self):
        return self.value, self.allowed_values


class MultiSelection(SelectionField):
    def __init__(self, values, allowed_values):
        """
        Enforces the values to be in the allowed values
        :param list|tuple values: list of values which all need to be allowed
        :param List[str] | Type[Selection] allowed_values: the list of allowed values
        """
        super(MultiSelection, self).__init__(tuple(values), allowed_values)

    def check(self, vals):
        return tuple((super(MultiSelection, self).check(val) for val in vals))

class Deprecated(object):
    def __init__(self, field=None, new_fieldname=None, migrate=None):
        """
        This is used as a wrapper to denote a field as deprecated.
        When the field is read from yaml it will be run through converter to convert contents
        to new field if needed.
        This field cannot be read by the software end-use any longer
        :param Field field: Original field declaration
        :param str new_fieldname:  name of the new target field the converted output should be stored in
        :param function migrate: function/lambda to migrate value from old field to new field
        """
        if new_fieldname is not None and not isinstance(new_fieldname, str):
            raise ValueError("new_fieldname arg must be the name of the converted target field")

        self.field = field
        self.new_fieldname = new_fieldname
        self.migrate = migrate

        if field is not None:
            self.field_converter = getattr(field, 'converter', None)
            self.field_updater = getattr(field, '_update_field', None)
            self.field_initialiser = getattr(field, "_field_initialiser", lambda: deepcopy(field))

    def __or__(self, other):
        return self

    def __deepcopy__(self, memodict=None):
        n = self.__class__(*deepcopy((self.field, self.new_fieldname, self.migration), memodict or {}))
        n.__doc__ = self.__doc__
        n.__group__ = self.__group__
        return n

    def _update_field(self, previous_value, new_value, parent=None, ignore_errors=False):
        if self.new_fieldname is None:
            return

        if self.field_updater:
            value = self.field_initialiser()
            self.field_updater(value, new_value, parent=parent, ignore_errors=ignore_errors)
            new_value = value
        elif self.field_converter:
            new_value = self.field_converter(new_value)

        if self.migrate:
            new_value = self.migrate(new_value)
        if parent and self.new_fieldname:
            parent[self.new_fieldname] = new_value

    def _field_initialiser(self):
        # Deprecated fields never add a value to output
        return OMIT_VALUE

class Group(object):
    def __init__(self, group_name):
        self.group_name = group_name

    def _field_initialiser(self):
        return OMIT_VALUE

    def _fields_registered(self, fields):
        inside_group = False
        for key, field in fields.items():
            if field == self:
                inside_group = True
            elif inside_group and isinstance(field, Group):
                break
            elif inside_group and hasattr(field, "__group__"):
                setattr(field, "__group__", self.group_name)


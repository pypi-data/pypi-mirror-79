import sys

import structured_config
from structured_config import *

import utime
import unittest
from pathlib import Path


tmpdir = Path('test_structured_config_out')
if tmpdir.exists():
    def remove(entry: Path):
        if entry.is_dir():
            for _entry in entry.iterdir():
                remove(_entry)
            entry.rmdir()
        else:
            entry.unlink()
    remove(tmpdir)


ORDER_PRESERVED = True


def test_ordering():
    global ORDER_PRESERVED
    a = dict(aaa=1, bbb=2, ccc=3)
    b = dict(ccc=3, bbb=2, aaa=1)
    if list(a.keys()) == list(b.keys()):
        print("WARNING: micropython is not maintaining dict order, groups and serialise features compromised")
        ORDER_PRESERVED = False


test_ordering()


class TestStructured_config(unittest.TestCase):

    def test_nofile_structure(self):
        class Config(Structure):
            class server(Structure):
                url = 'https://www.example.com'
                username = '<user>'
                password = '<password>'

            concurrent_connections = 32

        _config = Config()

        assert _config.server.url == 'https://www.example.com'
        assert _config.concurrent_connections == 32

    def test_contamination(self):
        class Config(Structure):
            class server(Structure):
                url = 'https://www.example.com'
                username = '<user>'
                password = '<password>'

            concurrent_connections = 32

        config1 = Config()
        config2 = Config()

        assert config1.server.url == 'https://www.example.com'
        assert config1.concurrent_connections == 32

        assert config2.server.url == 'https://www.example.com'
        assert config2.concurrent_connections == 32

        config1.server.url = 'https://new.example.com'
        config1.concurrent_connections = 64

        assert config2.server.url == 'https://www.example.com', config2.server.url
        assert config2.concurrent_connections == 32, config2.concurrent_connections

        assert config1.server.url == 'https://new.example.com'
        assert config1.concurrent_connections == 64

    def test_structure(self):

        class Config(Structure):
            class server(Structure):
                url = 'https://www.example.com'
                username = '<user>'
                password = '<password>'

            concurrent_connections = 32

        conffile = tmpdir / 'test_structure.json'

        assert not conffile.exists(), '_config file should not already exist'

        _config = Config(conffile)
        _config.__save__()

        assert conffile.exists(), '_config file should exist'

        assert _config.server.url == 'https://www.example.com'
        assert _config.concurrent_connections == 32

        self.assertRaises(AttributeError, lambda: _config.missing)

    def test_structure_iter(self):
        class Config(Structure):
            concurrent_connections = 32

            def __iter__(self):
                raise ValueError("__iter__ shouldn't be called")

        conffile = tmpdir / 'test_structure_iter.json'
        _config = Config(conffile)
        _config.__save__()
        _config.__serialise__()

        assert conffile.exists(), '_config file should exist'
        assert _config.concurrent_connections == 32

        _config = Config(conffile)

    def test_equality(self):
        class Config(Structure):
            class server(Structure):
                url = 'https://www.example.com'
                username = '<user>'
                password = '<password>'

            concurrent_connections = 32

        c1 = Config()
        c2 = Config()

        assert c1 == c2,  "basic equality failed"
        c1.server.username = "new"
        assert c1 != c2, "still equal after one changed"
        c2.server.username = "new"
        assert c1 == c2, "both changed equality failed"

    def test_write(self):

        class Config(Structure):
            class server(Structure):
                url = 'https://www.example.com'
                username = '<user>'
                password = '<password>'

            concurrent_connections = 32

        conffile = tmpdir / 'test_write.json'

        assert not conffile.exists(), '_config file should not already exist'

        _config = Config(conffile)
        _config.__save__()

        assert conffile.exists(), '_config file should exist'

        with conffile.open('r') as conffile_handle:
            orig_conf = conffile_handle.read()

        _config.concurrent_connections = 64
        _config.__save__()

        with conffile.open('r') as conffile_handle:
            post_conf = conffile_handle.read()

        assert orig_conf != post_conf

        # if fmt == CONF_PYTHON:
        #     assert 'class Config' in post_conf
        #     assert 'class server' in post_conf
        # elif fmt == CONF_JSON:
        assert '"Config":' not in post_conf
        assert '"server":' in post_conf
        # else:
        #     assert '!Config' in post_conf
        #     assert '!server' in post_conf
        assert 'url' in post_conf
        assert 'https://www.example.com' in post_conf
        assert 'username' in post_conf
        assert 'password' in post_conf
        assert 'concurrent_connections' in post_conf
        assert '64' in post_conf

    def test_round_trip(self):
        class Config(Structure):
            class server(Structure):
                url = 'https://www.example.com'
                username = '<user>'
                password = '<password>'

            concurrent_connections = 32

        conffile = tmpdir / 'test_round_trip.json'

        assert not conffile.exists(), '_config file should not already exist'

        _config = Config(conffile)

        _config.concurrent_connections = 64
        _config.server.password = 'new pass'
        _config.__save__()

        _config2 = Config(conffile)

        assert _config2.concurrent_connections == 64

        assert _config2.server == _config.server, "%s != %s" % (_config2.server, _config.server)

        assert _config2.server.url == _config.server.url
        assert _config2.server.username == _config.server.username
        assert _config2.server.password == _config.server.password

    def test_extending_structure(self):

        class Config(Structure):
            class server(Structure):
                url = 'https://www.example.com'
                username = '<user>'
                password = '<password>'

            concurrent_connections = 32

        conffile = tmpdir / 'test_extending_structure.json'

        assert not conffile.exists(), '_config file should not already exist'

        _config = Config(conffile)

        _config.concurrent_connections = 64
        _config.__save__()

        class Config(Structure):
            class server(Structure):
                url = 'https://www.example.com'
                username = '<user>'
                password = '<password>'

            concurrent_connections = 32
            new_field = "test"

        _config2 = Config(conffile)

        assert _config2.concurrent_connections == 64

        assert _config2.server == _config.server

        assert _config2.server.url == _config.server.url
        assert _config2.server.username == _config.server.username
        assert _config2.server.password == _config.server.password
        _config2.new_field = "write"
        _config2.__save__()

        _config3 = Config(conffile)

        assert _config3.new_field == "write"

    def test_attrib_structure(self):

        class Elem(Structure):
            a = None
            b = None

        class Config(Structure):
            first = Elem()
            second = Elem(a=3, b=4)
            third = Elem

        conffile = tmpdir / 'test_attrib_structure.json'

        assert not conffile.exists(), '_config file should not already exist'
        _config = Config(conffile)

        assert _config.first.a == _config.third.a
        assert _config.second.b == 4
        _config.__save__()
        assert conffile.exists(), 'config file should exist'

        _config2 = Config(conffile)

        assert _config2.first.a == _config2.third.a
        assert _config2.second.b == 4

    def test_nested_write(self):

        class Config(Structure):
            class server(Structure):
                url = 'https://www.example.com'
                username = '<user>'
                password = '<password>'

            concurrent_connections = 32

        conffile = tmpdir / 'test_nested_write.json'

        assert not conffile.exists(), '_config file should not already exist'

        _config = Config(conffile)

        new_url = 'http://www.new.url'
        _config.server.url = new_url
        _config.__save__()

        _config2 = Config(conffile)

        assert _config2.server.url == new_url

    def test_list(self):

        class Elem(Structure):
            a = None
            b = None

            elems = List

        class Node(Structure):
            group = List(
                Elem(a=10, b=11),
                Elem(a=12, b=13),
                Elem(a=14, b=15),
            type=Elem)

        class Config(Structure):
            nodes = List(
                Node(),
            type=Node)

        conffile = tmpdir / 'test_list.json'

        assert not conffile.exists(), '_config file should not already exist'

        _config = Config(conffile)

        # Check the initial settings are still as expected
        assert len(_config.nodes) == 1
        assert isinstance(_config.nodes[0], Node)

        assert len(_config.nodes[0].group) == 3
        assert isinstance(_config.nodes[0].group[0], Elem)
        assert _config.nodes[0].group[0].a == 10 and _config.nodes[0].group[0].b == 11

        # Check that the conf file reloaded matches
        _config2 = Config(conffile)
        assert _config2.nodes == _config.nodes
        _config = _config2  # type: Config
        assert isinstance(_config.nodes[0], Node)
        assert isinstance(_config.nodes[0].group[0], Elem)

        # Change a value on one of the elem and check reloaded matches
        _config.nodes[0].group[0].a = 1
        _config.__save__()

        _config3 = Config(conffile)
        assert _config3.nodes[0].group[0].a == 1

        # Change elems in the list and check reloaded matches
        _config3.nodes[0].group.pop(0)
        _config3.__save__()

        _config4 = Config(conffile)
        assert len(_config4.nodes[0].group) == 2
        assert _config4.nodes[0].group[0].a == 12
        assert _config4.nodes[0].group[1].a == 14

        assert set(dir(_config4)) == {'nodes'}
        assert isinstance(repr(_config4), str)

        assert dir(_config4.nodes[0].group)
        assert isinstance(repr(_config4.nodes[0].group), str)

        assert dir(_config4.nodes[0].group[0])
        assert isinstance(repr(_config4.nodes[0].group[0]), str)

    def test_list_contruction(self):

        class Elem(Structure):
            a = None
            b = None

            elems = List

        class Node(Structure):
            group = List(
                Elem(a=10, b=11),
                Elem(a=12, b=13),
                Elem(a=14, b=15),
                type=Elem)

        class Config(Structure):
            nodes = List(
                Node(),
                type=Node)

        _config = Config(
            nodes=[
                Node(
                    group=[
                        Elem(a=3, b=2)
                    ]
                )
            ])

        assert len(_config.nodes) == 1
        assert isinstance(_config.nodes[0], Node)
        assert len(_config.nodes[0].group) == 1
        assert isinstance(_config.nodes[0].group[0], Elem)
        assert _config.nodes[0].group[0].a == 3
        assert _config.nodes[0].group[0].b == 2

    def test_list_type_enforcement(self):
        try:
            List([1], type=float)
            self.fail("Expected exception due to type mismatch not thrown")
        except ValueError as ex:
            assert str(ex) == "1 must be of type <class 'float'>", "unexpected error: %s" % ex

        lst = List(type=float)
        try:
            lst.append(1)
            self.fail("Expected exception due to type mismatch not thrown")
        except ValueError as ex:
            assert str(ex) == "1 must be of type <class 'float'>", "unexpected error: %s" % ex

        class Config(Structure):
            items = List(type=int)

        config = Config()
        try:
            config.items = ["a"]
            self.fail("Expected exception due to type mismatch not thrown")
        except ValueError as ex:
            assert str(ex) == "a must be of type <class 'int'>", "unexpected error: %s" % ex
        assert config.items == List(), "List should have been cleared. Was: %s" % config.items

        # check that errors can be ignored if the types don't match
        config._update_field(config, {"items": ["a"]}, ignore_errors=True)
        assert config.items == List(), "List should have been cleared. Was: %s" % config.items

    def test_round_trip_crc(self):
        class Config(Structure):
            class server(Structure):
                url = 'https://www.example.com'
                username = '<user>'
                password = '<password>'

            concurrent_connections = 32

        conffile = tmpdir / 'test_round_trip_crc.json'

        assert not conffile.exists(), '_config file should not already exist'

        _config = Config(conffile)

        assert _config.__validated__ is None, "should only be validated after written and read"

        _config.concurrent_connections = 64
        _config.server.password = 'new pass'
        _config.__save__(checksum=True)

        _config2 = Config(conffile)

        assert _config2.concurrent_connections == 64

        assert _config2.server == _config.server

        assert _config2.server.url == _config.server.url
        assert _config2.server.username == _config.server.username
        assert _config2.server.password == _config.server.password

        assert _config2.__validated__, "read in config should be crc validated"

    def test_crc_xfer(self):
        data = b'{"server": ' \
               b'{"username": "<user>", ' \
               b'"password": "<password>", ' \
               b'"url": "https://www.example.com"}, ' \
               b'"concurrent_connections": 64, "new_field": "write"}'

        repeats = 100
        start = utime.ticks_ms()

        for _ in range(repeats):
            crc = ConfigFile.crc32_xfer(data)

        data_w_crc = data + crc.to_bytes(4, 'big')
        for _ in range(repeats):
            crc_after = ConfigFile.crc32_xfer(data_w_crc)

        end = utime.ticks_ms()
        print("crc fn takes %0.2fms" % (float(end-start) / repeats))
        assert crc, "initial crc shouldn't be zero"
        assert crc_after == 0, "crc(data + crc) should be zero"

    def test_subclass(self):
        class Config(Structure):
            root_key = None
            concurrent_connections = 32

        class Server(Config):
            url = 'https://www.example.com'
            username = '<user>'
            password = '<password>'

        config1 = Server()
        assert {'root_key', 'concurrent_connections', 'url', 'username', 'password'} == set(config1.__keys__)

        assert config1.concurrent_connections == 32
        config1.concurrent_connections = 60
        assert config1.concurrent_connections == 60, config1.concurrent_connections

    def test_subclass_contamination(self):
        class Config(Structure):
            root_key = None
            concurrent_connections = 32

        class Server(Config):
            url = 'https://www.example.com'
            username = '<user>'
            password = '<password>'

        config1 = Server()
        config2 = Server()

        assert config1.url == 'https://www.example.com'
        assert config1.concurrent_connections == 32

        assert config2.url == 'https://www.example.com'
        assert config2.concurrent_connections == 32

        # modify config1
        config1.url = 'https://new.example.com'
        config1.concurrent_connections = 64

        # Check config2 wasn't contaminated
        assert config2.url == 'https://www.example.com', config2.url
        assert config2.concurrent_connections == 32, config2.concurrent_connections

        assert config1.url == 'https://new.example.com'
        assert config1.concurrent_connections == 64, config1.concurrent_connections

        # Test that new object from class isn't contaminated with changes from config1
        config3 = Server()
        assert config3 == config2, config3

    def test_wrong_structure(self):
        class Config(Structure):
            root_key = None
            concurrent_connections = 32

        class Server(Structure):
            url = 'https://www.example.com'
            username = '<user>'
            password = '<password>'

        conffile1 = tmpdir / 'test_wrong_structure_1.json'
        conffile2 = tmpdir / 'test_wrong_structure_2.json'

        assert not conffile1.exists(), '_config file should not already exist'
        assert not conffile2.exists(), '_config file should not already exist'

        config1 = Config(conffile1).__save__()
        config2 = Server(conffile2).__save__()

        assert conffile1.exists(), '_config file should exist'
        assert conffile2.exists(), '_config file should exist'

        with self.assertRaises(AttributeError):
            config3 = Config(conffile2)

    def test_obsolete_field(self):
        class OldServer(Structure):
            url = 'https://www.example.com'
            username = '<user>'
            password = '<password>'

        class Server(Structure):
            url = Deprecated()
            username = ''
            password = ''

        conffile = tmpdir / 'test_obsolete_field_1.json'

        assert not conffile.exists(), '_config file should not already exist'

        config = OldServer(conffile).__save__()

        # Check loading still works
        config2 = Server(conffile)

        try:
            _ = config2.url
            self.fail("Expected AttributeError exception not thrown")
        except AttributeError as ex:
            assert str(ex) == "url", str(ex)
        assert config2.username == '<user>'
        assert config2.password == '<password>'

        conffile2 = tmpdir / 'test_obsolete_field_2.json'
        assert not conffile2.exists(), '_config file should not already exist'

        Server(conffile2).__save__()
        contents = conffile2.read_text()
        assert 'url' not in contents

    def test_dict(self):

        class Elem(Structure):
            a = None
            b = None

            elems = Dict

        class Node(Structure):
            group = Dict({
                "m":Elem(a=10, b=11),
                "n":Elem(a=12, b=13),
                "o":Elem(a=14, b=15)
                }, type=Elem)

        class Config(Structure):
            nodes = Dict({"p":Node()}, type=Node)

        conffile = tmpdir / 'test_dict.json'
        print(conffile.absolute())

        assert not conffile.exists(), '_config file should not already exist'

        _config = Config(conffile)

        # Check the initial settings are still as expected
        assert len(_config.nodes) == 1
        assert isinstance(_config.nodes["p"], Node)

        assert len(_config.nodes["p"].group) == 3
        assert isinstance(_config.nodes["p"].group["m"], Elem)
        assert _config.nodes["p"].group["m"].a == 10 and _config.nodes["p"].group["m"].b == 11

        # Check that the conf file reloaded matches
        _config2 = Config(conffile)
        assert _config2.nodes == _config.nodes
        _config = _config2  # type: Config
        assert isinstance(_config.nodes["p"], Node)
        assert isinstance(_config.nodes["p"].group["m"], Elem)

        # Change a value on one of the elem and check reloaded matches
        _config.nodes["p"].group["m"].a = 1
        _config.__save__()

        _config3 = Config(conffile)
        assert _config3.nodes["p"].group["m"].a == 1

        # Change elems in the dict and check reloaded matches
        _config3.nodes["p"].group.pop("m")
        _config3.nodes["p"].group["z"] = Elem(a=15, b=21)
        _config3.__save__()

        _config4 = Config(conffile)
        assert len(_config4.nodes["p"].group) == 3
        assert _config4.nodes["p"].group["n"].a == 12
        assert _config4.nodes["p"].group["o"].a == 14
        assert _config4.nodes["p"].group["z"].a == 15

        assert set(dir(_config4)) == {'nodes'}
        assert isinstance(repr(_config4), str)

        assert dir(_config4.nodes["p"].group)
        assert isinstance(repr(_config4.nodes["p"].group), str)

        assert dir(_config4.nodes["p"].group["n"])
        assert isinstance(repr(_config4.nodes["p"].group["n"]), str)

    def test_dict_construction(self):

        class Elem(Structure):
            a = None
            b = None
            c = List(type=str)

            elems = Dict

        class Node(Structure):
            group = Dict({
                "m":Elem(a=10, b=11),
                "n":Elem(a=12, b=13),
                "o":Elem(a=14, b=15)
                }, type=Elem)

        class Config(Structure):
            nodes = Dict({"p":Node()}, type=Node)

        _config = Config(
            nodes={
                "z": Node(
                    group={
                        "x": Elem(a=3, b=2, c=["1","2","3"])
                    }
                )
            })

        assert len(_config.nodes) == 1
        assert isinstance(_config.nodes["z"], Node)
        assert len(_config.nodes["z"].group) == 1
        assert isinstance(_config.nodes["z"].group["x"], Elem)
        assert _config.nodes["z"].group["x"].a == 3
        assert _config.nodes["z"].group["x"].b == 2
        assert _config.nodes["z"].group["x"].c == List("1","2","3")

    def test_dict_type_enforcement(self):
        try:
            Dict({"a": 1}, type=float)
            self.fail("Expected exception due to type mismatch not thrown")
        except ValueError as ex:
            assert str(ex) == "1 must be of type <class 'float'> (key: a)", "unexpected error: %s" % ex

        dct = Dict(type=float)
        try:
            dct["a"] = 1
            self.fail("Expected exception due to type mismatch not thrown")
        except ValueError as ex:
            assert str(ex) == "1 must be of type <class 'float'> (key: a)", "unexpected error: %s" % ex

        class Config(Structure):
            items = Dict(type=int)

        config = Config()
        try:
            config.items["a"] = "b"
            self.fail("Expected exception due to type mismatch not thrown")
        except ValueError as ex:
            assert str(ex) == "b must be of type <class 'int'> (key: a)", "unexpected error: %s" % ex
        assert config.items == Dict(), "Dict should have been cleared. Was: %s" % config.items

        # check that errors can be ignored if the types don't match
        config._update_field(config, {"items": {"a": "b"}}, ignore_errors=True)
        assert config.items == Dict(), "Dict should have been cleared. Was: %s" % config.items

    def test_typed_fields(self):

        class Config(Structure):
            concurrent_connections = IntField(32)
            path = TypedField('12345', lambda s: "".join(reversed(s)))

        conffile1 = tmpdir / 'test_typed_fields.json'

        assert not conffile1.exists(), '_config file should not already exist'

        config1 = Config(conffile1).__save__()

        assert config1.path == '54321', config1.path

        assert '"12345"' in Path(conffile1).read_text(), Path(conffile1).read_text()

        config1.concurrent_connections = '64'

        with self.assertRaises(ValueError):
            config1.concurrent_connections = 'abc'

        assert config1.concurrent_connections == 64
        config1.__save__()

        config2 = Config(conffile1)

        assert config2.concurrent_connections == 64
        assert config2.path == '54321', config2.path

        assert dir(config2)
        assert isinstance(repr(config2.concurrent_connections), str)

    def test_selection(self):

        class NewColours(Selection):
            new_ultraviolet = 'new_ultraviolet'
            new_red = 'new_red'
            new_green = 'new_green'

        class Colours(Selection):
            ultraviolet = ''
            red = ''
            green = ''
            blue = ''
            magenta = ''
            cyan = ''
            white = ''

        class Config(Structure):
            colour1 = SelectionField('red', Colours)
            colour2 = SelectionField(Colours.blue, Colours)
            colours = MultiSelection([], Colours)
            yesno = SelectionField('yes', ['yes', 'no'])

            new_sel = SelectionField(NewColours.new_red, NewColours)

            # dep_sel = Deprecated(SelectionField('red', Colours),
            #                      new_fieldname='new_sel',
            #                      converter=lambda x: getattr(Colours, str(x)))
            #
            # dep_mul = Deprecated(MultiSelection([Colours.ultraviolet], Colours),
            #                      new_fieldname='new_sel',
            #                      converter=lambda x: getattr(Colours, str(x[0])) if x else tuple())

        conffile = tmpdir / 'test_selection.json'

        config = Config(conffile)

        assert config.colour1 == Colours.red
        assert config.colour1 == 'red'

        assert config.colour1 != 'blue'

        assert config.colour2 == Colours.blue
        assert config.colour2 == 'blue'

        with self.assertRaises(KeyError):
            config.colour2 = "none"

        assert config.yesno == 'yes'

        with self.assertRaises(KeyError):
            config.yesno = "none"

        config.colours = [Colours.red, Colours.green, 'blue']
        assert len(config.colours) == 3
        assert 'green' in config.colours
        assert Colours.blue in config.colours
        with self.assertRaises(KeyError):
            config.colours = [Colours.red, 'dead']

        with self.assertRaises((KeyError, AttributeError)):
            config.colours.append('dead')

        # Reload from file
        config = Config(conffile)

        config.colours = [Colours.red, Colours.green, 'blue']
        assert len(config.colours) == 3
        assert 'green' in config.colours
        assert Colours.blue in config.colours

    def test_doc(self):

        class Config(Structure):
            zero = Field(0)                              | "zero"
            nope = BoolField('no')                       | "should be false"
            three = SelectionField('3', ['1', '2', '3']) | "three"

        conffile = tmpdir / 'test_doc.json'
        config = Config(conffile)

        assert config.zero == 0
        assert 'zero' in config.__fdoc__('zero')

        assert 'false' in config.__fdoc__('nope')
        assert config.nope is False

        assert 'three' in config.__fdoc__('three')
        assert config.three == '3'
        config.three = '1'
        config.__save__()
        del config

        config2 = Config(conffile)

        assert config2.zero == 0
        assert 'zero' in config2.__fdoc__('zero')

        assert 'false' in config2.__fdoc__('nope')
        assert config2.nope is False

        assert 'three' in config2.__fdoc__('three')
        assert config2.three == '1'

    def test_serialise(self):

        class Colours(Selection):
            ultraviolet = ''
            red = ''
            green = ''
            blue = ''
            magenta = ''
            cyan = ''
            white = ''

        class Elem(Structure):
            a = None
            b = None

        class Node(Structure):
            a_list = List(
                Elem(a=10, b=11),
                Elem(a=12, b=13),
                Elem(a=14, b=15),
            type=Elem)

            a_dict = Dict({
                "m":Elem(a=10, b=11),
                "n":Elem(a=12, b=13),
                "o":Elem(a=14, b=15)
                }, type=Elem)

        class Config(Structure):
            nodes = List(
                Node(),
            type=Node)

            zero = Field(0)                              | "zero"
            nope = BoolField('no')                       | "should be false"
            three = SelectionField('3', ['1', '2', '3']) | "three"

            class Inner(Structure):
                concurrent_connections = IntField(32)
                rf = RangedFloat(10, 1.0, 19.5)

            colour1 = SelectionField('red', Colours)

            deadtome = Deprecated()

        conffile1 = tmpdir / 'test_serialise_1.json'
        assert not conffile1.exists(), '_config file should not already exist'
        config1 = Config(conffile1).__save__()

        with self.assertRaises(KeyError, msg="'not-a-color' is not an allowed value"):
            config1.colour1 = "not-a-color"

        ser = config1.__serialise__()
        print('\n', ser)
        Config2 = structured_config.__deserialise__(ser)
        conffile2 = tmpdir / 'test_serialise_2.json'

        config2 = Config2(conffile2).__save__()
        ser2 = config2.__serialise__()
        print('\n', config2)

        self.assertEqual(config2.__fdoc__("zero"), "zero")
        # ensure deserialised object has the same limit behaviours
        with self.assertRaises(KeyError, msg="'not-a-color' is not an allowed value"):
            config1.colour1 = "not-a-color"

        assert config1 == config2, "Objects are not the same"
        # TODO check SelectionField behaviour survives

        if not ORDER_PRESERVED:
            print("SKIPPED checking file and ser obj equality: dict order not preserved")
        else:
            assert ser == ser2, "Serialised objects are not the same"
            assert conffile1.read_bytes() == conffile2.read_bytes(), "Files are not the same"

    def test_ctor_value_type_enforcement(self):
        class Config(Structure):
            class field(Structure):
                value = "some string"
                list_field = List(type=int)
                dict_field = Dict(type=bool)

        class Field2(Structure):
            value2 = "another string"

        with self.assertRaises(TypeError, msg="conf be either a matching type or a dict: <class 'Field2'>"):
            Config(field=Field2())

        with self.assertRaises(TypeError, msg="conf be either a matching type or a dict: <class 'Field2'>") as cm:
            Config().field = Field2()

        config = Config(field={"value": "a"})
        assert config.field.value == "a", "config.field.value was %s" % config.field.value

        config = Config(field={"list_field": [1]})
        assert config.field.list_field == List([1]), "config.field.list_field was %s" % config.field.list_field

        config = Config(field={"list_field": List([1], type=int)})
        assert config.field.list_field == List([1]), "config.field.list_field was %s" % config.field.list_field

        with self.assertRaises(ValueError, msg="1 must be of type <class 'bool'> (key: key)"):
            Config(field={"dict_field": {"key": 1}})

        config = Config(field={"dict_field": {"key": True}})
        assert config.field.dict_field == Dict({"key": True}), "config.field.dict_field was %s" % config.field.dict_field

    def test_deprecated_field_update(self):
        class Config(Structure):
            new_field = IntField(1)
            old_field = Deprecated(IntField(5), "new_field", lambda data: -1 * data)
            dead_field = Deprecated()

        config = Config()

        self.assertRaises(AttributeError, lambda: config.old_field)
        assert config.new_field == 1, 'deprecated field shouldnt override initial value on new_field'

        config.dead_field = 12
        self.assertRaises(AttributeError, lambda: config.dead_field)

        config.old_field = "4"
        self.assertRaises(AttributeError, lambda: config.old_field)
        assert config.new_field == -4, 'new_field should be set with value from deprecated field'

        config.old_field = 8
        self.assertRaises(AttributeError, lambda: config.old_field)
        assert config.new_field == -8, 'new_field should be updated with value from deprecated field'

        new_config = Config(dead_field="aaa")
        self.assertRaises(AttributeError, lambda: new_config.dead_field)
        assert new_config.new_field == 1, 'new_field should not be affected'

        new_config = Config(old_field=5)
        assert new_config.new_field == -5, 'new_field was %s after direct update from old_field'%new_config.new_field

        new_config = Config(new_field=10)
        assert new_config.new_field == 10, 'new_field was %s after direct update from new_field'%new_config.new_field

        new_config = Config(old_field=5, new_field=10)
        assert new_config.new_field == -5, 'new_field was %s after direct update with both fields'%new_config.new_field

        new_config = Config(new_field=10, old_field=5)
        assert new_config.new_field == -5, 'new_field was %s after direct update with both fields'%new_config.new_field

    def test_deprecated_field_collections(self):
        class Config(Structure):
            new_field = List(1, type=int)
            old_field = Deprecated(List(type=int), "new_field", lambda data: [-1 * v for v in data])

        config = Config()
        self.assertRaises(AttributeError, lambda: config.old_field)
        assert config.new_field == List(1), 'deprecated field shouldnt override initial value on new_field'

        config.old_field = [4]
        self.assertRaises(AttributeError, lambda: config.old_field)
        assert config.new_field == List(-4), 'new_field should be set with value from deprecated field: %s' % config.new_field

        config.old_field = [4, -10]
        self.assertRaises(AttributeError, lambda: config.old_field)
        assert config.new_field == List(-4, 10), 'new_field should be set with value from deprecated field: %s' % config.new_field

        new_config = Config(old_field=[5])
        assert new_config.new_field == List(-5), 'new_field was %s after direct update from old_field'%new_config.new_field

        new_config = Config(new_field=[10])
        assert new_config.new_field == List(10), 'new_field was %s after direct update from new_field'%new_config.new_field

        new_config = Config(old_field=[5], new_field=[10])
        assert new_config.new_field == List(-5), 'new_field was %s after direct update with both fields'%new_config.new_field

        new_config = Config(new_field=[10], old_field=[5])
        assert new_config.new_field == List(-5), 'new_field was %s after direct update with both fields'%new_config.new_field

        new_config.new_field = None
        assert new_config.new_field == List(), 'new_field was %s after direct update with both fields'%new_config.new_field

    def test_deprecated_field_read(self):
        def conv(data):
            return -1 * data if data is not None else None

        def conv_list(data):
            return [-1 * v for v in data]

        def conv_dict(data):
            return { k:-1 * v for k, v in data.items() }

        class ConfigOnDisk(Structure):
            old_field = IntField(5)
            old_list = List(1,2,3,type=int)
            old_dict = Dict({"a": 1, "b": 2},type=int)

        class NewConfig(Structure):
            new_field = IntField(91)
            old_field = Deprecated(IntField(95), "new_field", conv)

            new_list = List(4,5,6,type=int)
            old_list = Deprecated(List(1,2,3,type=int), "new_list", conv_list)

            new_dict = Dict({"c": 3, "d": 4},type=int)
            old_dict = Deprecated(Dict({"a": 5, "b": 6},type=int), "new_dict", conv_dict)

        class NewConfig2(Structure): # same as NewConfig but with field order reversed
            old_field = Deprecated(IntField(95), "new_field", conv)
            new_field = IntField(91)

            old_list = Deprecated(List(1,2,3,type=int), "new_list", conv_list)
            new_list = List(7,8,9,type=int)

            old_dict = Deprecated(Dict({"a": 5, "b": 6},type=int), "new_dict", conv_dict)
            new_dict = Dict({"c": 3, "d": 4},type=int)

        conffile = tmpdir / 'test_deprecated_field_read.json'

        ConfigOnDisk(conffile).__save__()
        print(conffile.read_text())

        reloaded = NewConfig(conffile)
        assert reloaded.new_field == -5, 'new_field was %s' % reloaded.new_field
        self.assertRaises(AttributeError, lambda: reloaded.old_field)

        assert reloaded.new_list == List(-1,-2,-3), 'new_list was %s' % reloaded.new_list
        self.assertRaises(AttributeError, lambda: reloaded.old_list)

        assert reloaded.new_dict == Dict({"a": -1, "b": -2}), 'new_dict was %s' % reloaded.new_dict
        self.assertRaises(AttributeError, lambda: reloaded.old_dict)

        reloaded = NewConfig2(conffile)
        assert reloaded.new_field == -5, 'new_field was %s' % reloaded.new_field
        self.assertRaises(AttributeError, lambda: reloaded.old_field)

        assert reloaded.new_list == List(-1,-2,-3), 'new_list was %s' % reloaded.new_list
        self.assertRaises(AttributeError, lambda: reloaded.old_list)

        assert reloaded.new_dict == Dict({"a": -1, "b": -2}), 'new_dict was %s' % reloaded.new_dict
        self.assertRaises(AttributeError, lambda: reloaded.old_dict)

        conffile.unlink()

        new_config = NewConfig(conffile)
        new_config.new_field = 10
        assert new_config.new_field == 10, 'new_field was %s' % new_config.new_field

        new_config.new_list = [20, 21, 22]
        assert new_config.new_list == List(20, 21, 22), 'new_list was %s' % new_config.new_list

        new_config.new_dict = {"c": 1, "d": 2}
        assert new_config.new_dict == Dict({"c": 1, "d": 2}), 'new_dict was %s' % new_config.new_dict

        new_config.__save__()

        reloaded = NewConfig2(conffile)
        assert reloaded.new_field == 10, 'new_field was %s after reload' % reloaded.new_field
        assert reloaded.new_list == List(20, 21, 22), 'new_list was %s' % reloaded.new_list
        assert reloaded.new_dict == Dict({"c": 1, "d": 2}), 'new_dict was %s' % reloaded.new_dict

    def test_deprecated_field_nested_with_migrations(self):
        class Config(Structure):
            new_field = StrField("c")
            teenage_field = Deprecated(StrField("b"), "new_field", lambda data: data + "|b")
            old_field = Deprecated(StrField("a"), "teenage_field", lambda data: data + "|a")

        config = Config()
        assert config.new_field == 'c', 'deprecated field shouldnt override initial value: %s' % config.new_field

        config.old_field = "x"
        assert config.new_field == 'x|a|b', 'some migrations missing: %s' % config.new_field

        config.teenage_field = "x"
        assert config.new_field == 'x|b', 'some migrations missing: %s' % config.new_field

        config.new_field = "x"
        assert config.new_field == 'x', 'unexpected migrations: %s' % config.new_field

    def test_groups(self):
        if not ORDER_PRESERVED:
            print("SKIPPED: dict order not preserved which breaks groups")
            return

        class Config(Structure):
            group_1 = Group("group 1")
            string_field = StrField("a")
            list_field = List()

            group_2 = Group("group 2")
            dict_field = Dict()
            class subtree(Structure):
                url = ""

        config = Config()
        self.assertEqual(config.__fgroup__("string_field"), "group 1")
        self.assertEqual(config.__fgroup__("list_field"), "group 1")
        self.assertEqual(config.__fgroup__("dict_field"), "group 2")
        self.assertEqual(config.__fgroup__("subtree"), "group 2")

        ser = config.__serialise__()
        Config2 = structured_config.__deserialise__(ser)
        config2 = Config2()
        self.assertEqual(config2.__fgroup__("string_field"), "group 1")
        self.assertEqual(config2.__fgroup__("list_field"), "group 1")
        self.assertEqual(config2.__fgroup__("dict_field"), "group 2")
        self.assertEqual(config2.__fgroup__("subtree"), "group 2")

    def test_serialise_list(self):
        class Config(Structure):
            interval = (
                List([1.0, 1.5, 2.0], type=float) | "The interval between reads"
            )

        config = Config()
        ser = config.__serialise__()
        print(ser)
        Config2 = structured_config.__deserialise__(ser)
        config2 = Config2()

        assert config2 == config


if __name__ == '__main__':
    unittest.main()

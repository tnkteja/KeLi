import pytest
from tests.setup_transaction_tests import chain as s, tester as t, ethereum_utils as u, check_gas, \
    get_contract_with_gas_estimation, get_contract


def test_test_bytes():
    test_bytes = """
def foo(x: bytes <= 100) -> bytes <= 100:
    return x
    """

    c = get_contract(test_bytes)
    moo_result = c.foo(b'cow')
    assert moo_result == b'cow'

    print('Passed basic bytes test')

    assert c.foo(b'\x35' * 100) == b'\x35' * 100

    print('Passed max-length bytes test')

    try:
        c.foo(b'\x35' * 101)
        assert False
    except:
        pass

    print('Passed input-too-long test')


def test_test_bytes2():
    test_bytes2 = """
def foo(x: bytes <= 100) -> bytes <= 100:
    y = x
    return y
    """

    c = get_contract(test_bytes2)
    assert c.foo(b'cow') == b'cow'
    assert c.foo(b'') == b''
    assert c.foo(b'\x35' * 63) == b'\x35' * 63
    assert c.foo(b'\x35' * 64) == b'\x35' * 64
    assert c.foo(b'\x35' * 65) == b'\x35' * 65

    print('Passed string copying test')


def test_test_bytes3():
    test_bytes3 = """
x: num
maa: bytes <= 60
y: num

def __init__():
    self.x = 27
    self.y = 37

def set_maa(inp: bytes <= 60):
    self.maa = inp

def set_maa2(inp: bytes <= 60):
    ay = inp
    self.maa = ay

def get_maa() -> bytes <= 60:
    return self.maa

def get_maa2() -> bytes <= 60:
    ay = self.maa
    return ay

def get_xy() -> num:
    return self.x * self.y
    """

    c = get_contract(test_bytes3)
    c.set_maa(b"pig")
    assert c.get_maa() == b"pig"
    assert c.get_maa2() == b"pig"
    c.set_maa2(b"")
    assert c.get_maa() == b""
    assert c.get_maa2() == b""
    c.set_maa(b"\x44" * 60)
    assert c.get_maa() == b"\x44" * 60
    assert c.get_maa2() == b"\x44" * 60
    c.set_maa2(b"mongoose")
    assert c.get_maa() == b"mongoose"
    assert c.get_xy() == 999

    print('Passed advanced string copying test')


def test_test_bytes4():
    test_bytes4 = """
a: bytes <= 60
def foo(inp: bytes <= 60) -> bytes <= 60:
    self.a = inp
    self.a = None
    return self.a

def bar(inp: bytes <= 60) -> bytes <= 60:
    b = inp
    b = None
    return b
    """

    c = get_contract(test_bytes4)
    assert c.foo() == b"", c.foo()
    assert c.bar() == b""

    print('Passed string deleting test')


def test_test_bytes5():
    test_bytes5 = """
g: {a: bytes <= 50, b: bytes <= 50}

def foo(inp1: bytes <= 40, inp2: bytes <= 45):
    self.g = {a: inp1, b: inp2}

def check1() -> bytes <= 50:
    return self.g.a

def check2() -> bytes <= 50:
    return self.g.b

def bar(inp1: bytes <= 40, inp2: bytes <= 45) -> bytes <= 50:
    h = {a: inp1, b: inp2}
    return h.a

def bat(inp1: bytes <= 40, inp2: bytes <= 45) -> bytes <= 50:
    h = {a: inp1, b: inp2}
    return h.b

def quz(inp1: bytes <= 40, inp2: bytes <= 45):
    h = {a: inp1, b: inp2}
    self.g = h
    """

    c = get_contract(test_bytes5)
    c.foo(b"cow", b"horse")
    assert c.check1() == b"cow"
    assert c.check2() == b"horse"
    assert c.bar(b"pig", b"moose") == b"pig"
    assert c.bat(b"pig", b"moose") == b"moose"
    c.quz(b"badminton", b"fluffysheep")
    assert c.check1() == b"badminton"
    assert c.check2() == b"fluffysheep"

    print('Passed string struct test')


def test_bytes_to_num_code():
    bytes_to_num_code = """
def foo(x: bytes <= 32) -> num:
    return bytes_to_num(x)
    """

    c = get_contract(bytes_to_num_code)
    assert c.foo(b"") == 0
    try:
        c.foo(b"\x00")
        success = True
    except:
        success = False
    assert not success
    assert c.foo(b"\x01") == 1
    try:
        c.foo(b"\x00\x01")
        success = True
    except:
        success = False
    assert not success
    assert c.foo(b"\x01\x00") == 256
    assert c.foo(b"\x01\x00\x00\x00\x01") == 4294967297
    assert c.foo(b"\xff" * 32) == -1
    try:
        c.foo(b"\x80" + b"\xff" * 31)
        success = True
    except:
        success = False
    try:
        c.foo(b"\x01" * 33)
        success = True
    except:
        success = False
    print('Passed bytes_to_num tests')

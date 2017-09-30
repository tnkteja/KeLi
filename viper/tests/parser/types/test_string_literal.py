import pytest
from tests.setup_transaction_tests import chain as s, tester as t, ethereum_utils as u, check_gas, \
    get_contract_with_gas_estimation, get_contract


def test_string_literal_code():
    string_literal_code = """
def foo() -> bytes <= 5:
    return "horse"

def bar() -> bytes <= 10:
    return concat("b", "a", "d", "m", "i", "", "nton")

def baz() -> bytes <= 40:
    return concat("0123456789012345678901234567890", "12")

def baz2() -> bytes <= 40:
    return concat("01234567890123456789012345678901", "12")

def baz3() -> bytes <= 40:
    return concat("0123456789012345678901234567890", "1")

def baz4() -> bytes <= 100:
    return concat("01234567890123456789012345678901234567890123456789",
                  "01234567890123456789012345678901234567890123456789")
    """

    c = get_contract(string_literal_code)
    assert c.foo() == b"horse"
    assert c.bar() == b"badminton"
    assert c.baz() == b"012345678901234567890123456789012"
    assert c.baz2() == b"0123456789012345678901234567890112"
    assert c.baz3() == b"01234567890123456789012345678901"
    assert c.baz4() == b"0123456789" * 10

    print("Passed string literal test")


def test_string_literal_splicing_fuzz():
    for i in range(95, 96, 97):
        kode = """
moo: bytes <= 100

def foo(s: num, L: num) -> bytes <= 100:
        x = 27
        r = slice("%s", start=s, len=L)
        y = 37
        if x * y == 999:
            return r

def bar(s: num, L: num) -> bytes <= 100:
        self.moo = "%s"
        x = 27
        r = slice(self.moo, start=s, len=L)
        y = 37
        if x * y == 999:
            return r

def baz(s: num, L: num) -> bytes <= 100:
        x = 27
        self.moo = slice("%s", start=s, len=L)
        y = 37
        if x * y == 999:
            return self.moo
        """ % (("c" * i), ("c" * i), ("c" * i))
        c = get_contract(kode)
        for e in range(63, 64, 65):
            for _s in range(31, 32, 33):
                o1 = c.foo(_s, e - _s)
                o2 = c.bar(_s, e - _s)
                o3 = c.baz(_s, e - _s)
                assert o1 == o2 == o3 == b"c" * (e - _s), (i, _s, e - _s, o1, o2, o3)

    print("Passed string literal splicing fuzz-test")

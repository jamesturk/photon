from csdl.enum import CEnum, CEnumSymbol

class TestEnum(CEnum):
    FIRST = 0
    SPECIAL = 2, 'a special case'
    BIG = 9001

def test_enumsymbol():
    assert isinstance(TestEnum.FIRST, int)
    assert TestEnum.FIRST == 0
    assert TestEnum.SPECIAL == 2
    assert TestEnum.FIRST.name == 'FIRST'
    assert TestEnum.SPECIAL.name == 'SPECIAL'
    assert TestEnum.FIRST.description == 'FIRST'
    assert TestEnum.SPECIAL.description == 'a special case'
    assert repr(TestEnum.FIRST) == '<FIRST>'
    assert repr(TestEnum.SPECIAL) == '<SPECIAL>'

def test_cenum():
    assert len(TestEnum.values()) == 3
    big_hopefully = TestEnum.from_int(9001)
    assert isinstance(big_hopefully, CEnumSymbol)
    assert big_hopefully.name == 'BIG'

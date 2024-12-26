import pytest

def test_eq_or_neq():
    assert 3 == 3

def test_is_instance():
    assert isinstance("Hi", str)

def test_boolean():
    validated = True
    assert validated is True

def test_assert_type():
    assert type("Hi" is str)

def test_gt_lt():
    assert 7>3
    assert 4<7

def test_list():
    num_list = [1,2,3,4,5]
    assert 1 in num_list
    assert 7 not in num_list
    assert all(num_list)

class Student:
    def __init__(self, first_name:str, last_name:str, major:str, years:int):
        self.first_name=first_name
        self.last_name=last_name
        self.major=major
        self.years=years
@pytest.fixture
def default_employee():
    return Student('John', 'Doe', 'CS', 3)

def test_person_initialization(default_employee):
    assert default_employee.first_name == 'John', 'First name should be John'
    assert default_employee.last_name == 'Doe'
    assert default_employee.major == 'CS'
    assert default_employee.years == 3
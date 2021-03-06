import pytest
from utils import *


def test_valid_date():
    etherscan_date_format_1 = "2022-06-09 1:14:52"
    etherscan_date_format_2 = "Jun-09-2022 01:14:52 AM +UTC"
    invalid_date_format = "2022-06-09"
    assert isinstance(valid_date(etherscan_date_format_1), datetime.datetime)
    assert isinstance(valid_date(etherscan_date_format_2), datetime.datetime)
    with pytest.raises(ValueError):
        valid_date(invalid_date_format)


def test_address_equals():
    address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
    assert address_equals(None, None) is False
    assert address_equals(address, None) is False
    assert address_equals(None, address) is False
    assert address_equals(address, address) is True
    assert address_equals(address, address.lower()) is True
    assert address_equals(address, address.upper()) is True

import datetime


def valid_date(d):
    """Parse dates from the common formats used in Etherscan, assume UTC"""
    for date_format in ("%Y-%m-%d %H:%M:%S", "%b-%d-%Y %I:%M:%S %p +%Z"):
        try:
            return datetime.datetime.strptime(d, date_format).replace(
                tzinfo=datetime.timezone.utc
            )
        except ValueError:
            pass
    raise ValueError("Invalid date format")


def address_equals(a, b):
    """Case insensitive string comparison"""
    if not a or not b:
        return False
    return a.casefold() == b.casefold()


def pick(dictionary, keys):
    """Return a subset of the supplied dictionary containing only the specified keys. If the key doesn't exist in the
    supplied dictionary, include it in the output dict with a value of None"""
    return dict((k, dictionary.get(k, None)) for k in keys)

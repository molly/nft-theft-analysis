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

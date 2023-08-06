from collections.abc import Iterable
import datetime
import enum

import pytz

from pyhafas import HafasClient
from pyhafas.profile import DBProfile

client = HafasClient(DBProfile(), debug=True)


def todict(obj):
    """
    Recursively convert a Python object graph to sequences (lists)
    and mappings (dicts) of primitives (bool, int, float, string, ...)
    """
    if isinstance(obj, str):
        return obj
    elif isinstance(obj, enum.Enum):
        return str(obj)
    elif isinstance(obj, dict):
        return dict((key, todict(val)) for key, val in obj.items())
    elif isinstance(obj, Iterable):
        return [todict(val) for val in obj]
    elif hasattr(obj, '__slots__'):
        return todict(dict((name, getattr(obj, name)) for name in getattr(obj, '__slots__')))
    elif hasattr(obj, '__dict__'):
        return todict(vars(obj))
    return obj


# print(todict(client.arrivals(
#     station='8005556',
#     date=datetime.datetime.now(),
#     max_trips=5,
#     direction='8002753'
# )))
# #
# print(client.arrivals(
#     station='8005556',
#     date=datetime.datetime.now(),
#     max_trips=5
# ))
# print(client.journey('¶HKI¶T$A=1@O=Berlin Jungfernheide@L=8011167@a=128@$A=1@O=Berlin Hbf (tief)@L=8098160@a=128@$202002101544$202002101549$RB 18521$$1$§T$A=1@O=Berlin Hbf (tief)@L=8098160@a=128@$A=1@O=München Hbf@L=8000261@a=128@$202002101605$202002102002$ICE 1007$$1$'))
print(todict(client.journeys(
        destination="8002753",
        origin="8005556",
        date=datetime.datetime.now(),
        min_change_time=0,
        max_changes=-1,
        max_journeys=2,
    )))
# print(client.locations("Au(Sieg)"))
#
# print(client.trip("1|1372374|3|80|9062020"))
#
# print('='*20)
# vsn = HafasClient(VSNProfile())
# print(vsn.departures(
#     station='9034033',
#     date=datetime.datetime.now(),
#     max_journeys=5
# ))

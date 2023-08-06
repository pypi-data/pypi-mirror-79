import datetime
import os

from pyhafas.profile.vsn import VSNProfile
from pyhafas.types.fptf import (Journey, Leg, Mode, Station, StationBoardLeg,
                                Stopover)

from tests.types import PyTestHafasResponse


def test_vsn_journeys_parsing():
    directory = os.path.dirname(os.path.realpath(__file__))
    raw_hafas_json_file = open(directory + "/journeys_raw.json", "r")
    hafas_response = PyTestHafasResponse(raw_hafas_json_file.read())
    raw_hafas_json_file.close()
    correct_journeys = [
        Journey(
            id='¶HKI¶T$A=1@O=Göttingen@L=8000128@a=128@$A=1@O=Lenglern@L=8003644@a=128@$202008090710$202008090719$    RB85$$1$$$',
            date=datetime.date(
                2020,
                8,
                9),
            duration=datetime.timedelta(
                seconds=540),
            legs=[
                Leg(
                    id='1|147532|0|80|9082020',
                    origin=Station(
                        id='8000128',
                        name='Göttingen',
                        latitude=51.536812,
                        longitude=9.926069
                    ),
                    destination=Station(
                        id='8003644',
                        name='Lenglern',
                        latitude=51.588428,
                        longitude=9.871199
                    ),
                    departure=VSNProfile().timezone.localize(datetime.datetime(
                        2020,
                        8,
                        9,
                        7,
                        10
                    )),
                    arrival=VSNProfile().timezone.localize(datetime.datetime(
                        2020,
                        8,
                        9,
                        7,
                        19
                    )),
                    mode=Mode.TRAIN,
                    name='RB85',
                    cancelled=False,
                    distance=None,
                    departure_delay=datetime.timedelta(seconds=0),
                    departure_platform='4',
                    arrival_delay=datetime.timedelta(seconds=60),
                    arrival_platform='1',
                    stopovers=[
                        Stopover(
                            stop=Station(
                                id='8000128',
                                name='Göttingen',
                                latitude=51.536812,
                                longitude=9.926069
                            ),
                            cancelled=False,
                            arrival=None,
                            arrival_delay=None,
                            arrival_platform=None,
                            departure=VSNProfile().timezone.localize(datetime.datetime(
                                2020,
                                8,
                                9,
                                7,
                                10)),
                            departure_delay=datetime.timedelta(seconds=0),
                            departure_platform=None
                        ),
                        Stopover(
                            stop=Station(
                                id='8003644',
                                name='Lenglern',
                                latitude=51.588428,
                                longitude=9.871199
                            ),
                            cancelled=False,
                            arrival=VSNProfile().timezone.localize(datetime.datetime(
                                2020,
                                8,
                                9,
                                7,
                                19)),
                            arrival_delay=datetime.timedelta(seconds=60),
                            arrival_platform=None,
                            departure=None,
                            departure_delay=None,
                            departure_platform=None
                        )
                    ]
                )
            ]
        )
    ]
    assert VSNProfile().parse_journeys_request(hafas_response) == correct_journeys

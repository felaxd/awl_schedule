from datetime import time

DAY_START_HOUR = time(hour=8, minute=0, second=0)

AMOUNT_OF_TIME_BLOCK_PER_DAY = 16
# te dwie wartości są ze sobą powiązane - pamiętaj żey zmiany uwzględniać w obu!
HOUR_BLOCK_START_TIMESPANS = {
    1: (time(hour=8, minute=0, second=0), time(hour=8, minute=45, second=0)),
    2: (time(hour=8, minute=45, second=0), time(hour=9, minute=30, second=0)),
    3: (time(hour=9, minute=40, second=0), time(hour=10, minute=25, second=0)),
    4: (time(hour=10, minute=25, second=0), time(hour=11, minute=10, second=0)),
    5: (time(hour=11, minute=30, second=0), time(hour=12, minute=15, second=0)),
    6: (time(hour=12, minute=15, second=0), time(hour=13, minute=0, second=0)),
    7: (time(hour=13, minute=10, second=0), time(hour=13, minute=55, second=0)),
    8: (time(hour=13, minute=55, second=0), time(hour=14, minute=40, second=0)),
    9: (time(hour=14, minute=45, second=0), time(hour=15, minute=30, second=0)),
    10: (time(hour=15, minute=30, second=0), time(hour=16, minute=15, second=0)),
    11: (time(hour=16, minute=20, second=0), time(hour=17, minute=5, second=0)),
    12: (time(hour=17, minute=5, second=0), time(hour=17, minute=50, second=0)),
    13: (time(hour=17, minute=55, second=0), time(hour=18, minute=40, second=0)),
    14: (time(hour=18, minute=40, second=0), time(hour=19, minute=25, second=0)),
    15: (time(hour=19, minute=30, second=0), time(hour=20, minute=15, second=0)),
    16: (time(hour=20, minute=15, second=0), time(hour=21, minute=0, second=0)),
}

DEFAULT_MODULE_TYPE = "wykład"
MODULE_TYPES_TUPLE = [
    ("-Ć", "ćwiczenia"),
    ("-L", "laboratorium"),
    ("-F", "fakultet"),
]

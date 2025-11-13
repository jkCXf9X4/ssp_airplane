

from pyssp_standard.ssd import SSD
from pathlib import Path

with SSD(Path("./build/structure/aircraft.ssd")) as file:
        file.__check_compliance__()
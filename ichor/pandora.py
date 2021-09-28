from ichor.globals import GLOBALS
from pathlib import Path
from ichor.machine import MACHINE, Machine
from ichor.files import OptionalFile


class CannotFindPandora(Exception):
    pass


def PANDORA_LOCATION() -> Path:
    pandora_location = OptionalFile

    if GLOBALS.PANDORA_LOCATION.exists():
        if GLOBALS.PANDORA_LOCATION.exists():
            if GLOBALS.PANDORA_LOCATION.is_dir():
                if (GLOBALS.PANDORA_LOCATION / 'pandora.py').exists():
                    pandora_location = GLOBALS.PANDORA_LOCATION / 'pandora.py'
            else:
                pandora_location = GLOBALS.PANDORA_LOCATION
    elif MACHINE is Machine.ffluxlab:
        pandora_location = Path('/shared/pandora/pandora.py')
    elif MACHINE is Machine.csf3:
        pandora_location = Path('/mnt/pp01-home01/shared/pandora/pandora.py')
    else:
        pass
        # implement download for pandora

    if not pandora_location.exists():
        raise CannotFindPandora(f"Cannot find pandora location from: {pandora_location}")

    return pandora_location




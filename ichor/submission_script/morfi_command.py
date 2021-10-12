from pathlib import Path
from typing import List, Optional

from ichor.common.functools import classproperty
from ichor.globals import GLOBALS
from ichor.modules import Modules
from ichor.submission_script.aimall_command import AIMAllCommand
from ichor.submission_script.command_line import CommandLine
from ichor.submission_script.pandora_command import PandoraMorfiCommand


class NoInputs(Exception):
    pass


class MorfiCommand(CommandLine):
    def __init__(
        self,
        morfi_input: Path,
        aimall_wfn: Optional[Path] = None,
        atoms: Optional[List[str]] = None,
    ):
        self.pandora_command = PandoraMorfiCommand(morfi_input)
        self.aimall_command = (
            AIMAllCommand(aimall_wfn, atoms=atoms)
            if aimall_wfn is not None
            else None
        )

    @classproperty
    def modules(self) -> Modules:
        return PandoraMorfiCommand.modules + AIMAllCommand.modules

    @property
    def ncores(self):
        return GLOBALS.MORFI_NCORES

    @property
    def data(self) -> List[str]:
        data = self.pandora_command.data
        if self.aimall_command is not None:
            data += self.aimall_command.data
        return data

    def command(self) -> str:
        return ""

    def repr(self, variables: List[str]) -> str:
        repr = self.pandora_command.repr(
            variables[: self.pandora_command.ndata]
        )
        if self.aimall_command is not None:
            repr += "\n"
            repr += self.aimall_command.repr(
                variables[self.pandora_command.ndata :]
            )
        return repr
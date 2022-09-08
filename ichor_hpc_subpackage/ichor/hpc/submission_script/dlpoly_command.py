from pathlib import Path
from typing import List
from ichor.core.common.functools import classproperty
from ichor.hpc.modules import DlpolyModules, Modules
from ichor.hpc.submission_script.command_line import CommandLine


class DlpolyCommand(CommandLine):
    """Class used to construct a Dlpoly job. Jobs are submitted using the `SubmissionScript` class.

    :param dlpoly_directory: Path to where the working directory for dlpoly.
    """

    def __init__(self, dlpoly_program_path: Path, dlpoly_directory: Path , ncores: int = 1):
        
        self.dlpoly_program_path = dlpoly_program_path
        self.dlpoly_directory = dlpoly_directory
        self.ncores = ncores

    @property
    def data(self) -> List[str]:
        return [str(self.dlpoly_directory.absolute())]

    @classproperty
    def modules(self) -> Modules:
        """No modules need to be loaded for DL POLY. DL POLY needs to be compiled before it can be used with ICHOR."""
        return ""

    @property
    def command(self) -> str:
        """Return the command word that is used to run DL POLY. In this case, the path to the DL POLY
        executable is returned."""
        return str(self.dlpoly_program_path.absolute())

    def repr(self, variables: List[str]) -> str:
        """Return a string that is used to construct DL POLY job files."""
        cmd = f"pushd {variables[0]}\n"
        cmd += f"{self.command} &> Energies\n"
        cmd += "popd\n"
        return cmd

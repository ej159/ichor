"""
Global variables are the backbone of ichor and are used throughout
Mutable global variables are tricky things and should be used with caution, the global variables
defined in Globals are carefully maintained by a series of parsers, formatters and checkers to try
and make sure that the global variable is always valid.

|Global Variable|Type|Default Value|Description|Notes|
|---------------|----|-------------|-----------|-----|
SYSTEM_NAME                     | str             | SYSTEM            | Name of the current system                                                                 |
ALF_REFERENCE_FILE              | Path            | None, set automatically if not specified | Path to file containing atom hash and alf. Can contain data for multiple systems.                                          | gjf or xyz                                                                                      # todo: convert to Path
ATOM_REFERENCE_FILE             | Path            | None, set automatically if not specified | Path to a .xyz, .gjf, or PointsDirecotry which contains geometry for current system|
ALF                             | List[List[int]] | []                | ALF used for ichor containing atomic indices                                               | 1-index
ATOMS                           | Atoms           | None              | Instance of Atoms from ALF_REFERENCE_FILE                                                  |
CWD                             | Path            | os.getcwd()       | Current working directory                                                                  |
N_ITERATIONS                    | int             | 1                 | Number of iterations to run adaptive sampling for                                          |
POINTS_PER_ITERATION            | int             | 1                 | Number of points to add to training set per iteration                                      |
OPTIMISE_PROPERTY               | str             | iqa               | Atomic property to optimise in adaptive sampling                                           |
OPTIMISE_ATOM                   | str             | all               | Atom to optimise in adaptive sampling                                                      | Can be all or a specific atom
ACTIVE_LEARNING_METHOD          | str             | epe               | Active learning method to use                                                              | Currently only epe is implemented
NORMALISE                       | bool            | False             | Whether to normalise data before running through ferebus                                   | No longer implemented
STANDARDISE                     | bool            | False             | Whether to standardise data before running through ferebus                                 | No longer implemented
METHOD                          | str             | B3LYP             | Quantum mechanics method to use in Gaussian calculation                                    |
BASIS_SET                       | str             | 6-31+g(d,p)       | Basis set to use in Gaussian calculation                                                   |
KEYWORDS                        | List[str]       | []                | Keywords used to run Gaussian                                                              | 
ENCOMP                          | int             | 3                 | Encomp setting to use for AIMAll                                                           | Can be 3 or 4
BOAQ                            | str             | gs20              | Boaq setting used for AIMAll                                                               |
IASMESH                         | str             | fine              | Iasmesh setting used for AIMAll                                                            |
TRAINING_POINTS                 | int             | 500               | Number of training points to initialise training set with                                  | Not used by min_max or min_max_mean
SAMPLE_POINTS                   | int             | 9000              | Number of sample points to initialise sample pool with                                     |
VALIDATION_POINTS               | int             | 500               | Number of validation points to initialise validation set with                              |
TRAINING_SET_METHOD             | List[str]       | [min_max_mean]    | Methods to initialise training set                                                         | Ran in order of the list                                                                        # todo: implement parser for reading from config
SAMPLE_POOL_METHOD              | List[str]       | [random]          | Methods to initialise sample pool                                                          | Ran in order of the list                                                                        # todo: implement parser for reading from config
VALIDATION_SET_METHOD           | List[str]       | [random]          | Methods to initialise validation set                                                       | Ran in order of the list                                                                        # todo: implement parser for reading from config
KERNEL                          | str             | rbf-cyclic        | Kernel to use in ferebus                                                                   | Can only use rbf-cyclic currently
FEREBUS_TYPE                    | str             | executable        | Tells ichor to run FEREBUS or FEREBUS.py                                                   | Currently executable implemented only                                                           # todo: implement python variant and convert to enum
FEREBUS_VERSION                 | Version         | 7.0               | Current ferebus version                                                                    | Older versions use different training set and config files                                      # todo: reimplement older style for v3
FEREBUS_LOCATION                | Path            | PROGRAMS/FEREBUS  | Path to ferebus executable                                                                 |
GAUSSIAN_MEMORY_LIMIT           | str             | 1GB               | Memory limit for runnning Gaussian
GAUSSIAN_NCORES             | int             | 2                 | Number of cores to run Gaussian                                                            |
AIMALL_NCORES               | int             | 2                 | Number of cores to run AIMAll                                                              |
FEREBUS_NCORES              | int             | 4                 | Number of cores to run FEREBUS                                                             |
DLPOLY_NCORES               | int             | 1                 | Number of cores to run DLPOLY                                                              |
CP2K_CORE_COUNT                 | int             | 8                 | Number of cores to run CP2K                                                                |
GAUSSIAN_N_TRIES                | int             | 10                | Number of tries to run Gaussian job before giving up                                       | If negative will run infinitely
AIMALL_N_TRIES                  | int             | 10                | Number of tries to run AIMAll job before giving up                                         | If negative will run infinitely
SCRUB_POINTS                    | bool            | False             | Whether or not to remove any bad/failed points after Gaussian or AIMALL are ran            | Only implemented for Gaussian and Aimall currently. Default is false.
FEREBUS_SWARM_SIZE              | int             | 50                | Swarm size for FEREBUS PSO                                                                 |
FEREBUS_NUGGET                  | float           | 1.0e-10           | Nugget parameter for FEREBUS                                                               |
FEREBUS_THETA_MIN               | float           | 0.0               | Min theta value for PSO initialisation in FEREBUS                                          |
FEREBUS_THETA_MAX               | float           | 3.0               | Max theta value for PSO initialisation in FEREBUS                                          |
MAX_NUGGET                      | float           | 1e-4              | ICHOR v2 iteratively increased nugget value when near singular matrix was encountered      | Can probably delete this # todo: delete MAX_NUGGET
FEREBUS_INERTIA_WEIGHT          | float           | 0.72900           | Inertia weight for FEREBUS PSO                                                             |
FEREBUS_COGNITIVE_LEARNING_RATE | float           | 1.49400           | Cognitive learning rate for FEREBUS PSO                                                    |
FEREBUS_SOCIAL_LEARNING_RATE    | float           | 1.49400           | Social learning rate for FEREBUS PSO                                                       |
FEREBUS_MEAN                    | str             | constant          | Mean function for ferebus to use                                                           | Currently only constant implemented
FEREBUS_OPTIMISATION            | str             | pso               | Optimiser for ferebus                                                                      | Currently only PSO implemented
FEREBUS_TOLERANCE               | float           | 1.0e-8            | Tolerance for relative difference calculation in ferebus PSO                               | 1e-8 is reasonably strict convergence criteria
FEREBUS_STALL_ITERATIONS        | int             | 50                | Stall iterations for relative difference calculation in ferebus PSO                        | 50 is reasonably strict convergence criteria
FEREBUS_CONVERGENCE             | int             | 20                | Old version of FEREBUS_STALL_ITERATIONS                                                    | Can probably delete # todo: delete FEREBUS_CONVERGENCE
FEREBUS_MAX_ITERATION           | int             | 1000              | Number of iterations FEREBUS PSO should run for                                            |
DLPOLY_VERSION                  | Version         | 4.09              | Current DLPOLY version                                                                     | Older versions of DLPOLY used different inputs # todo: reimplement older dlpoly version
DLPOLY_NUMBER_OF_STEPS          | int             | 500               | Number of steps to run DLPOLY simulation for                                               | DLPOLY currently not implemented in v3                                                         # todo: implement interface to DLPOLY
DLPOLY_TEMPERATURE              | int             | 0                 | Temperature to run DLPOLY simulation (K)                                                   | DLPOLY currently not implemented in v3                                                         # todo: implement interface to DLPOLY
DLPOLY_PRINT_EVERY              | int             | 1                 | DLPOLY output prints every `DLPOLY_PRINT_EVERY` timesteps                                  | DLPOLY currently not implemented in v3                                                         # todo: implement interface to DLPOLY
DLPOLY_TIMESTEP                 | float           | 0.001             | Length of timestep in DLPOLY simulation (ps)                                               | DLPOLY currently not implemented in v3                                                         # todo: implement interface to DLPOLY
DLPOLY_LOCATION                 | Path            | PROGRAMS/DLPOLY.Z | Path to DLPOLY executable                                                                  | DLPOLY currently not implemented in v3                                                         # todo: implement interface to DLPOLY
DLPOLY_CHECK_CONVERGENCE        | bool            | False             | Older DLPOLY version allowed for convergence check in geometry optimisations               | DLPOLY currently not implemented in v3                                                         # todo: implement interface to DLPOLY
DLPOLY_CONVERGENCE_CRITERIA     | int             | -1                | Older DLPOLY version allowed for convergence check in geometry optimisations               | DLPOLY currently not implemented in v3                                                         # todo: implement interface to DLPOLY
DLPOLY_MAX_ENERGY               | float           | -1.0              | Older DLPOLY version allowed for convergence check in geometry optimisations               | DLPOLY currently not implemented in v3                                                         # todo: implement interface to DLPOLY
DLPOLY_MAX_FORCE                | float           | -1.0              | Older DLPOLY version allowed for convergence check in geometry optimisations               | DLPOLY currently not implemented in v3                                                         # todo: implement interface to DLPOLY
DLPOLY_RMS_FORCE                | float           | -1.0              | Older DLPOLY version allowed for convergence check in geometry optimisations               | DLPOLY currently not implemented in v3                                                         # todo: implement interface to DLPOLY
DLPOLY_MAX_DISP                 | float           | -1.0              | Older DLPOLY version allowed for convergence check in geometry optimisations               | DLPOLY currently not implemented in v3                                                         # todo: implement interface to DLPOLY
DLPOLY_RMS_DISP                 | float           | -1.0              | Older DLPOLY version allowed for convergence check in geometry optimisations               | DLPOLY currently not implemented in v3                                                         # todo: implement interface to DLPOLY
CP2K_INPUT                      | str             |                   | CP2K input geometry file                                                                   | CP2K interface not implemented in v3                                                           # todo: implement CP2K interface for v3
CP2K_TEMPERATURE                | int             | 300               | Temperature to run CP2K simulation (K)                                                     | CP2K interface not implemented in v3                                                           # todo: implement CP2K interface for v3
CP2K_STEPS                      | int             | 10000             | Number of timesteps to run CP2K simulation for                                             | CP2K interface not implemented in v3                                                           # todo: implement CP2K interface for v3
CP2K_TIMESTEP                   | float           | 1.0               | Length of timestep in CP2K simulation (ps)                                                 | CP2K interface not implemented in v3                                                           # todo: implement CP2K interface for v3
CP2K_METHOD                     | str             | BLYP              | QM method for CP2K simulation                                                              | CP2K interface not implemented in v3                                                           # todo: implement CP2K interface for v3
CP2K_BASIS_SET                  | str             | 6-31G*            | Basis set for CP2K simulation                                                              | CP2K interface not implemented in v3                                                           # todo: implement CP2K interface for v3
CP2K_DATA_DIR                   | str             |                   | Path to CP2K data directory                                                                | CP2K interface not implemented in v3                                                           # todo: implement CP2K interface for v3
WARN_RECOVERY_ERROR             | bool            | True              | Switch on warnings for large recovery errors                                               | Warnings not currently implemented in v3                                                       # todo: implement recovery error warning for v3
RECOVERY_ERROR_THRESHOLD        | float           | 0.00038           | Threshold to warn user about large recover errors (Ha)                                     | Warnings not currently implemented in v3                                                       # todo: implement recovery error warning for v3
WARN_INTEGRATION_ERROR          | bool            | True              | Switch on warnings for large integration errors                                            | Warnings not currently implemented in v3                                                       # todo: implement integration error warning for v3
INTEGRATION_ERROR_THRESHOLD     | float           | 0.001             | Threshold to warn user about large integration erorrs                                      | Warnings not currently implemented in v3                                                       # todo: implement integrations error warning for v3
LOG_WARNINGS                    | bool            | False             | Switch to write warnings to log file                                                       | Warnings not currently implemented in v3                                                       # todo: implement warnings for v3
OS                              | OS              | OS.Linux          | Current operating system                                                                   | Should automatically detect between linux, macos and windows
DISABLE_PROBLEMS                | bool            | False             | Disables showing problems at the top of the main menu                                      | Problems currently not implemented for v3                                                      # todo: implement problems for v3
UID                             | UUID            | Arguments.uid     | Unique ID for ichor instance                                                               | Very important variable for making sure ichor reads and writes data to the correct location
IQA_MODELS                      | bool            | False             | Deprecated variable for older ferebus version to toggle whether ichor is making iqa models | No longer required # todo: delete `IQA_MODELS`
DROP_COMPUTE                  | bool            | False             | Toggle whether to use drop-n-compute                                                       | Drop-n-compute not currently implemented for v3                                                # todo: implement drop-n-compute interface for v3
DROP_COMPUTE_LOCATION         | Path            |                   | Location of drop-n-compute directory                                                       | Drop-n-compute not currently implemented for v3                                                # todo: implement drop-n-compute interface for v3
GIT_USERNAME                    | str             |                   | Git username for cloning popelier-group repositories                                       | Shouldn't be needed if GIT_TOKEN is defined
GIT_PASSWORD                    | str             |                   | Git password for cloning popelier-group repositories                                       | Git has deprecated use of passwords on remote machines                                         # todo: delete `GIT_PASSWORD`
GIT_TOKEN                       | str             | ghp_...           | Git token for cloning popelier-group repositories                                          |
INCLUDE_NODES                   | List[str]       | []                | Node whitelist for ichor to run jobs on                                                    |
EXCLUDE_NODES                   | List[str]       | []                | Node blacklist for ichor not to run jobs on                                                |
"""

import inspect
import os
import platform
from ast import literal_eval
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
from typing import List, Optional, Union
from uuid import UUID, uuid4

from ichor.core import constants
from ichor.core.atoms.atoms import Atoms
from ichor.core.atoms.calculators import ALF
from ichor.core.common.types import Version
from ichor.hpc.globals import checkers, formatters, parsers
from ichor.hpc.globals.config_provider import ConfigProvider
from ichor.hpc.globals.os import OS
from ichor.hpc.globals.parsers import read_alf

# todo: automatically generate md table from global variables into 'doc/GLOBALS.md'


class GlobalVariableError(Exception):
    pass


class Globals:
    # format: off
    _types = []

    # Variables that can't be set from config file
    _protected: List[str] = []
    # Variables set in config
    _in_config: List[str] = []
    # Default values for variables
    _defaults = {}
    # Allowed values for variables
    _allowed_values = {}

    # For parsing global variables into type
    _parsers = defaultdict(list)
    # For formatting global variables after parsing
    _formatters = defaultdict(list)
    # For checking global variables after formatting
    _checkers = defaultdict(list)

    # for saving the location the global variables were loaded from
    _config_file: Optional[Path] = None

    SYSTEM_NAME: str = "SYSTEM"

    _POINTS_LOCATION: Path = (
        None  # a file / directory which contains geometries
    )
    _ATOMS_REFERENCE_FILE: Path = None  # set automatically if not defined. Can be manually defined in config properties, which then modified self._ATOMS
    _ATOMS: Atoms = None  # set automatically if not defined
    _ALF_REFERENCE_FILE: Path = None  # set automatically if not defined. Can be manually defined in config properties
    _ALF: List[ALF] = None

    CWD: Path = Path(os.getcwd())

    N_ITERATIONS: int = 1
    POINTS_PER_ITERATION: int = 1

    BATCH_SIZE: int = 5000

    OPTIMISE_PROPERTY: str = "iqa"
    OPTIMISE_ATOM: str = "all"

    ACTIVE_LEARNING_METHOD: str = "epe"

    MAX_RUNNING_TASKS: int = -1  # set to <= 0 for unlimited tasks

    NORMALISE: bool = False
    STANDARDISE: bool = False

    METHOD: str = "B3LYP"
    BASIS_SET: str = "6-31+g(d,p)"
    KEYWORDS: List[str] = []

    AIMALL_ENCOMP: int = 3
    AIMALL_BOAQ: str = "gs20"
    AIMALL_IASMESH: str = "fine"
    AIMALL_BIM: str = "auto"
    AIMALL_CAPTURE: str = "auto"
    AIMALL_EHREN: int = 0
    AIMALL_FEYNMAN: bool = False
    AIMALL_IASPROPS: bool = True
    AIMALL_MAGPROPS: str = "none"
    AIMALL_SOURCE: bool = False
    AIMALL_IASWRITE: bool = False
    AIMALL_ATIDSPROPS: str = "0.001"
    AIMALL_WARN: bool = True
    AIMALL_SCP: str = "some"
    AIMALL_DELMOG: bool = True
    AIMALL_SKIPINT: bool = False
    AIMALL_F2W: str = "wfx"
    AIMALL_F2WONLY: bool = False
    AIMALL_MIR: float = -1.0
    AIMALL_CPCONN: str = "moderate"
    AIMALL_INTVEEAA: str = "new"
    AIMALL_ATLAPRHOCPS: bool = False
    AIMALL_WSP: bool = True
    AIMALL_SHM: int = 5
    AIMALL_MAXMEM: int = 2400
    AIMALL_VERIFYW: str = "yes"
    AIMALL_SAW: bool = False
    AIMALL_AUTONNACPS: bool = True

    TRAINING_POINTS: int = 500
    SAMPLE_POINTS: int = 9000
    VALIDATION_POINTS: int = 500

    TRAINING_SET_METHOD: List[str] = ["min_max_mean"]
    SAMPLE_POOL_METHOD: List[str] = ["random"]
    VALIDATION_SET_METHOD: List[str] = ["random"]

    KERNEL: str = "periodic"  # rbf or rbf-cyclic currently
    FEREBUS_TYPE: str = (
        "executable"  # executable (FEREBUS) or python (FEREBUS.py)
    )
    FEREBUS_VERSION: Version = Version("7.0")
    FEREBUS_LOCATION: Path = None

    FEREBUS_LIKELIHOOD: str = "concentrated"

    GAUSSIAN_MEMORY_LIMIT: str = "1GB"

    # CORE COUNT SETTINGS FOR RUNNING PROGRAMS (SUFFIX CORE_COUNT)
    GAUSSIAN_NCORES: int = 2
    AIMALL_NCORES: int = 2
    FEREBUS_NCORES: int = 4
    DLPOLY_NCORES: int = 1
    CP2K_NCORES: int = 8
    PYSCF_NCORES: int = 2
    MORFI_NCORES: int = 4
    AMBER_NCORES: int = 1
    TYCHE_NCORES: int = 1

    # N TRIES SETTINGS FOR RETRYING TO RUN PROGRAMS
    GAUSSIAN_N_TRIES: int = 10
    AIMALL_N_TRIES: int = 10

    # WHETHER OR NOT TO RERUN POINTS THAT HAVE FAILED (UP TO GAUSSIAN_N_TRIES, AIMALL_N_TRIES)
    RERUN_POINTS = False
    # WHETHER OR NOT TO MOVE POINTS FOR WHICH AIMALL OR GAUSSIAN HAVE FAILED OR CONTAIN BAD DATA.
    SCRUB_POINTS: bool = True

    FEREBUS_SWARM_SIZE: int = (
        50  # If negative >> Size dynamically allocated by FEREBUS
    )
    FEREBUS_NUGGET: float = 1.0e-10  # Default value for FEREBUS nugget
    FEREBUS_THETA_MIN: float = (
        0.0  # Minimum theta value for initialisation (best to keep 0)
    )
    FEREBUS_THETA_MAX: float = 3.0  # Maximum theta value for initialisation

    MAX_NUGGET: float = 1e-4

    FEREBUS_INERTIA_WEIGHT: float = 0.72900
    FEREBUS_COGNITIVE_LEARNING_RATE: float = 1.49400
    FEREBUS_SOCIAL_LEARNING_RATE: float = 1.49400

    FEREBUS_MEAN: str = "constant"
    FEREBUS_OPTIMISATION: str = "pso"

    FEREBUS_TOLERANCE: float = 1.0e-8
    FEREBUS_STALL_ITERATIONS: int = 20
    FEREBUS_CONVERGENCE: int = 20
    FEREBUS_MAX_ITERATION: int = 1000

    # DLPOLY RUNTIME SETTINGS (PREFIX DLPOLY)
    DLPOLY_VERSION: Version = Version("4.09")

    DLPOLY_NUMBER_OF_STEPS: int = 500  # Number of steps to run simulation for
    DLPOLY_TEMPERATURE: int = (
        0  # If set to 0, will perform geom opt but default to 10 K
    )
    DLPOLY_PRINT_EVERY: int = 1  # Print trajectory and stats every n steps
    DLPOLY_TIMESTEP: float = 0.001  # in ps
    DLPOLY_LOCATION: Path = None
    DLPOLY_HOOVER: float = 0.04

    DLPOLY_CHECK_CONVERGENCE: bool = False
    DLPOLY_CONVERGENCE_CRITERIA: int = -1
    DLPOLY_CELL_SIZE: float = 25.0

    DLPOLY_MAX_ENERGY: float = -1.0
    DLPOLY_MAX_FORCE: float = -1.0
    DLPOLY_RMS_FORCE: float = -1.0
    DLPOLY_MAX_DISP: float = -1.0
    DLPOLY_RMS_DISP: float = -1.0

    # CP2K SETTINGS
    CP2K_INPUT: str = ""
    CP2K_TEMPERATURE: int = 300  # K
    CP2K_STEPS: int = 10000
    CP2K_TIMESTEP: float = 1.0  # fs
    CP2K_METHOD: str = "BLYP"
    CP2K_BASIS_SET: str = "6-31G*"
    CP2K_DATA_DIR: str = ""

    # AMBER SETTINGS
    AMBER_TEMPERATURE: float = 300  # K
    AMBER_TIMESTEP: float = 0.001  # ps
    AMBER_STEPS: int = 100000
    AMBER_LN_GAMMA: float = 0.7

    # TYCHE SETTINGS
    TYCHE_TEMPERATURE: float = 300  # K
    TYCHE_STEPS: int = 10000
    TYCHE_LOCATION: Path = None

    # OPTIMUM ENERGY
    OPTIMUM_ENERGY: float = None
    OPTIMUM_ENERGY_FILE: Path = None

    # Recovery and Integration Errors
    WARN_RECOVERY_ERROR: bool = True
    RECOVERY_ERROR_THRESHOLD: float = (
        1.0 / constants.ha_to_kj_mol
    )  # Ha (1.0 kJ/mol)

    WARN_INTEGRATION_ERROR: bool = True
    INTEGRATION_ERROR_THRESHOLD: float = 0.001

    # Activate Warnings when making models
    LOG_WARNINGS: bool = (
        False  # Gets set in create_ferebus_directories_and_submit
    )

    OS: OS = OS.Linux

    DISABLE_PROBLEMS: bool = False
    UID: UUID = uuid4()

    IQA_MODELS: bool = False

    DROP_COMPUTE: bool = False
    DROP_COMPUTE_LOCATION: Path = ""

    PANDORA_LOCATION: Path = ""
    PANDORA_CCSDMOD: str = "ccsdM"
    MORFI_ANGULAR: int = 5
    MORFI_RADIAL: float = 10.0
    MORFI_ANGULAR_H: int = 5
    MORFI_RADIAL_H: float = 8.0

    ADD_DISPERSION_TO_IQA: bool = True

    GIT_USERNAME: str = ""
    GIT_PASSWORD: str = ""
    GIT_TOKEN: str = " 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"

    INCLUDE_NODES: List[str] = []
    EXCLUDE_NODES: List[str] = []

    # format: on

    def __init__(
        self,
        config_file: Optional[Path] = None,
        globals_instance: Optional["Globals"] = None,
        **kwargs,
    ):

        # this is needed because properties which are in self.global_variables also have setter methods
        # we do not have these properties already set like the rest of the class variables above
        # check types
        for global_variable in self.global_variables:
            # if variable is not in annotations or variable does not have a setter method
            if global_variable not in self.__annotations__.keys():
                if global_variable not in self.properties_with_setter_methods:
                    self.__annotations__[global_variable] = type(
                        self.get(global_variable)
                    )
                # if it is a setter method, then make the type default to Path
                # TODO: make this inspect the output of the property and check what type it returns
                # TODO: then, this is going to be added to parsers/formatters and then it will update
                # the variable using the setter method for the property
                else:
                    self.__annotations__[global_variable] = Path

        # Set Protected Variables
        self._protected = [
            "FILE_STRUCTURE",
            "SGE",
            "SUBMITTED",
            "UID",
            "IQA_MODELS",
            "MACHINE",
            "OS",
            "ATOMS",
            "CWD",
        ]

        # Setup Parsers
        for global_variable in self.global_variables:
            global_type = self.__annotations__[global_variable]
            if global_type is str:
                self._parsers[global_variable] += [parsers.parse_str]
            elif global_type is bool:
                self._parsers[global_variable] += [parsers.parse_bool]
            elif global_type is int:
                self._parsers[global_variable] += [parsers.parse_int]
            elif global_type is float:
                self._parsers[global_variable] += [parsers.parse_float]
            elif global_type is Path:
                self._parsers[global_variable] += [parsers.read_path]

        # add these separately because these attributes have more complicated types
        self._parsers["KEYWORDS"] += [parsers.split_keywords]
        self._parsers["FEREBUS_VERSION"] += [parsers.read_version]
        self._parsers["DLPOLY_VERSION"] += [parsers.read_version]
        self._parsers["INCLUDE_NODES"] += [parsers.split_keywords]
        self._parsers["EXCLUDE_NODES"] += [parsers.split_keywords]
        self._parsers["TRAINING_SET_METHOD"] += [parsers.split_keywords]
        self._parsers["SAMPLE_POOL_METHOD"] += [parsers.split_keywords]
        self._parsers["VALIDATION_SET_METHOD"] += [parsers.split_keywords]
        self._parsers["UID"] += [parsers.read_uid]
        # TODO: Make sure List[int] is parsed correctly

        # Setup Formatters
        for global_variable in self.global_variables:
            global_type = self.__annotations__[global_variable]
            if global_type is str:
                self._formatters[global_variable] += [formatters.cleanup_str]

        self._formatters["SYSTEM_NAME"] += [formatters.to_upper]
        self._formatters["OPTIMISE_PROPERTY"] += [formatters.to_lower]

        # Setup Checkers
        self._allowed_values = {
            "METHOD": constants.GAUSSIAN_METHODS,
            "AIMALL_BOAQ": constants.BOAQ_VALUES,
            "AIMALL_IASMESH": constants.IASMESH_VALUES,
            "FEREBUS_TYPE": constants.FEREBUS_TYPES,
            "OPTIMISE_PROPERTY": ["iqa"] + constants.multipole_names + ["all"],
            "KERNEL": constants.KERNELS,
        }

        # TODO: Checks to add
        # - Basis Set (not sure how to do this one)
        # - Optimise Atom, must be done after determining system
        # - Check FEREBUS Location
        # - Check DLPOLY Location
        # - FEREBUS Mean
        # - FEREBUS Optimiser
        # - CP2K Method
        # - CP2K Basis Set

        # set up a dictionary, whose values are functions which
        # check if the values given to the GLOBALS options are allowed
        for variable, allowed_values in self._allowed_values.items():
            self._checkers[variable] += [
                lambda val, av=allowed_values: checkers.check_allowed(val, av)
            ]
        # adaptive sampling checks
        self._checkers["MAX_ITERATION"] += [checkers.positive]
        self._checkers["POINTS_PER_ITERATION"] += [checkers.positive]
        self._checkers["TRAINING_POINTS"] += [checkers.positive_or_zero]
        self._checkers["SAMPLE_POINTS"] += [checkers.positive_or_zero]
        self._checkers["VALIDATION_POINTS"] += [checkers.positive_or_zero]
        # FEREBUS checks
        self._checkers["FEREBUS_SWARM_SIZE"] += [checkers.positive]
        self._checkers["FEREBUS_NUGGET"] += [checkers.positive]
        self._checkers["FEREBUS_INERTIA_WEIGHT"] += [checkers.positive]
        self._checkers["FEREBUS_COGNITIVE_LEARNING_RATE"] += [
            checkers.positive
        ]
        self._checkers["FEREBUS_SOCIAL_LEARNING_RATE"] += [checkers.positive]
        self._checkers["FEREBUS_TOLERANCE"] += [checkers.positive]
        self._checkers["FEREBUS_STALL_ITERATIONS"] += [checkers.positive]
        self._checkers["FEREBUS_CONVERGENCE"] += [checkers.positive]
        self._checkers["FEREBUS_MAX_ITERATION"] += [checkers.positive]
        # DLPOLY checks
        self._checkers["DLPOLY_NUMBER_OF_STEPS"] += [checkers.positive]
        self._checkers["DLPOLY_TEMPERATURE"] += [checkers.positive_or_zero]
        self._checkers["DLPOLY_PRINT_EVERY"] += [checkers.positive]
        self._checkers["DLPOLY_TIMESTEP"] += [checkers.positive]
        # CP2K checks
        self._checkers["CP2K_TEMPERATURE"] += [checkers.positive]
        self._checkers["CP2K_STEPS"] += [checkers.positive]
        self._checkers["CP2K_TIMESTEP"] += [checkers.positive]

        # Setup Defaults. These can be reverted to if needed.
        for global_variable in self.global_variables:
            # modify variables which are in global variables but also have setter methods
            # this then stores the underscore-beginning values which were going to be used in the setter methods
            if global_variable in self.properties_with_setter_methods:
                global_variable = f"_{global_variable}"
            self._defaults[global_variable] = self.get(global_variable)

        # Set OS
        if platform in {"linux", "linux2"}:
            self.OS = OS.Linux
        elif platform == "darwin":
            self.OS = OS.MacOS
        elif platform == "win32":
            self.OS = OS.Windows

        if config_file:
            self.init_from_config(config_file)

        if globals_instance is not None:
            self.init_from_globals(globals_instance)

        # if an option that is not supported is passed in, raise error
        for key, value in kwargs.items():
            if key not in self.global_variables:
                raise GlobalVariableError(
                    f"Global Variable: {key} does not exist."
                )
            self.set(key, value)

        # TODO: add MAX_RUINNING_TASKS to Globals docstring
        if "MAX_RUNNING_TASKS" not in self._in_config:
            from ichor.hpc import MACHINE, Machine

            if MACHINE is Machine.ffluxlab:
                self.MAX_RUNNING_TASKS = (
                    25  # <- might be a bit conservative, increase in future?
                )
            elif MACHINE is Machine.csf3:
                self.MAX_RUNNING_TASKS = -1

    @property
    def POINTS_LOCATION(self):
        if self._POINTS_LOCATION is None:
            try:
                self._POINTS_LOCATION = get_atoms_reference_file(Path.cwd())
            except FileNotFoundError as e:
                raise ValueError("Define 'GLOBALS.POINTS_LOCATION'") from e
        if not self._POINTS_LOCATION.exists():
            raise FileNotFoundError(
                f"'POINTS_LOCATION' '{self._POINTS_LOCATION}' was not found"
            )
        return self._POINTS_LOCATION

    @POINTS_LOCATION.setter
    def POINTS_LOCATION(self, value: Union[str, Path]):
        """Set the alf reference file to a specified file."""
        value = Path(value)
        if not value.exists():
            raise FileNotFoundError(
                f"'POINTS_LOCATION: '{value}' was not found"
            )
        self._POINTS_LOCATION = value.resolve()

    @property
    def ATOMS_REFERENCE_FILE(self) -> Path:
        if self._ATOMS_REFERENCE_FILE is None:
            return self.POINTS_LOCATION
        if not self._ATOMS_REFERENCE_FILE.exists():
            raise FileNotFoundError(
                f"'ATOMS_REFERENCE_FILE: '{self._ATOMS_REFERENCE_FILE}' was not found"
            )
        return self.ATOMS_REFERENCE_FILE.resolve()

    @ATOMS_REFERENCE_FILE.setter
    def ATOMS_REFERENCE_FILE(self, value: Union[str, Path]):
        """Set the alf reference file to a specified file."""
        value = Path(value)
        if not value.exists():
            raise FileNotFoundError(
                f"'ATOMS_REFERENCE_FILE: '{value}' was not found"
            )
        self._ALF_REFERENCE_FILE = value.resolve()

    @property
    def ALF_REFERENCE_FILE(self) -> Path:
        if self._ALF_REFERENCE_FILE is None:
            return self.ATOMS_REFERENCE_FILE
        if not self._ALF_REFERENCE_FILE.exists():
            raise FileNotFoundError(
                f"'ALF_REFERENCE_FILE: '{self._ALF_REFERENCE_FILE}' was not found"
            )
        return self._ALF_REFERENCE_FILE.resolve()

    @ALF_REFERENCE_FILE.setter
    def ALF_REFERENCE_FILE(self, value: Union[str, Path]):
        """Set the alf reference file to a specified file."""
        value = Path(value)
        if not value.exists():
            raise FileNotFoundError(
                f"'ALF_REFERENCE_FILE: '{value}' was not found"
            )
        self._ALF_REFERENCE_FILE = value.resolve()

    @property
    def ATOMS(self) -> Atoms:
        return get_atoms(self.ATOMS_REFERENCE_FILE)

    @property
    def ALF(self) -> List["ALF"]:
        """Returns the atomic local frame for every atom in the system.
        This is in the form of a list of lists, where each inner lists contains
        three integers. These integers represent the central atom (the atom on
        which the ALF is currently centered on), the x-axis atom, and the
        xy-plane atom (if system has more than 2 atoms). Note that these
        are 0-indexed because it makes it easier to use the ALF this way in
        Python.

        :returns: A list of lists (of ints), representing the ALF of the system.
        """
        if self._ALF is None:
            self._ALF = [
                atom.alf() for atom in get_atoms(self.ALF_REFERENCE_FILE)
            ]
        return self._ALF

    @ALF.setter
    def ALF(self, alf: List["ALF"]):
        self._ALF = read_alf(alf)

    def init(self, src: Optional[Union[Union[Path, str], "Globals"]] = None):
        """Uses either a config file or another instance of `Globals` from which to
        initialize values for the current Globals instance. Essentially, it copies over
        all the values for user-specified options, so they match the given config file
        or `Globals` instance.

        :param src: A Path object or string pointing to a valid config file
            or another Globals instance

        .. note::
            This does not return a new `Globals` instance. It just modifies the
            values for the options that a user can change.
        """
        if src is not None:
            if isinstance(src, Globals):
                self.init_from_globals(src)
            else:
                src = Path(src)
                self.init_from_config(src)

    def init_from_config(self, config_file: Path):
        """Reads in options from a config file and sets the values of the
        attributes in this `Globals` instance based on the values read.

        :param config_file: A config file from which to copy options

        .. note::
            This does not return a new `Globals` instance. It just modifies the
            values for the options that a user can change.
        """
        self._config_file = config_file
        config = ConfigProvider(source=config_file)

        for key, val in config.items():
            if key in self.global_variables:
                self.set(key, val)
                self._in_config += [key]
            elif key in [
                "MAX_ITERATION",
                "N_ITERATION",
            ]:  # Deprecated variable names
                self.set("N_ITERATIONS", val)
                self._in_config += ["N_ITERATIONS"]
            else:
                # PROBLEM_FINDER.unknown_settings += [key]
                pass  # todo: fix this

    def init_from_globals(self, globals_instance: "Globals"):
        """Reads in options another `Globals` instance and sets the values of the
        attributes in this `Globals` instance based on the values read from the other
        `Globals` instance

        :param globals_instance: A `Globals` instance from which to copy options

        .. note::
            This does not return a new `Globals` instance. It just modifies the
            values for the options that a user can change.
        """
        for key, value in globals_instance.items(show_protected=True):
            self.set(key, value)

    def set(self, name: str, value):
        """Sets a value for a `Globals` variable.

        :param name: Name of variable for which to set value
        :param value: A value to set for the variable.

        .. note::
            The type of the value is checked in the __setattr__ method
        """
        name = name.upper()
        if name not in self.global_variables:
            # PROBLEM_FINDER.unknown_settings.append(name)
            pass  # todo: fix this
        elif name in self._protected:
            # PROBLEM_FINDER.protected_settings.append(name)
            pass  # todo: fix this
        else:
            try:
                setattr(self, name, value)
            except ValueError as e:
                # PROBLEM_FINDER.incorrect_settings[name] = e
                pass  # todo: fix this

    def get(self, name: str):
        """Returns the value for some attribute/class variable or None if the attribute/class variable is not set."""
        return getattr(self, name, None)

    def items(self, show_protected=False):
        return [
            (global_variable, getattr(self, global_variable))
            for global_variable in self.global_variables
            if global_variable not in self._protected or show_protected
        ]

    def save_to_properties_config(self, config_file: Path, global_variables):
        with open(config_file, "w") as config:
            config.write(f"{constants.ichor_logo}\n\n")
            for key, val in global_variables.items():
                if str(val) in {"[]", "None"}:
                    continue
                config.write(f"{key}={val}\n")

    def save_to_yaml_config(self, config_file: Path, global_variables):
        try:
            import yaml
        except ImportError as e:
            raise ImportError(
                f"Must have 'yaml' module installed to save to yaml file ({config_file})"
            )

        with open(config_file, "w") as config:
            yaml.dump(global_variables, config)

    def save_to_config(self, config_file: Optional[Path] = None):
        """Save the GLOBALS variables and values to a config file. Only the non-default options are saved. This means this function will write out
        an empty config.properties file (with only the ichor logo present) if all the options have been left to the default options.

        :param config_file: A string or Path to a config file to which to write config options, defaults to None. If None is given the `Arguments`
            class config file is used.
        """

        if config_file is None:
            if self._config_file is None:
                # if no config file is provided and the instance of globals wasn't defined from a config, default to
                # `Arguments.config_file`
                from ichor.hpc.arguments import Arguments

                config_file = Arguments.config_file
            else:
                config_file = self._config_file
        config_file = Path(config_file)

        global_variables = {}
        for global_variable, global_value in self.items():
            if global_variable in self.properties_with_setter_methods:
                # if a property with a setter method, append _ because this is the hidden variable
                if (
                    global_value != self._defaults["_" + global_variable]
                    or global_variable in self._in_config
                ):
                    global_variables[global_variable] = global_value
            else:
                if (
                    global_value != self._defaults[global_variable]
                    or global_variable in self._in_config
                ):
                    global_variables[global_variable] = global_value

        if config_file.suffix == ".properties":
            self.save_to_properties_config(config_file, global_variables)
        elif config_file.suffix == ".yaml":
            self.save_to_yaml_config(config_file, global_variables)

    @property
    def config_variables(self):
        return [
            g for g in self.global_variables if g in self._in_config.keys()
        ]

    @property
    def properties_with_setter_methods(self) -> List[str]:
        """Returns a list of strings for properties which can be set with a setter method. The setter
        method is the same name as the property and it updates a variable begginning with an underscore _ ."""
        return [
            p[0]
            for p in inspect.getmembers(
                Globals, lambda o: isinstance(o, property)
            )
            if p[1].fset is not None
        ]

    @property
    def global_variables(self) -> List[str]:
        """Returns a list of strings which are all the options that a user can set
        through the GLOBALS class.

        :returns: A list of strings corresponding to all the attributes that can
            be set through GLOBALS.
        """

        try:
            return self._global_variables
        except AttributeError:

            # methods implemented in Globals
            methods = [
                f[0]
                for f in inspect.getmembers(
                    Globals, predicate=inspect.isfunction
                )
            ]

            # properties implemented in Globals
            properties = [
                p[0]
                for p in inspect.getmembers(
                    Globals, lambda o: isinstance(o, property)
                )
                if p[1].fset is None
            ]
            methods += properties

            # get all attributes which do not start with _ (as these cannot be set by user)
            # and which are not methods/properties
            self._global_variables = [
                key
                for key in dir(self)
                if not key.startswith("_") and key not in methods
            ]

            return self._global_variables

    def __setattr__(self, name, value):
        if (
            hasattr(self, "_global_variables")
            and name in self.global_variables
        ):
            for parser in self._parsers.get(name, []):
                value = parser(value)
            for formatter in self._formatters.get(name, []):
                value = formatter(value)
            for check in self._checkers.get(name, []):
                check(value)  # Should raise error if incorrect

        super(Globals, self).__setattr__(name, value)

    def __enter__(self, *args, **kwargs):
        from ichor.hpc import globals

        self._save_globals = Globals(globals_instance=globals.GLOBALS)
        globals.GLOBALS.init_from_globals(self)

    def __exit__(self, type, value, traceback):
        from ichor.hpc import globals

        globals.GLOBALS.init_from_globals(self._save_globals)


class NoAtomsFound(Exception):
    pass


@lru_cache()
def get_atoms(atoms_reference_path: Path) -> Atoms:
    """Gets an Atoms instance from an atom_reference_path that was given."""

    if atoms_reference_path.exists():

        if atoms_reference_path.is_file():
            if atoms_reference_path.suffix == ".gjf":
                from ichor.core.files import GJF

                return GJF(atoms_reference_path).atoms
            elif atoms_reference_path.suffix == ".xyz":
                from ichor.core.files import XYZ

                return XYZ(atoms_reference_path).atoms
            else:
                raise ValueError(
                    f"Unknown filetype {atoms_reference_path}. Make sure to choose a .gjf or .xyz file."
                )

        elif atoms_reference_path.is_dir():
            from ichor.core.files import PointsDirectory

            return PointsDirectory(atoms_reference_path)[0].atoms

        # we should have returned by now, but return None if no file matches criteria
        return

    else:
        raise FileNotFoundError(
            f"ATOMS reference file with path {atoms_reference_path} is not found on disk."
        )


@lru_cache()
def get_atoms_reference_file(path: Union[Path, str] = None) -> Path:
    """Gets an Atoms instance from an atom_reference_path that was given."""

    # default to current directory
    if not path:
        path = Path()

    if not path.exists():
        raise FileNotFoundError("The given path does not exist on disk.")
    for file_or_dir in path.iterdir():

        if file_or_dir.is_file():
            if file_or_dir.suffix in [".gjf", ".xyz"]:
                return file_or_dir.resolve()
        elif file_or_dir.is_dir():
            for p in file_or_dir.iterdir():
                if p.is_dir():
                    for f1 in p.iterdir():
                        if f1.suffix in [".gjf", ".xyz"]:
                            return f1.resolve()
                elif p.suffix == ".gjf" or path.suffix == ".xyz":
                    return p.resolve()
    # return None if no file that matches criteria was found.
    raise FileNotFoundError("Could not find atoms reference file")

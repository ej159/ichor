from functools import wraps
from typing import Optional

import numpy as np

from ichor.common.functools import cached_property, classproperty
from ichor.common.functools.buildermethod import buildermethod
from ichor.common.str import get_digits
from ichor.files.file import File, FileContents
from ichor.itypes import F
from ichor.models.kernels import RBF, Kernel, RBFCyclic
from ichor.models.kernels.interpreter import KernelInterpreter
from ichor.models.mean import ConstantMean, Mean, ZeroMean


def check_x_2d(func: F) -> F:
    @wraps(func)
    def wrapper(self, x, *args, **kwargs):
        if x.ndim == 1:
            x = x[np.newaxis, :]
        return func(self, x, *args, **kwargs)

    return wrapper


class Model(File):
    """A model file that is returned back from our machine learning program FEREBUS.

    .. note::
        Another program can be used for the machine learning as long as it outputs files of the same format as the FEREBUS outputs.
    """

    # these can be accessed with __annotations__, so leave them
    _system: Optional[str]
    _atom: Optional[str]
    _type: Optional[str]
    _nfeats: Optional[int]
    _ntrain: Optional[int]
    _mean: Optional[Mean]
    _k: Optional[Kernel]
    _x: Optional[np.ndarray]
    _y: Optional[np.ndarray]
    # _weights: Optional[np.ndarray] = None

    nugget: Optional[float] = None

    def __init__(self, path):
        File.__init__(self, path)
        self.nugget = 1e-10

        self._system: Optional[str] = FileContents
        self._atom: Optional[str] = FileContents
        self._type: Optional[str] = FileContents
        self._nfeats: Optional[int] = FileContents
        self._ntrain: Optional[int] = FileContents
        self._mean: Optional[Mean] = FileContents
        self._k: Optional[Kernel] = FileContents
        self._x: Optional[np.ndarray] = FileContents
        self._y: Optional[np.ndarray] = FileContents

    @buildermethod
    def _read_file(self) -> None:
        """Read in a FEREBUS output file which contains the optimized hyperparameters, mean function, and other information that is needed to make predictions."""
        kernel_composition = ""
        kernel_list = {}

        # implemented as a series of if statements to reduced number of iterations needed to read the file
        with open(self.path) as f:
            for line in f:
                if line.startswith("#"):
                    continue

                if "name" in line:  # system name e.g. WATER
                    self._system = line.split()[1]
                    continue

                if line.startswith(
                    "atom"
                ):  # atom for which a GP model was made
                    self._atom = line.split()[1]
                    continue

                if (
                    "property" in line
                ):  # property (such as IQA or particular multipole moment) for which a GP model was made
                    self._type = line.split()[1]
                    continue

                if "nugget" in line:
                    self.nugget = float(line.split()[-1])
                    continue

                if "number_of_features" in line:
                    self._nfeats = int(line.split()[1])
                    continue

                if (
                    "number_of_training_points" in line
                ):  # number of training points to make the GP model
                    self._ntrain = int(line.split()[1])
                    continue

                if "[mean]" in line:
                    _ = next(f)
                    line = next(f)
                    self._mean = ConstantMean(float(line.split()[1]))
                    continue

                if (
                    "composition" in line
                ):  # which kernels were used to make the GP model. Different kernels can be specified for different input dimensions
                    kernel_composition = line.split()[-1]
                    continue

                if "[kernel." in line:
                    kernel_name = line.split(".")[-1].rstrip().rstrip("]")
                    line = next(f)
                    kernel_type = line.split()[-1].strip()

                    if kernel_type == "rbf":
                        _ = next(f)
                        _ = next(f)
                        line = next(f)
                        lengthscale = np.array(
                            [float(hp) for hp in line.split()[1:]]
                        )
                        # todo: Rename theta to lengthscale in ferebus because it is more widely used / easier to think about
                        # TODO: Change theta from FEREBUS to lengthscale to match label
                        kernel_list[kernel_name] = RBF(lengthscale)
                    elif kernel_type in [
                        "rbf-cyclic",
                        "rbf-cylic",
                    ]:  # Due to typo in FEREBUS 7.0
                        line = next(f)
                        line = next(f)
                        line = next(f)
                        lengthscale = np.array(
                            [float(hp) for hp in line.split()[1:]]
                        )
                        kernel_list[kernel_name] = RBFCyclic(lengthscale)
                    continue

                if "[training_data.x]" in line:
                    line = next(f)
                    x = []
                    while line.strip() != "":
                        x += [[float(num) for num in line.split()]]
                        line = next(f)
                    self._x = np.array(x)
                    continue

                if "[training_data.y]" in line:
                    line = next(f)
                    y = []
                    while line.strip() != "":
                        y += [float(line)]
                        line = next(f)
                    self._y = np.array(y)
                    continue

                # if "[weights]" in line:
                #     line = next(f)
                #     weights = []
                #     while line.strip() != "":
                #         weights += [float(line)]
                #         try:
                #             line = next(f)
                #         except:
                #             break
                #     self.weights = np.array(weights)
                #     self.weights = self.weights[:, np.newaxis]

        self.k = KernelInterpreter(kernel_composition, kernel_list).interpret()

    @cached_property
    def system(self):
        return self._system

    @cached_property
    def atom(self):
        return self._atom

    @cached_property
    def type(self):
        return self._type

    @cached_property
    def nfeats(self):
        return self._nfeats

    @cached_property
    def ntrain(self):
        return self._ntrain

    @cached_property
    def mean(self):
        return self._mean

    @cached_property
    def k(self):
        return self._k

    @cached_property
    def x(self):
        return self._x

    @cached_property
    def y(self):
        return self._y

    @classproperty
    def filetype(self) -> str:
        return ".model"

    def write(self) -> None:
        # TODO
        pass

    @cached_property
    def atom_num(self) -> int:
        return get_digits(self.atom)

    @cached_property
    def i(self) -> int:
        return self.atom_num - 1

    @check_x_2d
    def r(self, x: np.ndarray) -> np.ndarray:
        return self.k.r(self.x, x)

    @cached_property
    def weights(self):
        return np.matmul(
            self.invR, self.y[:, np.newaxis] - self.mean.value(self.x)
        )

    @cached_property
    def R(self) -> np.ndarray:
        return self.k.R(self.x) + (self.nugget * np.eye(self.ntrain))

    @cached_property
    def invR(self) -> np.ndarray:
        return np.linalg.inv(self.R)

    @check_x_2d
    def predict(self, x: np.ndarray) -> np.ndarray:
        return (
            self.mean.value(x) + np.dot(self.k.r(self.x, x).T, self.weights)
        ).flatten()

    @check_x_2d
    def variance(self, x: np.ndarray) -> np.ndarray:
        r = self.k.r(self.x, x).T
        invR = self.invR
        ones = np.ones((self.ntrain, 1))
        variance = np.empty(len(x))
        res3 = np.matmul(np.matmul(ones.T, invR), ones)

        # TODO: Remove loop
        for i, ri in enumerate(r):
            res1 = np.matmul(np.matmul(ri.T, invR), ri)
            res2 = (1.0 - np.matmul(np.matmul(ones.T, invR), ri)) ** 2
            variance[i] = 1.0 - res1 + res2 / res3
        return variance

    def __repr__(self):
        return (
            f"Model(system={self.system}, atom={self.atom}, type={self.type})"
        )

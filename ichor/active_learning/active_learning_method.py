from abc import ABC, abstractmethod
from typing import List
from ichor.atoms import ListOfAtoms
from ichor.common.functools import classproperty
from ichor.models import Models
import numpy as np

class ActiveLearningMethod(ABC):
    def __init__(self, models: Models):
        self.models = models

    @abstractmethod
    @classproperty
    def name(self) -> str:
        """Name of the expected improvement function to be selected from GLOBALS."""
        pass

    @abstractmethod
    def get_points(self, points: ListOfAtoms, npoints: int) -> np.ndarray:
        """
        Method which gets the indeces of the points to be added from the sample pool to the training set based on active learning criteria.
        """
        pass

    def __call__(self, points: ListOfAtoms, npoints: int) -> np.ndarray:
        """Once an instance of an `ActiveLearningMethod` has been created, the instance can be called as a function (which will then
        go into this __call__ method and execute self.get_points() which is defined in each subclass of `ActiveLearningMethod`"""
        return self.get_points(points, npoints)
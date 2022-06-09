import random
from typing import List

from ichor.cli.make_set_methods.make_set_method import MakeSetMethod
from ichor.core.atoms import ListOfAtoms


class RandomPoints(MakeSetMethod):
    """Chooses random points from the sample pool which are added to the training set"""

    npoints: int = 1

    def __init__(self, npoints: int):
        self.npoints = npoints

    @classmethod
    def get_npoints(cls, npoints: int, points: ListOfAtoms) -> int:
        return npoints

    @classmethod
    def name(cls) -> str:
        return "random"

    def get_points(self, points: ListOfAtoms) -> List[int]:
        return random.sample(
            range(len(points)), k=min(self.npoints, len(points))
        )
import sys
from pathlib import Path
from typing import Optional, List

from ichor.batch_system import JobID
from ichor.common.io import last_line
from ichor.files import PointsDirectory, GJF
from ichor.logging import logger
from ichor.submission_script import (SCRIPT_NAMES, GaussianCommand,
                                     SubmissionScript, print_completed)


def submit_points_directory_to_gaussian(directory: Path) -> Optional[JobID]:
    """Function that writes out .gjf files from .xyz files that are in each directory and 
    calls submit_gjfs which submits all .gjf files in a directory to Gaussian. Gaussian outputs .wfn files.

    :param directory: A Path object which is the path of the directory (commonly traning set path, sample pool path, etc.).
    """
    points = PointsDirectory(
        directory
    )  # a directory which contains points (a bunch of molecular geometries)
    gjf_files = write_gjfs(points)
    return submit_gjfs(gjf_files)

def write_gjfs(points: PointsDirectory) -> List[Path]:
    """Writes out .gjf files in every PointDirectory which is contained in a PointsDirectory. Each PointDirectory should always have a `.xyz` file in it,
    which contains only one molecular geometry. This `.xyz` file can be used to write out the `.gjf` file in the PointDirectory (if it does not exist already).

    :param points: A PointsDirectory instance which wraps around a whole directory containing points (such as TRAINING_SET).
    :return: A list of Path objects which point to `.gjf` files in each PointDirectory that is contained in the PointsDirectory.
    """
    gjfs = []
    for point in points:
        if not point.gjf.exists():
            point.gjf = GJF(Path(point.path / (point.path.name + GJF.filetype)))
            point.gjf.atoms = point.xyz
        point.gjf.write()
        gjfs.append(point.gjf.path)
    return gjfs


def submit_gjfs(gjfs: List[Path], force: bool = False, hold: Optional[JobID] = None) -> Optional[JobID]:
    """Function that writes out a submission script which contains an array of Gaussian jobs to be ran on compute nodes. If calling this function from
    a log-in node, it will write out the submission script, a datafile (file which contains the names of all the .gjf file that need to be ran through Gaussian),
    and it will submit the submission script to compute nodes as well to run Gaussian on compute nodes. However, if using this function from a compute node,
    (which will happen when ichor is ran in auto-run mode), this function will only be used to write out the datafile and will not submit any new jobs
    from the compute node (as you cannot submit jobs from compute nodes on CSF3.)

    :param gjfs: A list of Path objects pointing to .gjf files
    :param force: todo: Not sure when this is used[description], defaults to False
    :param hold: An optional JobID for which this job to hold. This is used in auto-run to hold this job for the previous job to finish, defaults to None
    :return: The JobID of this job given by the submission system.
    """

    # make a SubmissionScript instance which is going to house all the jobs that are going to be ran
    # the submission_script object can be accessed even after the context manager
    with SubmissionScript(SCRIPT_NAMES["gaussian"]) as submission_script:
        for gjf in gjfs:
            if force or not gjf.with_suffix('.wfn').exists():
                submission_script.add_command(GaussianCommand(gjf))
                logger.debug(
                    f"Adding {gjf} to {submission_script.path}"
                )  # make a list of GaussianCommand instances.
    # write the final submission script file that containing the job that needs to be ran (could be an array job that has many tasks)
    if len(submission_script.commands) > 0:
        logger.info(
            f"Submitting {len(submission_script.commands)} GJF(s) to Gaussian"
        )
        # submit the final submission script to the queuing system, so that job is ran on compute nodes.
        return submission_script.submit(hold=hold)


def rerun_gaussian(gaussian_file: str):
    """Used by `CheckManager`. Checks if Gaussian jobs ran correctly and a full .wfn file is returned. If there is no .wfn file or it does not
    have the correct contents, then rerun Gaussian.
    
    :param gaussian_file: A string that is a Path to a .gjf file
    """
    if not gaussian_file:
        print_completed()
        sys.exit()
    if Path(gaussian_file).with_suffix(
        ".wfn"
    ).exists() and "TOTAL ENERGY" in last_line(
        Path(gaussian_file).with_suffix(".wfn")
    ):
        print_completed()
    else:
        logger.error(f"Gaussian Job {gaussian_file} failed to run")

def scrub_gaussian_point(gaussian_file: str):
    """ Used by `CheckManager`. Checks if Gaussian job ran correctly. If it did not, it will move the Point to the `FILE_STRUCTURE["gaussian_scrubbed_points"]` directory
    and record that it has moved the point in the log file. If a .wfn file exists and it contains the correct information in its last line, then
    this checking function will not do anything.
    
    :param gaussian_file: A string that is a Path to a .gjf file
    """

    from ichor.common.io import mkdir, move
    from ichor.logging import logger
    from ichor.file_structure import FILE_STRUCTURE

    if gaussian_file:

        wfn_file_name = Path(gaussian_file).with_suffix(".wfn")

        if (not wfn_file_name.exists()) or (not "TOTAL ENERGY" in last_line(wfn_file_name)):
            mkdir(FILE_STRUCTURE["gaussian_scrubbed_points"])
            # get the name of the directory only containing the .gjf file
            point_dir_name = wfn_file_name.parent.name
            # get the Path to the Parent directory
            point_dir_path = wfn_file_name.parent
            new_path = FILE_STRUCTURE["gaussian_scrubbed_points"] / point_dir_name

            # move to new path and record in logger
            move(point_dir_path, new_path)
            logger.error(f"Moved point directory {point_dir_path} to {new_path} because it failed to run.")

from pathlib import Path
from typing import Optional

from ichor.batch_system import JobID
from ichor.common.types import MutableValue
from ichor.main.pandora import submit_points_directory_to_morfi
from ichor.submission_script import (SCRIPT_NAMES, ICHORCommand,
                                     SubmissionScript, TimingManager)


def submit_ichor_morfi_command_to_auto_run(
    directory: Path,
    atoms: Optional[MutableValue],
    hold: Optional[JobID] = None,
) -> Optional[JobID]:
    """Writes out the datafile needed to submit the wavefunction files to AIMALL. The actual AIMALL calculations are ran in the next step."""
    submission_script = SubmissionScript(
        SCRIPT_NAMES["ichor"]["pandora"]["morfi"]
    )
    ichor_command = ICHORCommand(auto_run=True)
    ichor_command.add_function_to_job(
        submit_points_directory_to_morfi, str(directory), atoms.value
    )
    with TimingManager(submission_script, message="Submitting WFNs"):
        submission_script.add_command(ichor_command)
    submission_script.write()
    return submission_script.submit(hold=hold)
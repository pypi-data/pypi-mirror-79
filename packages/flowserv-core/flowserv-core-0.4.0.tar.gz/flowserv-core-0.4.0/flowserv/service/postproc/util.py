# This file is part of the Reproducible and Reusable Data Analysis Workflow
# Server (flowServ).
#
# Copyright (C) 2019-2020 NYU.
#
# flowServ is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""This module contains helper functions that prepare the input data for
post-porcessing workflows.
"""

import os
import shutil
import tempfile

import flowserv.util as util
import flowserv.service.postproc.base as base


def prepare_postproc_data(input_files, ranking, run_manager):
    """Create input and output directories for post-processing steps.

    The input directory contains a file runs.json that lists the runs in the
    ranking together with their group name. For each run a sub-folder with the
    run identifier as name is created. That folder contains copies of result
    files for the run for those files that are specified in the input files
    list.

    Returns the created temporary input directory.

    Parameters
    ----------
    input_files: list(string)
        List of identifier for benchmark run output files that are copied into
        the input directory for each submission.
    ranking: list(flowserv.model.ranking.RunResult)
        List of runs in the current result ranking
    run_manager: flowserv.model.run.RunManager
        Manager for workflow runs

    Returns
    -------
    string
    """
    # Copy the required input files from all workflow runs in the ranking to
    # subfolders in a temporary input directory. The directory will also
    # contain the 'runs.json' file containing the run metadata.
    basedir = tempfile.mkdtemp()
    run_listing = list()
    for entry in ranking:
        # Create a sub-folder for the run in the ranking result. Then copy the
        # requested files from the run resources to that folder.
        run_id = entry.run_id
        rundir = os.path.join(basedir, run_id)
        os.makedirs(rundir, exist_ok=True)
        for in_key in input_files:
            _, filename = run_manager.get_runfile(run_id=run_id, key=in_key)
            target_file = os.path.join(rundir, in_key)
            os.makedirs(os.path.dirname(target_file), exist_ok=True)
            # The run file may either be the path to a local file on disk or
            # a BytesIO buffer.
            if isinstance(filename, str):
                shutil.copy(src=filename, dst=target_file)
            else:
                with open(target_file, 'wb') as f:
                    f.write(filename.read())
        run_listing.append({
            base.LABEL_ID: run_id,
            base.LABEL_NAME: entry.group_name,
            base.LABEL_FILES: input_files
        })
    # Write the runs metadata to file
    util.write_object(
        filename=os.path.join(basedir, base.RUNS_FILE),
        obj=run_listing
    )
    # Return created temporary data directory
    return basedir

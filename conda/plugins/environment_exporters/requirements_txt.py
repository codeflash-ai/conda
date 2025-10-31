# Copyright (C) 2012 Anaconda, Inc
# SPDX-License-Identifier: BSD-3-Clause
"""Built-in conda requirements environment exporter plugin.

This module implements the requirements format defined in CEP 23:
Files with MatchSpec strings (no @EXPLICIT marker) for flexible package specifications.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from conda.models.environment import Environment

from ... import __version__
from ...exceptions import CondaValueError
from ..hookspec import hookimpl
from ..types import CondaEnvironmentExporter

if TYPE_CHECKING:
    from typing import Final

    from ...models.environment import Environment


#: The name of the requirements format
REQUIREMENTS_FORMAT: Final = "requirements"


def export_requirements(env: Environment) -> str:
    """Export Environment to requirements format with MatchSpecs (CEP 23 compliant)."""
    # Only create requirements files if we have requested packages
    if not env.requested_packages:
        raise CondaValueError(
            "Cannot export requirements format: no requested packages found. "
            "Use 'explicit' format for environments with installed packages, "
            "or ensure the environment has package specifications."
        )

    lines = [
        "# This file may be used to create an environment using:",
        "# $ conda create --name <env> --file <this file>",
        f"# platform: {env.platform}",
        f"# created-by: conda {__version__}",
        "# Note: This is a conda requirements file (MatchSpec format)",
        "# Contains conda package specifications, not pip requirements",
        ""
    ]
    
    lines.extend(map(str, env.requested_packages))
    return "\n".join(lines)


@hookimpl
def conda_environment_exporters():
    """Environment exporter plugin for requirements format."""
    yield CondaEnvironmentExporter(
        name=REQUIREMENTS_FORMAT,
        aliases=("reqs", "txt"),
        export=export_requirements,
        default_filenames=("requirements.txt", "spec.txt"),
    )

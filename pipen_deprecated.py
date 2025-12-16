from __future__ import annotations

from typing import Type
from pipen.utils import get_marked, get_logger
from pipen.pluginmgr import plugin
from pipen.proc import Proc

logger = get_logger("depr", "info")
__version__ = "1.0.0"


def _deprecate_proc(proc_obj: Proc, proc: Type[Proc]) -> bool:
    """Show deprecation warning for a process."""
    depr = get_marked(proc, "deprecated")
    if not depr:
        # Check if it is a subclass of a deprecated process
        for base in proc.__bases__:
            if base is Proc or not issubclass(base, Proc):
                continue

            dpr = _deprecate_proc(proc_obj, base)
            if dpr:
                return True
        return False

    if depr is True:
        depr = (
            "This is process is [bold][yellow]DEPRECATED[/yellow][/bold] and "
            "will be removed in a future release."
        )

    depr = depr.format(proc=proc)
    proc_obj.log("warning", depr, logger=logger)
    return True


class PipenDeprecatedPlugin:
    """pipen-deprecated plugin: marking pipen processes as deprecated."""

    __version__ = __version__
    name = "deprecated"

    @plugin.impl
    async def on_proc_start(self, proc: Proc):
        """Check if a process is deprecated and log a warning."""
        _deprecate_proc(proc, proc.__class__)


pipen_deprecated_plugin = PipenDeprecatedPlugin()

# pipen-deprecated

Marking [pipen](https://github.com/pwwang/pipen) processes as deprecated.

# Installation

```bash
pip install -U pipen-deprecated
```

# Enable/Disable
The plugin is enabled by default after installation. To disable it, either uninstall it or:

```python
from pipen import Proc, Pipen

# process definition

class MyPipeline(Pipen):
    plugins = ["-deprecated"]
```

# Usage

To mark a process as deprecated, use the `@mark(deprecated=...)` decorator.

```python
from pipen import Proc
from pipen.utils import mark

@mark(deprecated=True)
class ProcDeprecatedTrue(Proc):
    ...


@mark(deprecated="This process is deprecated.")
class ProcDeprecatedMessage(Proc):
    ...
```

When a deprecated process is run, a warning message will be logged.

If the process is marked with `deprecated=True`, the message will be:

```
[ProcDeprecatedTrue] is deprecated and will be removed in a future release.
```

If a custom message is provided, it will be used instead:

```
[ProcDeprecatedMessage] This process is deprecated.
```

You can use `proc` in the message as a placeholder for the process class. For example:

```python
@mark(deprecated='"{proc.name}" is deprecated.')
class ProcDeprecatedMessage(Proc):
    ...
```

This will log:

```
"ProcDeprecatedMessage" is deprecated.
```

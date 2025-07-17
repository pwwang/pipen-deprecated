import pytest  # noqa: F401 # type: ignore
from pipen import Proc, Pipen
from pipen.utils import mark


class BaseProc(Proc):
    """A base process class for testing."""

    input = "invar:var"
    input_data = [1]
    output = "outvar:var"
    script = "echo 'Hello, World!'"


@mark(deprecated=True)
class ProcDeprecatedTrue(BaseProc):
    """A process that is marked as deprecated with True."""


@mark(deprecated="{proc.name} is deprecated.")
class ProcDeprecatedMessage(BaseProc):
    """A process that is marked as deprecated with a custom message."""


class ProcDeprecatedInherited(ProcDeprecatedTrue): ...


def test_normal_proc(caplog):
    """Test a normal process without deprecation."""

    class PipelineNormal(Pipen):
        starts = BaseProc

    pipeline = PipelineNormal()
    pipeline.run()

    assert "is deprecated" not in caplog.text


def test_deprecated_true_proc(caplog):
    """Test a process marked as deprecated with True."""

    class PipelineDeprecatedTrue(Pipen):
        starts = ProcDeprecatedTrue

    pipeline = PipelineDeprecatedTrue()
    pipeline.run()

    assert (
        "[ProcDeprecatedTrue] is DEPRECATED and will be removed in a future release."
        in caplog.text
    )


def test_deprecated_message_proc(caplog):
    """Test a process marked as deprecated with a custom message."""

    class PipelineDeprecatedMessage(Pipen):
        starts = ProcDeprecatedMessage

    pipeline = PipelineDeprecatedMessage()
    pipeline.run()

    assert "ProcDeprecatedMessage is deprecated." in caplog.text


def test_deprecated_inherited_proc(caplog):
    """Test a process that inherits deprecation from its parent."""

    class PipelineDeprecatedInherited(Pipen):
        starts = ProcDeprecatedInherited

    pipeline = PipelineDeprecatedInherited()
    pipeline.run()

    assert (
        "[ProcDeprecatedTrue] is DEPRECATED and will be removed in a future release."
        in caplog.text
    )

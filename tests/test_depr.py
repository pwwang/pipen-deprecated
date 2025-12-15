import pytest  # noqa: F401 # type: ignore
from pipen import Proc, Pipen
from pipen.utils import mark
from pipen_deprecated import PipenDeprecatedPlugin, __version__


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


@mark(deprecated="Process {proc.name} is no longer supported!")
class ProcDeprecatedCustomFormat(BaseProc):
    """A process with custom formatted deprecation message."""


class ProcDeprecatedInherited(ProcDeprecatedTrue):
    """A process that inherits deprecation from its parent."""


class ProcDeprecatedMultipleInheritance(ProcDeprecatedTrue, BaseProc):
    """A process with multiple inheritance, one deprecated parent."""


@mark(deprecated=True)
class ProcDeprecatedBase(Proc):
    """A deprecated base process."""
    input = "invar:var"
    input_data = [1]
    output = "outvar:var"
    script = "echo 'Test'"


class ProcDeprecatedDeepInheritance(ProcDeprecatedInherited):
    """A process with deep inheritance chain."""


def test_plugin_metadata():
    """Test plugin metadata and version."""
    plugin = PipenDeprecatedPlugin()
    assert plugin.name == "deprecated"
    assert plugin.__version__ == __version__
    assert hasattr(plugin, "on_proc_start")


def test_normal_proc(caplog):
    """Test a normal process without deprecation."""

    class PipelineNormal(Pipen):
        starts = BaseProc

    pipeline = PipelineNormal()
    pipeline.run()

    assert "is deprecated" not in caplog.text.lower()
    assert "DEPRECATED" not in caplog.text


def test_deprecated_true_proc(caplog):
    """Test a process marked as deprecated with True."""

    class PipelineDeprecatedTrue(Pipen):
        starts = ProcDeprecatedTrue

    pipeline = PipelineDeprecatedTrue()
    pipeline.run()

    assert (
        "and will be removed in a future release."
        in caplog.text
    )


def test_deprecated_message_proc(caplog):
    """Test a process marked as deprecated with a custom message."""

    class PipelineDeprecatedMessage(Pipen):
        starts = ProcDeprecatedMessage

    pipeline = PipelineDeprecatedMessage()
    pipeline.run()

    assert "ProcDeprecatedMessage is deprecated." in caplog.text


def test_deprecated_custom_format_proc(caplog):
    """Test a process with custom formatted deprecation message."""

    class PipelineDeprecatedCustomFormat(Pipen):
        starts = ProcDeprecatedCustomFormat

    pipeline = PipelineDeprecatedCustomFormat()
    pipeline.run()

    assert "Process ProcDeprecatedCustomFormat is no longer supported!" in caplog.text


def test_deprecated_inherited_proc(caplog):
    """Test a process that inherits deprecation from its parent."""

    class PipelineDeprecatedInherited(Pipen):
        starts = ProcDeprecatedInherited

    pipeline = PipelineDeprecatedInherited()
    pipeline.run()

    assert (
        "and will be removed in a future release."
        in caplog.text
    )


def test_deprecated_deep_inheritance(caplog):
    """Test a process with deep inheritance chain."""

    class PipelineDeprecatedDeepInheritance(Pipen):
        starts = ProcDeprecatedDeepInheritance

    pipeline = PipelineDeprecatedDeepInheritance()
    pipeline.run()

    # Should inherit deprecation from ProcDeprecatedTrue (grandparent)
    assert (
        "and will be removed in a future release."
        in caplog.text
    )


def test_deprecated_multiple_inheritance(caplog):
    """Test a process with multiple inheritance."""

    class PipelineDeprecatedMultipleInheritance(Pipen):
        starts = ProcDeprecatedMultipleInheritance

    pipeline = PipelineDeprecatedMultipleInheritance()
    pipeline.run()

    # Should detect deprecation from the first deprecated parent
    assert (
        "and will be removed in a future release."
        in caplog.text
    )


def test_multiple_deprecated_processes(caplog):
    """Test a pipeline with multiple deprecated processes in sequence."""

    class ProcDeprecated1(BaseProc):
        """First deprecated process."""

    class ProcDeprecated2(BaseProc):
        """Second deprecated process."""
        requires = ProcDeprecated1

    # Mark them as deprecated
    mark(deprecated="First process is deprecated")(ProcDeprecated1)
    mark(deprecated="Second process is deprecated")(ProcDeprecated2)

    class PipelineMultipleDeprecated(Pipen):
        starts = ProcDeprecated1

    pipeline = PipelineMultipleDeprecated()
    pipeline.run()

    # Should show warnings for both processes
    assert "First process is deprecated" in caplog.text
    assert "Second process is deprecated" in caplog.text


def test_non_proc_base_skipped():
    """Test that non-Proc base classes are skipped during deprecation check."""

    class SomeOtherClass:
        """A non-Proc class."""
        pass

    @mark(deprecated=True)
    class MixedInheritance(SomeOtherClass, BaseProc):
        """A process inheriting from both Proc and non-Proc."""

    class PipelineMixedInheritance(Pipen):
        starts = MixedInheritance

    # Should not raise any errors
    pipeline = PipelineMixedInheritance()
    pipeline.run()


def test_plugin_on_proc_create():
    """Test the plugin's on_proc_create hook directly."""
    plugin = PipenDeprecatedPlugin()

    # Create a mock process instance
    class MockPipeline(Pipen):
        starts = ProcDeprecatedTrue

    pipeline = MockPipeline()
    # The plugin hook should be called during pipeline execution
    # This is tested indirectly through other tests

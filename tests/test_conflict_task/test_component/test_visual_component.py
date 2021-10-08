import pytest
from psychopy import visual

from conflict_task.component.visual_component import VisualComponent
from conflict_task.constants import *
from conflict_task.devices.window import Window


def test_no_name(win: Window, capsys: pytest.CaptureFixture):
    with pytest.raises(SystemExit):
        VisualComponent({"type": "TextStim", "spec": {}}, win)

    assert (
        "Please specify a name for each VisualComponent, either at top level or in spec"
        in capsys.readouterr().out
    )


def test_name_specified_top_level(win: Window):
    component = VisualComponent({"name": "Text", "type": "TextStim", "spec": {}}, win)
    assert component.name == "Text"


def test_name_specified_in_spec(win: Window):
    component = VisualComponent({"type": "TextStim", "spec": {"name": "Text"}}, win)
    assert component.name == "Text"


def test_no_type(win: Window, capsys: pytest.CaptureFixture):
    with pytest.raises(SystemExit):
        VisualComponent({"name": "Text", "spec": {}}, win)

    assert "Text: VisualComponents must specify a 'type'" in capsys.readouterr().out


def test_unknown_type(win: Window, capsys: pytest.CaptureFixture):
    with pytest.raises(SystemExit):
        VisualComponent({"name": "Text", "type": "SillyDucks", "spec": {}}, win)

    assert (
        "Text: There's no visual component type SillyDucks" in capsys.readouterr().out
    )


def test_no_spec(win: Window, capsys: pytest.CaptureFixture):
    with pytest.raises(SystemExit):
        VisualComponent({"name": "Text", "type": "TextStim"}, win)

    assert (
        "Text: VisualComponents require specifications - use 'spec' field"
        in capsys.readouterr().out
    )


def test_spec_not_dictionary(win: Window, capsys: pytest.CaptureFixture):
    with pytest.raises(SystemExit):
        VisualComponent({"name": "Text", "type": "TextStim", "spec": 23}, win)

    assert f"'spec' must be of type '{dict}'" in capsys.readouterr().out


def test_all_settings_are_set(win: Window):
    component = VisualComponent(
        {
            "type": "TextStim",
            "spec": {
                "name": "Text",
                "font": "Arial",
                "bold": True,
                "italic": True,
                "pos": (1.0, 2.0),
                "color": "white",
                "height": 0.05,
            },
        },
        win,
    )

    assert type(component.component) is visual.TextStim
    assert component.component.name == "Text"
    assert component.component.font == "Arial"
    assert component.component.bold
    assert component.component.italic
    assert all(a == b for a, b in zip(component.component.pos, [1.0, 2.0]))
    assert all(a == b for a, b in zip(component.component.color, [1.0, 1.0, 1.0]))
    assert component.component.height == 0.05

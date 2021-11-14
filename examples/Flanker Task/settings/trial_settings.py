from conflict_task.devices.window import Window

FONT_SIZE = 42

fixation_cross = dict(
    start=0.0,
    stop=0.75,
    type="text",
    spec=dict(
        name="fixation_cross",
        text="+",
        color="black",
        font="Courier New",
        size=FONT_SIZE,
    ),
)

distractor = dict(
    start=0.75,
    stop=1.7,
    type="text",
    spec=dict(
        name="distractor",
        color="black",
        size=FONT_SIZE,
        font="Courier New",
    ),
    variable=dict(text="distractor_text"),
)

target = dict(
    start=0.85,
    stop=1.7,
    type="text",
    spec=dict(
        name="target",
        color="black",
        size=FONT_SIZE,
        font="Courier New",
    ),
    variable=dict(
        text="target_text",
    ),
)

response = dict(
    start=0.85,
    stop=2.0,
    keys=["left", "right"],
    variable=dict(
        correct_key="correct_key",
    ),
)

trial_sequence = {
    "type": "Trial",
    "visual_components": [fixation_cross, distractor, target],
    "response": response,
    "takes_trial_values": True,
}


if __name__ == "__main__":
    from conflict_task.preview import preview_sequence, preview_component

    for values in [
        {
            "distractor_text": "HH HH",
            "target_text": "H",
            "correct_key": "left",
        },
        {
            "distractor_text": "SS SS",
            "target_text": "H",
            "correct_key": "left",
        },
        {
            "distractor_text": "HH HH",
            "target_text": "S",
            "correct_key": "right",
        },
        {
            "distractor_text": "SS SS",
            "target_text": "S",
            "correct_key": "right",
        }
    ]:
        preview_sequence(trial_sequence, sequence_values=values)

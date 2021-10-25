FONT_FAMILY = "Courier New"

distractor = {
    "start": 1.0,
    "stop": 1.133,
    "type": "TextStim",
    "spec": {
        "name": "distractor",
        "color": "black",
        "height": 64,
        "font": FONT_FAMILY,
    },
    "variable": {
        "text": "distractor_text",
    },
}

target = {
    "start": 1.166,
    "stop": 1.3,
    "type": "TextStim",
    "spec": {"name": "target", "color": "black", "height": 103, "font": FONT_FAMILY},
    "variable": {
        "text": "target_text",
    },
    "marker": 61,
}

response = {
    "start": 1.3,
    "duration": 1.383,
    "keys": ["f", "g", "j", "n"],
    "variable": {
        "correct_key": "correct_key",
    },
    "marker": [41, 42, 43],
}

feedback = {
    "stop": 0.2,
    "type": "TextStim",
    "spec": {"name": "feedback", "color": "black", "height": 80, "font": FONT_FAMILY},
    "variable": {
        "text": "feedback_text",
    },
}

trial_sequence = {
    "type": "Trial",
    "visual_components": [distractor, target],
    "response": response,
    "takes_trial_values": True,
    "feedback": True,
    "marker": True,
    "feedback_sequence": {
        "visual_components": [feedback],
        "marker": True,
        "marker_addition": 20,
        "trial_values": lambda trial: {
            **trial,
            "feedback_text": (
                "Zu langsam"
                if not trial["response_made"]
                else ("Fehler" if not trial["response_correct"] else "")
            )
            if trial["feedback_block"]
            else "",
        },
    },
}

if __name__ == "__main__":
    from conflict_task.devices import EMGConnector
    from conflict_task.preview import preview_sequence

    EMGConnector.connect()

    for values in [
        {
            "distractor_text": "Left\nLeft\nLeft",
            "target_text": "Right",
            "correct_key": "g",
            "feedback_opacity": 0.0,
            "marker_start": 1,
            "marker_end": 11,
        },
        {
            "distractor_text": "Left\nLeft\nLeft",
            "target_text": "Right",
            "correct_key": "g",
            "feedback_opacity": 1.0,
            "marker_start": 1,
            "marker_end": 11,
        },
        {
            "distractor_text": "Left\nLeft\nLeft",
            "target_text": "Right",
            "correct_key": "g",
            "feedback_opacity": 0.0,
            "marker_start": 1,
            "marker_end": 11,
        },
    ]:
        preview_sequence(trial_sequence, sequence_values=values)

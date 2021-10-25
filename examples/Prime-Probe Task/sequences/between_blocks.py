FONT_FAMILY = "Courier New"

between_blocks_text = """
Wenn Sie wieder bereit sind, starten Sie den nächsten Block mit der Leertaste
"""

between_blocks = {
    "type": "Screen",
    "cut_on_response": True,
    "visual_components": [
        {
            "name": "text",
            "type": "TextStim",
            "spec": {
                "text": between_blocks_text,
                "height": 72,
                "wrapWidth": 1500,
                "font": FONT_FAMILY,
                "color": "black",
            },
        }
    ],
    "response": {"keys": ["space"]},
    "early_quit_keys": ["f12"]
}

if __name__ == "__main__":
    from conflict_task.preview import preview_sequence

    preview_sequence(between_blocks)

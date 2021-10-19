between_blocks_text = """
You can now wait for up to 30 seconds before starting again.

Press [space] to continue.
"""

between_blocks = {
    "type": "Screen",
    "cut_on_response": True,
    "timed": True,
    "timer": 30.0,
    "visual_components": [
        {
            "name": "text",
            "type": "TextStim",
            "spec": {
                "name": "text",
                "color": "white",
                "height": 48,
                "wrapWidth": 1200, 
                "text": between_blocks_text
            }
        }
    ],
    "response": {
        "keys": ["space"]
    },
}

if __name__ == "__main__":
    from conflict_task.preview import preview_sequence

    preview_sequence(between_blocks, window_settings={"units": "pix"})

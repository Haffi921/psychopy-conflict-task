between_blocks_text = """
You can now wait for up to 30 seconds before starting again.

Press [space] to continue.
"""

between_component = dict(
    name="text",
    type="TextStim",
    spec=dict(name="text", color="white", height=0.03, text=between_blocks_text),
)

between_blocks = dict(
    type="Screen",
    visual_components=dict(text=between_component),
    response=dict(keys=["space"]),
    cut_on_response=True,
    timed=True,
    timer=30.0,
)

if __name__ == "__main__":
    from conflict_task.experiment import preview_sequence

    preview_sequence(between_blocks, window_settings={"color": [-1, -1, -1]})

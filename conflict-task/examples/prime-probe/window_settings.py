# Modify these settings to customize experiment window
window_settings = dict(

    # Size of the window in pixels (x, y)
    size = (1920, 1200),

    # Color of background as [r, g, b] list or single value. Each gun can take values between -1.0 and 1.0
    color = [-1, -1, -1],

    # Create a window in ‘full-screen’ mode. Better timing can be achieved in full-screen mode
    fullscreen = True,

    # If not fullscreen, then position of the top-left corner of the window on the screen (x, y)
    pos = (0, 0),

    # Which monitor? 0 is primary monitor, 1 is secondary, etc.
    screen = 0,

    #---- Rest are less useful settings to tinker with, so it's not recommended ----#

    # Set the window type or back-end to use
    winType = 'pyglet',

    # Use framebuffer object
    useFBO = True,

    # Defines the default units of stimuli drawn in the window (can be overridden by each stimulus).
    # Values can be None, ‘height’ (of the window), ‘norm’ (normalised), ‘deg’, ‘cm’, ‘pix’
    units = 'height'
)
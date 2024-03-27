class Config:
    # window size
    WIDTH, HEIGHT = 1080, 800

    # constant
    AU = 149.6e6 * 1000
    G = 6.67428e-11

    # variables
    SCALE = 100 / AU  # 100 / AU is 1AU = 100 pixels. Adjust the scale if needed
    TIMESTEP = 3600 * 24  # 3600 * 24 = 1 day per frame. Adjust the timestep to slow down the simulation
    zoom_factor = 0.05  # How much each scroll zooms in or out
    isPaused = False
    pausedTime = 0  # store the timestep when pause
    aiming_mode = False
    activate_rocket = False

    @classmethod
    def get_scale(cls):
        return cls.SCALE

    @classmethod
    def set_scale(cls, value):
        cls.SCALE = value

    @classmethod
    def get_timestep(cls):
        return cls.TIMESTEP

    @classmethod
    def set_timestep(cls, value):
        cls.TIMESTEP = value

    @classmethod
    def get_zoom_factor(cls):
        return cls.zoom_factor

    @classmethod
    def set_zoom_factor(cls, value):
        cls.zoom_factor = value

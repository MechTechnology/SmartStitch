from core.models.app_settings import AppSettings


class AppProfiles:
    """Model for holding Pointers to Settings Profile"""

    def __init__(self, dict: dict[str, any] = None):
        # Core Settings
        self.current_profile: str = 'default'
        self.settings_profiles: dict[str, any] = {'default': AppSettings()}

        if dict is not None:
            for key, value in dict.items():
                setattr(self, key, value)

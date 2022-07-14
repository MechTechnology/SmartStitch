from .app_settings import AppSettings


class AppProfiles:
    """Model for holding Pointers to Settings Profile"""

    def __init__(self, json_dict: dict[str, any] = None):
        # Core Settings
        self.current_profile: str = 'default'
        self.settings_profiles: dict[str, any] = {'default': vars(AppSettings())}

        if json_dict is not None:
            for key, value in json_dict.items():
                setattr(self, key, value)

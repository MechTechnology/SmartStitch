from .app_settings import AppSettings


class AppProfiles:
    """Model for holding Pointers to Settings Profile"""

    def __init__(self, json_dict: dict[str, any] = None):
        # Core Settings
        self.current: int = 0
        self.profiles: list[dict[str, any]] = [
            {"profile_name": "Settings Profile 1", **vars(AppSettings())}
        ]

        if json_dict is not None:
            for key, value in json_dict.items():
                setattr(self, key, value)

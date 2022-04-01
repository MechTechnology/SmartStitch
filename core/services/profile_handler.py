import json
import os

from core.models.app_profiles import AppProfiles
from core.models.app_settings import AppSettings
from core.services.global_logger import logFunc
from core.utils.constants import SETTINGS_REL_DIR
from core.utils.errors import ProfileException


class ProfileHandler:
    def __init__(self):
        self.profile_file = os.path.join(SETTINGS_REL_DIR, 'profiles.json')
        self.settings_file = os.path.join(SETTINGS_REL_DIR, 'settings.json')
        self.current_profiles = self.load_all()

    def get_profile(self, profile_name: str) -> AppSettings:
        """Selects current profile settings folder"""
        if profile_name not in self.current_profiles.settings_profiles.keys():
            raise ProfileException(profile_name + ' profile does not exist')
        settings_dict = self.current_profiles.settings_profiles[profile_name]
        return AppSettings(settings_dict)

    @logFunc(inclass=True)
    def add_profile(self, profile_name: str, profile_settings: AppProfiles):
        """Adds a settings profile to the collection"""
        self.current_profiles.settings_profiles[profile_name] = vars(profile_settings)
        self.save_all(self.current_profiles)

    @logFunc(inclass=True)
    def remove_profile(self, profile_name: str):
        if profile_name == 'default':
            raise ProfileException('default profile can not be removed')
        if profile_name in self.current_profiles.settings_profiles.keys():
            del self.current_profiles.settings_profiles[profile_name]
            self.save_all(self.current_profiles)

    @logFunc(inclass=True)
    def load_all(self):
        """Loads settings profile pointers from a json file."""
        if not os.path.exists(self.profile_file):
            return self.save_all()
        else:
            with open(self.profile_file, "r") as f:
                return AppProfiles(json.load(f))

    @logFunc(inclass=True)
    def save_all(self, profiles: AppProfiles = None):
        """Saves settings profile pointers from a json file."""
        if not os.path.exists(SETTINGS_REL_DIR):
            os.makedirs(SETTINGS_REL_DIR)
        if not (profiles):
            profiles = AppProfiles()
        with open(self.profile_file, "w") as f:
            json.dump(vars(profiles), f, indent=2)
        return profiles

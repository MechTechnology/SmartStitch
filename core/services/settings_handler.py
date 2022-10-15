import json
import os

from core.utils.errors import ProfileException

from ..models import AppProfiles, AppSettings
from ..services import logFunc
from ..utils.constants import SETTINGS_REL_DIR


class SettingsHandler:
    def __init__(self):
        self.settings_file = os.path.join(SETTINGS_REL_DIR, 'settings.json')
        self.current_profiles = self.load_all()
        self.current_settings = self.load_current_settings()

    def load(self, key: str) -> any:
        """Loads the value of a single setting key"""
        return self.current_settings.__dict__[key]

    @logFunc(inclass=True)
    def save(self, key: str, value: any):
        """Updates a single setting value"""
        self.current_settings.__dict__[key] = value
        self.save_current_settings(self.current_settings)

    def load_current_settings(self) -> AppSettings:
        """Loads application settings from current profile"""
        if not self.current_profiles.profiles:
            return AppSettings()
        return AppSettings(
            self.current_profiles.profiles[self.current_profiles.current]
        )

    def save_current_settings(self, settings: AppSettings = None) -> AppSettings:
        """Saves application settings to current profile"""
        if not (settings):
            settings = AppSettings()
        current_profile = self.current_profiles.profiles[self.current_profiles.current]
        self.current_profiles.profiles[self.current_profiles.current] = {
            **current_profile,
            **vars(settings),
        }
        self.save_all(self.current_profiles)
        return settings

    # Profile Handling Logic
    def get_current_index(self) -> int:
        return self.current_profiles.current

    @logFunc(inclass=True)
    def set_current_index(self, new_index):
        self.current_profiles.current = new_index
        self.save_all(self.current_profiles)
        self.current_settings = self.load_current_settings()

    def get_current_profile_name(self) -> int:
        index = self.current_profiles.current
        if index > len(self.current_profiles.profiles):
            raise ProfileException('Current profile not found')
        return self.current_profiles.profiles[index].get("profile_name")

    def set_current_profile_name(self, new_name):
        index = self.current_profiles.current
        if index > len(self.current_profiles.profiles):
            raise ProfileException('Current profile not found')
        self.current_profiles.profiles[index]["profile_name"] = new_name
        self.save_all(self.current_profiles)

    def get_profile_names(self) -> list[str]:
        names = []
        for profile in self.current_profiles.profiles:
            names.append(profile.get("profile_name"))
        return names

    @logFunc(inclass=True)
    def add_profile(self, profile_name: str = None):
        """Adds a settings profile to the collection"""
        if not profile_name:
            profile_name = "Settings Profile " + str(
                len(self.current_profiles.profiles) + 1
            )
        self.current_profiles.profiles.append(
            {"profile_name": profile_name, **vars(self.current_settings)}
        )
        self.save_all(self.current_profiles)
        return profile_name

    @logFunc(inclass=True)
    def remove_profile(self, index: int):
        if len(self.current_profiles.profiles) == 1:
            raise ProfileException('Last existing profile can not be removed')
        del self.current_profiles.profiles[index]
        self.set_current_index(0)
        self.save_all(self.current_profiles)

    def load_all(self):
        """Loads settings profile pointers from a json file."""
        if not os.path.exists(self.settings_file):
            return self.save_all()
        else:
            with open(self.settings_file, "r") as f:
                return AppProfiles(json.load(f))

    def save_all(self, profiles: AppProfiles = None):
        """Saves settings profile pointers from a json file."""
        if not os.path.exists(SETTINGS_REL_DIR):
            os.makedirs(SETTINGS_REL_DIR)
        if not (profiles):
            profiles = AppProfiles()
        with open(self.settings_file, "w") as f:
            json.dump(vars(profiles), f, indent=2)
        return profiles

import json
import os

from core.utils.errors import ProfileException

from ..models import AppProfiles, AppSettings
from ..services import logFunc
from ..utils.constants import SETTINGS_REL_DIR


class SettingsHandler:
    def __init__(self):
        # Define the path to the settings file
        self.settings_file = os.path.join(SETTINGS_REL_DIR, 'settings.json')

        # Load all profiles and current settings from the file
        self.current_profiles = self.load_all()
        self.current_settings = self.load_current_settings()

    def load(self, key: str) -> any:
        """Loads the value of a single setting key"""
        return self.current_settings.__dict__[key]

    @logFunc(inclass=True)
    def save(self, key: str, value: any):
        """Updates a single setting value"""
        # Update the setting value and save it
        setattr(self.current_settings, key, value)
        self.save_current_settings(self.current_settings)

    def load_current_settings(self) -> AppSettings:
        """Loads application settings from the current profile"""
        if not self.current_profiles.profiles:
            return AppSettings()
        return AppSettings(self.current_profiles.profiles[self.current_profiles.current])

    def save_current_settings(self, settings: AppSettings = None) -> AppSettings:
        """Saves application settings to the current profile"""
        if not settings:
            settings = AppSettings()

        # Update the settings for the current profile and save all profiles
        current_profile = self.current_profiles.profiles[self.current_profiles.current]
        current_profile.update(vars(settings))
        self.save_all(self.current_profiles)
        return settings

    # Profile Handling Logic
    def get_current_index(self) -> int:
        """Returns the index of the current profile"""
        return self.current_profiles.current

    @logFunc(inclass=True)
    def set_current_index(self, new_index):
        """Sets the index of the current profile and saves it"""
        self.current_profiles.current = new_index
        self.save_all(self.current_profiles)
        self.current_settings = self.load_current_settings()

    def get_current_profile_name(self) -> int:
        """Returns the name of the current profile"""
        index = self.current_profiles.current
        if index >= len(self.current_profiles.profiles):
            raise ProfileException('Current profile not found')
        return self.current_profiles.profiles[index].get("profile_name")

    def set_current_profile_name(self, new_name):
        """Sets the name of the current profile and saves it"""
        index = self.current_profiles.current
        if index >= len(self.current_profiles.profiles):
            raise ProfileException('Current profile not found')
        self.current_profiles.profiles[index]["profile_name"] = new_name
        self.save_all(self.current_profiles)

    def get_profile_names(self) -> list[str]:
        """Returns a list of profile names"""
        return [profile.get("profile_name") for profile in self.current_profiles.profiles]

    @logFunc(inclass=True)
    def add_profile(self, profile_name: str = None):
        """Adds a new settings profile to the collection"""
        if not profile_name:
            profile_name = "Settings Profile " + str(len(self.current_profiles.profiles) + 1)
        new_profile = {"profile_name": profile_name, **vars(self.current_settings)}
        self.current_profiles.profiles.append(new_profile)
        self.save_all(self.current_profiles)
        return profile_name

    @logFunc(inclass=True)
    def remove_profile(self, index: int):
        """Removes a profile from the collection"""
        if len(self.current_profiles.profiles) == 1:
            raise ProfileException('Last existing profile cannot be removed')
        del self.current_profiles.profiles[index]
        self.set_current_index(0)
        self.save_all(self.current_profiles)

    def load_all(self):
        """Loads settings profile pointers from a JSON file."""
        if not os.path.exists(self.settings_file):
            # If the file doesn't exist, create a new AppProfiles object and save it
            return self.save_all()
        else:
            # Load the profiles from the existing file
            with open(self.settings_file, "r") as f:
                return AppProfiles(json.load(f))

    def save_all(self, profiles: AppProfiles = None):
        """Saves settings profile pointers to a JSON file."""
        if not os.path.exists(SETTINGS_REL_DIR):
            os.makedirs(SETTINGS_REL_DIR)
        if not profiles:
            profiles = AppProfiles()

        # Save the profiles to the JSON file
        with open(self.settings_file, "w") as f:
            json.dump(vars(profiles), f, indent=2)
        return profiles
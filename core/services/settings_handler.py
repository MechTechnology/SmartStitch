import json
import os
from typing import Any
from core.utils.constants import SETTINGS_REL_DIR
from core.models.app_settings import AppSettings
from core.services.global_logger import logFunc


class SettingsHandler():
  def __init__(self, profile_name: str = "Default"):
    self.select_profile(profile_name)
    self.current_settings = self.load_all()

  @logFunc(inclass=True)
  def select_profile(self, profile_name: str = "Default"):
    """Selects current profile settings folder"""
    self.profile_file = os.path.join(SETTINGS_REL_DIR, profile_name + '.json')

  @logFunc(inclass=True)
  def load(self, key: str) -> Any:
    """Loads the value of a single setting key"""
    return self.current_settings.__dict__[key]

  @logFunc(inclass=True)
  def save(self, key: str, value: Any):
    """Updates a single setting value"""
    self.current_settings.__dict__[key] = value
    self.save_all(self.current_settings)

  def load_all(self) -> AppSettings:
    """Loads application settings from a Pickle file."""
    self.save_all()
    if not os.path.exists(self.profile_file):
      self.save_all()
    else:
      with open(self.profile_file, "r") as f:
        return AppSettings(json.load(f))         

  def save_all(self, settings: AppSettings = None):
    """Saves application settings to pickle file"""
    if not (settings):
      settings = AppSettings()
    if not os.path.exists(SETTINGS_REL_DIR):
      os.makedirs(SETTINGS_REL_DIR)
    settings = vars(settings)
    with open(self.profile_file, "w") as f:
      json.dump(settings, f)

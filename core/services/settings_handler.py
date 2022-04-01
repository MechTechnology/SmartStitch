import json
import os
from core.utils.constants import SETTINGS_REL_DIR
from core.models.app_settings import AppSettings
from core.services.global_logger import logFunc


class SettingsHandler():
  def __init__(self, profile_name: str = "Default"):
    self.settings_file = os.path.join(SETTINGS_REL_DIR, 'settings.json')
    self.current_settings = self.load_all()
  
  @logFunc(inclass=True)
  def load(self, key: str) -> any:
    """Loads the value of a single setting key"""
    return self.current_settings.__dict__[key]

  @logFunc(inclass=True)
  def save(self, key: str, value: any):
    """Updates a single setting value"""
    self.current_settings.__dict__[key] = value
    self.save_all(self.current_settings)

  def load_all(self) -> AppSettings:
    """Loads application settings from a json file."""
    if not os.path.exists(self.settings_file):
      return self.save_all()
    else:
      with open(self.settings_file, "r") as f:
        return AppSettings(json.load(f))         

  def save_all(self, settings: AppSettings = None) -> AppSettings:
    """Saves application settings to a json file"""
    if not (settings):
      settings = AppSettings()
    with open(self.settings_file, "w") as f:
      json.dump(vars(settings), f, indent=2)
    return settings
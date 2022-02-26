import pickle
from os import path
from typing import Any
from core.models.app_settings import AppSettings

class SettingsHandler():
  def __init__(self):
    self.current_settings = self.load_all()

  def load(self, key: str) -> Any:
    """Loads the value of a single setting key"""
    return self.current_settings.__dict__[key]

  def save(self, key: str, value):
    """Updates a single setting value"""
    self.current_settings.__dict__[key] = value
    self.save_all(self.current_settings)

  def load_all(self) -> AppSettings:
    """Loads application settings from a Pickle file."""
    if not path.exists("settings.pickle"):
      self.save_all()
    else:
      with open("settings.pickle", 'rb') as app_settings_handler:
        return pickle.load(app_settings_handler)

  def save_all(self, settings: AppSettings):
    """Saves application settings to pickle file"""
    if not (settings):
      settings = AppSettings()
    with open("settings.pickle", "wb") as file_handler:
      pickle.dump(settings, file_handler)
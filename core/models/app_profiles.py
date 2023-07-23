from .app_settings import AppSettings

# The class AppProfiles is used to hold pointers to settings profiles.

class AppProfiles:
    """Model for holding Pointers to Settings Profile"""

    def __init__(self, json_dict: dict[str, any] = None):
        # Core Settings
        # Initialize the 'current' attribute to 0.
        self.current: int = 0

        # Initialize the 'profiles' attribute as a list containing a dictionary with the default settings profile.
        # The default settings profile is named "Settings Profile 1" and is created using the vars() function on an instance of the AppSettings class.
        # vars() function returns the __dict__ attribute of an object as a dictionary, essentially converting an object's attributes to a dictionary.
        # The ** operator is used to unpack the dictionary returned by vars() and merge it with the "profile_name" key-value pair.
        # This ensures that the initial profile contains the same attributes as an instance of the AppSettings class, and also includes a custom profile_name.
        self.profiles: list[dict[str, any]] = [
            {"profile_name": "Settings Profile 1", **vars(AppSettings())}
        ]

        # If a JSON dictionary 'json_dict' is provided during initialization, update the instance attributes accordingly.
        if json_dict is not None:
            for key, value in json_dict.items():
                setattr(self, key, value)

# The purpose of this code is to create an AppProfiles object that can hold and manage multiple settings profiles.
# Each settings profile is represented as a dictionary containing the profile_name and the attributes of the AppSettings class.
# The 'current' attribute is used to track the currently active settings profile.
# If a JSON dictionary is provided during initialization, the attributes of the AppProfiles instance are updated based on the keys and values in the JSON dictionary.
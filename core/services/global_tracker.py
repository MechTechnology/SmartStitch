from ..utils.funcs import get_classname_stack, get_funcname_stack, print_tracking
from .global_logger import logFunc

# Main GlobalTracker Class
# This class represents an experimental service based on the Observer Pattern Tracker.
# It is not currently in use and not implemented in the GUI or console.
class GlobalTracker:
    # Array of functions subscribed to this tracker
    subscribers = [print_tracking]

    # Dictionary to store tracked functions and their corresponding values
    tracking_dict = {}

    # Variables to keep track of progress
    process_count = 1
    progress_track = 0
    total_progress = 0

    # Reset the GlobalTracker
    @classmethod
    @logFunc(inclass=True)
    def reset(cls, process_count: int = 1):
        cls.process_count = process_count
        cls.progress_track = 0
        cls.update_total()

    # Add a subscriber function to the tracker
    @classmethod
    @logFunc(inclass=True)
    def add_subscriber(cls, subscriber_func: any):
        cls.subscribers.append(subscriber_func)
        cls.subscribers = list(set(cls.subscribers))
        cls.update_total()

    # Add a function and its value to the tracking dictionary
    @classmethod
    def add_tracking(cls, func_name: str, value: float):
        class_name = get_classname_stack(2)
        if class_name:
            func_name = class_name + '.' + func_name
        cls.tracking_dict[func_name] = value
        cls.update_total()

    # Remove a function and its value from the tracking dictionary
    @classmethod
    def remove_tracking(cls, func_name: str, value: float):
        class_name = get_classname_stack(2)
        if class_name:
            func_name = class_name + '.' + func_name
        cls.tracking_dict.pop(func_name, None)
        cls.update_total()

    # Update the total progress by summing all values in the tracking dictionary
    @classmethod
    def update_total(cls):
        cls.total_progress = 0
        for value in cls.tracking_dict.values():
            cls.total_progress += value

    # Update the progress and notify subscribers
    # This function is not logged to avoid excessive log file spam.
    @classmethod
    def update(cls, message: str = None, fraction: float = 1):
        class_name = get_classname_stack(2)
        func_name = get_funcname_stack(2)
        if class_name:
            func_name = class_name + '.' + func_name
        tracking_details = cls.tracking_dict.get(func_name, None)
        if tracking_details:
            value = (tracking_details * fraction) / cls.process_count
            cls.progress_track += value
            percentage = float(cls.progress_track / cls.total_progress) * 100
            if not message:
                message = func_name + ' ran successfully!'
            for subscriber in cls.subscribers:
                subscriber(percentage, message)
from ..utils.funcs import get_classname_stack, get_funcname_stack, print_tracking
from .global_logger import logFunc

class GlobalTracker:
    # Array of functions subscribed to this tracker
    subscribers = {print_tracking}

    # Dictionary to store tracked functions and their corresponding values
    tracking_dict = {}

    # Variables to keep track of progress
    process_count = 1
    progress_track = 0
    total_progress = 0

    @classmethod
    @logFunc(inclass=True)
    def reset(cls, process_count: int = 1):
        # Reset the GlobalTracker
        cls.process_count = process_count
        cls.progress_track = 0
        cls.update_total()

    @classmethod
    @logFunc(inclass=True)
    def add_subscriber(cls, subscriber_func: any):
        # Add a subscriber function to the tracker
        cls.subscribers.add(subscriber_func)
        cls.update_total()

    @classmethod
    def add_tracking(cls, func_name: str, value: float):
        # Add a function and its value to the tracking dictionary
        class_name = get_classname_stack(2)
        if class_name:
            func_name = f"{class_name}.{func_name}"
        cls.tracking_dict[func_name] = value
        cls.update_total()

    @classmethod
    def remove_tracking(cls, func_name: str, value: float):
        # Remove a function and its value from the tracking dictionary
        class_name = get_classname_stack(2)
        if class_name:
            func_name = f"{class_name}.{func_name}"
        cls.tracking_dict.pop(func_name, None)
        cls.update_total()

    @classmethod
    def update_total(cls):
        # Update the total progress by summing all values in the tracking dictionary
        cls.total_progress = sum(cls.tracking_dict.values())

    @classmethod
    def update(cls, message: str = None, fraction: float = 1):
        # Update the progress and notify subscribers
        # This function is not logged to avoid excessive log file spam.
        class_name = get_classname_stack(2)
        func_name = get_funcname_stack(2)
        if class_name:
            func_name = f"{class_name}.{func_name}"
        tracking_details = cls.tracking_dict.get(func_name)
        if tracking_details:
            value = (tracking_details * fraction) / cls.process_count
            cls.progress_track += value
            percentage = cls.progress_track / cls.total_progress * 100
            if not message:
                message = f"{func_name} ran successfully!"
            for subscriber in cls.subscribers:
                subscriber(percentage, message)

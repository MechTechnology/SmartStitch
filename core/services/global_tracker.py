from core.services.global_logger import logFunc
from core.utils.funcs import get_classname_stack, get_funcname_stack, print_tracking


# Main GlobalTracker Class
class GlobalTracker:
    # Array of functions subscribed on this tracker
    subscribers = [print_tracking]
    # List of function that are being tracked/observed
    tracking_dict = {}
    process_count = 1
    progress_track = 0
    total_process = 0

    @classmethod
    @logFunc(inclass=True)
    def reset(self, process_count: int = 1):
        self.subscribers = [print_tracking]
        self.tracking_dict = {}
        self.process_count = process_count
        self.progress_track = 0
        self.total_process = 0

    @classmethod
    @logFunc(inclass=True)
    def add_subscriber(self, subscriber_func: any):
        self.subscribers.append(subscriber_func)
        self.subscribers = list(set(self.subscribers))

    @classmethod
    def track_func(self, func_name: str, value: float):
        class_name = get_classname_stack(2)
        if class_name:
            func_name = class_name + '.' + func_name
        self.tracking_dict[func_name] = value
        self.total_process = 0
        for value in self.tracking_dict.values():
            self.total_process += value

    # Update & Message funcs is not logged so it does not spam the log file.
    @classmethod
    def update(self, message: str = None, fraction: float = 1):
        class_name = get_classname_stack(2)
        func_name = get_funcname_stack(2)
        if class_name:
            func_name = class_name + '.' + func_name
        tracking_details = self.tracking_dict.get(func_name, None)
        if tracking_details:
            value = (tracking_details * fraction) / self.process_count
            self.progress_track += value
            percentage = float(self.progress_track / self.total_process) * 100
            if not message:
                message = func_name + ' ran sucessfully!'
            for subscriber in self.subscribers:
                subscriber(percentage, message)

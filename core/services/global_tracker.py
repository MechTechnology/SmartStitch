import functools

from core.services.global_logger import logFunc


class Tracker:
    def __init__(self, process_count: int = 1):
        # Array of functions subscribed on this tracker
        self.subscribers = [print]
        # Dict where tracked functions are the keys, and values is a list of track percentage (0), and message (1)
        self.tracking_dict = {}
        self.process_count = process_count
        self.progress_track = 0
        self.total_process = 0

    @logFunc(inclass=True)
    def reset(self, process_count: int = 1):
        self.subscribers = [print]
        self.tracking_dict = {}
        self.process_count = process_count
        self.progress_track = 0
        self.total_process = 0

    @logFunc(inclass=True)
    def addSubscriber(self, subscriber_func: any):
        self.subscribers.append(subscriber_func)
        self.subscribers = list(set(self.subscribers))
        print(self.subscribers)

    @logFunc(inclass=True)
    def addObservedService(self, service_name: str, tracking_details: list):
        self.tracking_dict[service_name] = tracking_details
        self.total_process = 0
        for detail in self.tracking_dict.values():
            self.total_process += float(detail[0])
        print(self.total_process)

    # Update func is not logged so it does not spam the log file.
    def update(self, service_name: str, iterations: int):
        tracking_details = self.tracking_dict.get(service_name, None)
        if tracking_details:
            value = float(tracking_details[0]) / (self.process_count * iterations)
            self.progress_track += value
            for subscriber in self.subscribers:
                subscriber(
                    self.progress_track, '% - ', self.tracking_dict.get(service_name)[1]
                )


def initGlobalTracker():
    global _globalTrackerInstance
    _globalTrackerInstance = Tracker()
    return _globalTrackerInstance


def resetGlobalTracker(process_count: int = 1):
    _globalTrackerInstance.reset(process_count)


def addGlobalSubscriber(subscriber_func: any):
    _globalTrackerInstance.addSubscriber(subscriber_func)


def addGloballyObservedService(service_name: str, tracking_details: list):
    _globalTrackerInstance.addObservedService(service_name, tracking_details)


def trackIterableFunc(service_name: str, iterations: int = 1):
    _globalTrackerInstance.update(service_name, iterations)


def trackFunc(func=None, inclass=False):
    if func is None:
        return functools.partial(trackFunc, inclass=inclass)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        service_name = str(func.__name__)
        if inclass:
            caller_class = type(args[0]).__name__
            service_name = f'{caller_class}.{func.__name__}'
        result = func(*args, **kwargs)
        trackIterableFunc(service_name)
        return result

    return wrapper


initGlobalTracker()

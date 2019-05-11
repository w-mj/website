import datetime
from abc import abstractmethod
import icalendar as ic


class Course:
    def __init__(self):
        self.name = None
        self.id = None
        self.location = None
        self.day = None
        self.stime = None
        self.etime = None
        self.sweek = None
        self.eweek = None

    def get_event(self, first_week):
        event = ic.Event()
        event.add('name', self.name)
        event.add('location', self.location)
        event.add('dtstart', first_week + datetime.timedelta(weeks=self.sweek, days=self.day) + self.stime)
        event.add('dtend', first_week + datetime.timedelta(weeks=self.sweek, days=self.day) + self.etime)
        event.add('rrule', {'freq': 'weekly', 'until':
            first_week + datetime.timedelta(weeks=self.eweek, days=self.day) + self.etime})
        return event


class Schedule:
    def __init__(self):
        self.course_list = []
        self.first_week = None

    @abstractmethod
    def update(self, **kwargs):
        pass

    def get_calendar(self):
        calendar = ic.Calendar()
        for c in self.course_list:
            calendar.add_component(c.get_event(self.first_week))
        return calendar

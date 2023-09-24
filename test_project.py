from tracker import Tracker, get_all_tracker_names
from db import get_db, create_tables, get_all_habits, get_all_daily_habits
from timespan import TimeSpan

class TestTracker:

    def setup_method(self):
        self.db = get_db()
        self.cur = self.db.cursor()


    def test_create_tracker_instance(self):
        tracker = Tracker('test')
        assert tracker.name == 'test'

    def test_get_all_tracker_names(self):
        assert "test" in get_all_tracker_names(self.cur)

class TestDB:

    def setup_method(self):
        self.db = get_db()
        self.cur = self.db.cursor()

    def test_get_all_habits(self):
        assert len(get_all_habits('test')) == 10

    def test_get_all_daily_habits(self):
        assert len(get_all_daily_habits('test')) == 5

class TestTimeSpan:

    def test_create_timespan_instance(self):
        timespan = TimeSpan(1)
        assert timespan.span == 1
        assert str(timespan) == 'daily'
        timespan = TimeSpan(7)
        assert timespan.span == 7
        assert str(timespan) == 'weekly'


from datetime import datetime
import json

from public import db


class AttrDict(dict):
    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __getattr__(self, item):
        return self.__getitem__(item)

    def __delattr__(self, item):
        self.__delitem__(item)


def json_response(data='', message=''):
    if message:
        return json.dumps({'data': '', 'message': message})
    if isinstance(data, list) and all([hasattr(x, 'to_json') for x in data]):
        data = [x.to_json() for x in data]
    elif isinstance(data, db.Model) and hasattr(data, 'to_json'):
        data = data.to_json()
    return json.dumps({'data': data, 'message': message or ''})


def human_time(date=None):
    if date:
        assert isinstance(date, datetime)
    else:
        date = datetime.now()
    return date.strftime('%Y-%m-%d %H:%M:%S')


def human_diff_time(time1, time2):
    if not (isinstance(time1, datetime) and isinstance(time2, datetime)):
        raise TypeError('Expect a datetime.datetime value')
    delta = time1 - time2 if time1 > time2 else time2 - time1
    if delta.seconds < 60:
        text = '%d秒' % delta.seconds
    elif delta.seconds < 3600:
        text = '%d分' % (delta.seconds / 60)
    else:
        text = '%d小时' % (delta.seconds / 3600)
    return '%d天%s' % (delta.days, text) if delta.days else text

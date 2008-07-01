import datetime, time, calendar

def tupletodatetime(tuple):
  """translate tuple to datetime object"""
  return datetime.datetime.utcfromtimestamp(calendar.timegm(tuple))
  
def datetimetotuple(dt):
  """translate datetimeobject to tuple"""
  return dt.timetuple()
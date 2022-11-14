from datetime import datetime
from datetime import date
# time(hour = 0, minute = 0, second = 0)
today = date.today()
a = datetime(today.year,today.month, today.day, 12, 0, 0)
print(a)

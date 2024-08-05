from datetime import datetime, timedelta

d=datetime(867,1,2)
d=d+timedelta(days=400)
print(d.strftime("%Y-%m-%d %H:%M:%S"),d.year)

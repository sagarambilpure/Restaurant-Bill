import datetime
def get_day(d1):
	d2=d1.isoweekday()
	if d2==1:
		return "mon"
	elif d2==2:
		return "tue"
	elif d2==3:
		return "wed"	
	elif d2==4:
		return "thu"
	elif d2==5:
		return "fri"
	elif d2==6:
		return "sat"
	elif d2==7:
		return "sun"
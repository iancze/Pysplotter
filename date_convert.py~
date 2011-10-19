#!/usr/bin/python
#Date Convert

'''Date convert is a command-line tool designed to aid in the conversion of 
astronomical dates. It can also be imported and its functions used.'''

import datetime

MJD_0 = datetime.datetime(1858,11,17)
print(MJD_0)

def MJD_to_UT(MJD):
	UT_date = MJD_0 + datetime.timedelta(MJD)
	print(UT_date)
	print("%s %.2f UT" % (UT_date.strftime("%Y %B"),get_decimal_day(UT_date)))
	print()
	
	return UT_date
	
	
def get_decimal_day(my_datetime):
	dec_day = my_datetime.day + my_datetime.hour/24.0 + my_datetime.minute/(24.*60.) + \
		my_datetime.second/(24.0*3600.)
	print("%s %.2f UT" % (my_datetime.strftime("%Y %B"),dec_day))
	return dec_day
	
if __name__=="__main__":
	print("upper limit")
	MJD_to_UT(55220.74)
	print("LT obs started")
	MJD_to_UT(55233.98)
	#HET
	date0 = datetime.datetime(2010,2,7,7,14)
	#NOT
	date1 = datetime.datetime(2010,2,12,4,57)
	#GMOS
	date3 = datetime.datetime(2010,2,21,13,36)
	get_decimal_day(date0)
	get_decimal_day(date1)
	get_decimal_day(date3)

	
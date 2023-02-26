#¡/usr/bin/env python3

import csv
import time
from datetime import datetime, timedelta, date

wh={} # { 'yyyy-mm-dd' : { 'Start':'yyyy-mm-dd hh:mm:ss', 'End':'yyyy-mm-dd hh:mm:ss'  }}
dt={} # {  x : { 'Start':yyyy-mm-dd hh:mm:ss, 'End':yyyy-mm-dd hh:mm:ss, 'Monitor':'text', 'DurationWH':yyyy-mm-dd hh:mm:ss }}
wh_filename = "WorkingHours5.csv"
data_filename = "Outage Report_testdata_02.csv"
new_filename = 'New'+data_filename

def to_time( time_str ):
    return datetime.strptime( time_str, "%Y-%m-%d %H:%M:%S" )

def read_working(): # Read Working Hours lookup file into wh{}
    with open( wh_filename ) as wh_file_data:
        wh_file = csv.DictReader( wh_file_data )
        for row in wh_file:
            key = to_time( row['Date'] )
            key = str( key.date() )
            wh.update( { key : { 'Start':row['Start'], 'End':row['End'] }} )
            #print( wh[key] )

def read_data(): # Read ourage report Data file into dt{}
    with open( data_filename ) as data_file_data:
        data_file = csv.DictReader( data_file_data )
        x = 1
        for row in data_file: # Monitor Name,Start Time,End Time,Duration
            dt.update( { x: { 'Start Time':row['Start Time'], 'End Time':row['End Time'], 'Monitor':row['Monitor Name'] } } )
            #print( dt[x])
            x += 1

def write_data(): # Write ourage report Data file into dt{}
    with open( new_filename, 'w' ) as new_file_data:
        line = 'Monitor, Start Time, End Time, Total Secs, Working Secs'
        new_file_data.write( line+'\n' )
        for key, row in dt.items():
            wsec = str( int( row['Working Hrs'].total_seconds() ) )
            tsec = str( int( row['Total Hrs'].total_seconds() ) )
            line = row['Monitor']+', '+row['Start Time']+', '+row['End Time']+', '+tsec+', '+wsec
            new_file_data.write( line+'\n' )
        new_file_data.close()


def calculate_working():# Iterate dt{} calculating ranges that fall within wh{} lookup table

    def daterange( start_date, end_date ):
        for n in range( int( (end_date - start_date).days+1) ):
            yield start_date + timedelta( n )

    def calc_day( started, ended, work_start, work_end ):# returns timedelta value
        if ended < work_start or started > work_end:
            in_range = timedelta( seconds = 0 )
        else:
            if ended > work_end:
                pinned_end = work_end
            else:
                pinned_end = ended
            if started < work_start:
                pinned_start = work_start
            else:
                pinned_start = started
            in_range = (pinned_end - pinned_start)
        return in_range

    for key, row in dt.items():
        total_in_range = timedelta( seconds = 0 )
        start_time = datetime.strptime( row['Start Time'], "%d %B %Y %H:%M:%S %Z" )
        end_time   = datetime.strptime( row['End Time'], "%d %B %Y %H:%M:%S %Z" )
        total_dt = end_time - start_time
        print( total_dt )
        start_date = start_time.date()
        end_date   = end_time.date()
        print( 'Start time '+str( start_time )+' - End time '+str( end_time ) )
        if start_date == end_date:
                start_work = to_time( wh[ str(start_date) ]['Start'] )
                end_work   = to_time( wh[ str(start_date) ]['End'] )
                #print( ' start work '+str( start_work )+' ...end work '+str( end_work ) )
                total_in_range = calc_day( start_time, end_time, start_work, end_work )
                print( '        total = '+str( total_in_range ) )
        else:
            for a_day in daterange( start_date, end_date ):
                start_work = to_time( wh[ str(a_day) ]['Start'] )
                end_work   = to_time( wh[ str(a_day) ]['End'] )
                in_range   = calc_day( start_time, end_time, start_work, end_work )
                print( '   '+str( a_day )+' = '+str( in_range ) )
                total_in_range = total_in_range + in_range
            print( '        Total = '+str( total_in_range ) )
        row['Working Hrs'] = total_in_range
        row['Total Hrs'] = total_dt
        print( dt[key])
        print('')


if __name__ == '__main__':
    read_working()
    read_data()
    calculate_working()
    write_data()

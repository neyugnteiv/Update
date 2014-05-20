#! /bin/usr/python

import csv, sys, os, time
import json
#import pandas as pd
#import numpy as np
#from pandas import DataFrame as df

def authenticate():
    '''authenticate to appnexus api'''
    return os.system("curl -b cookies -c cookies -X post -d @auth http://api.appnexus.com/auth")


#def to_json(df,filename):
#    '''convert and write pandas dataframe to a json file'''
#    d = {"line-item": 
#        dict([
#            (colname, row[i])
#            for i,colname in enumerate(df.columns)
#        ])
#        for row in df.values
#    }
#    return json.dump(d, open(filename + '.json', 'w'))

def backup_line_item_to_be_replaced(url):
    '''make a copy of the current value in line_item for a specific advertiser.  output to a log file named line_item_backup_log_"date" '''
    file_name = 'backup_log_line_item_%s' % today
    #print time to log
    echo_cmd = "date >> %s" % file_name
    os.system(echo_cmd)
    #line_item url
    cmd_line_item_url = "curl -b cookies -c cookies '%s' >> %s" % (url, file_name)
    return os.system(cmd_line_item_url)
	
def update_line_item(url):
    '''Put json file to appnexus api server to update line_item'''
    put_cmd = "curl -b cookies -c cookies -X put --data-binary @update_file.json '%s'" % (url)
    return os.system(put_cmd)
	
def delete_line_item(url):
    delete_cmd = "curl -b cookies -c cookies -X DELETE --data-binary @update_file.json '%s%'" % (url)
    return os.system(delete_cmd)

#Global Variables:
base_url = 'http://api.appnexus.com/'
today = time.strftime('%Y_%m_%d')

def main():
    if len(sys.argv) >1:
        if sys.argv[1].lower() in ['y', 'yes', 'a', 'auth', 'authenticate']:
            authenticate()

    with open('test.csv', 'rb') as f:
        reader = csv.DictReader(f)
        for line in reader:
            print line
            orig_dict = line
            #remove key with empty string as value
            full_dict = {k: v for k, v in line.items() if v}
            
            dict = full_dict
            adver_id = dict['advertiser_id']
            line_id = dict['line_item_id']
            line_item_url = 'line-item?id=%s&advertiser_id=%s' % (line_id, adver_id)
            url = base_url + line_item_url 
            #do the work
            print 'backing up'
            #backup_line_item_to_be_replaced(url)
            print ' making json'
            d = {"line-item": dict }
            json.dump(d, open('update_file.json', 'w'))
            print 'updating'
            #update_line_item(url)
            #backup_line_item_to_be_replaced(url)
	return 1
	
if __name__ == '__main__':
	main()
    
    
    
#version 1:
#	#Input:
#	data = pd.read_csv("test.csv")
	
#	for i in data.index:
#		df1 = df(data.ix[i,0:]).transpose()
#		adver_id = data.ix[i,1]
#		line_id = data.ix[i,0]
#		line_item_url = 'line-item?id=%s&advertiser_id=%s' % (line_id, adver_id)
#		url = base_url + line_item_url 
#		#do the work
#		print 'backing up'
#		backup_line_item_to_be_replaced(url)	
#		print ' making json'
#		to_json(df1, 'update_file')	
#		print 'updating'
#		#update_line_item(url)
#version 2:
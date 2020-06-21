hash = 'PASTE_HASH_HERE' # Generate hash using zendesk-hash.py
VIEW_ID = 'PASTE_VIEW_ID_HERE' # Obtained from https://analytics.google.com/



from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import re
from time import sleep

import requests
from base64 import b64encode


# ========== REPORTING API ==========

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
# SCOPES = ['https://www.googleapis.com/auth/plus.login']
KEY_FILE_LOCATION = 'client_secrets.json'


def initialize_analyticsreporting():
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, SCOPES)

  # Build the service object.
  analytics = build('analytics', 'v3', credentials=credentials)

  return analytics



def get_report(service):
  	return service.data().realtime().get(
		  ids='ga:'+VIEW_ID,
		  metrics='rt:pageviews',
		  dimensions='rt:pagePath').execute()


def process_pages(results):
  if results.get('rows', []):
    for row in results.get('rows'):
      id = re.search('/hc/(?P<locale>[a-z-]+)/articles/(?P<id>[0-9]+)', row[0])
      if id:
        is_source = zendesk_is_source(id.group('id'), id.group('locale'))
        labels = zendesk_labels(id.group('id'), id.group('locale'))
        # print('\033[1;35m + ' + id.group('id') + '\033[1;32m - ' + id.group('locale') + ' (source? ' + ('✅' if is_source else '❌') + ')\t\033[1;36mtags: ' + ', '.join(labels) + '\033[0m')
        print('\033[1;35m + ' + id.group('id') + '\033[1;32m - ' + id.group('locale') + ' (source? ' + ('✅' if is_source else '❌') + ')\t\033[1;36mtags: ' + ('✅' if labels else '❌') + '\033[0m')
        if not is_source and not labels:
          zendesk_flag(id.group('id'), id.group('locale'))
      else:
      	print('\033[3;31m' + row[0] + '\033[0m')
  else:
    print('No Results Found')


def print_response(results):
  print('**Real-Time Report Response**') 

  print_report_info(results)
  print_query_info(results.get('query'))
  print_profile_info(results.get('profileInfo'))
  print_column_headers(results.get('columnHeaders'))
  print_data_table(results)
  print_totals_for_all_results(results)

def print_data_table(results):
  print('Data Table:')
  # Print headers.
  output = []
  for header in results.get('columnHeaders'):
    output.append('%30s' % header.get('name'))
  print(''.join(output))
  # Print rows.
  if results.get('rows', []):
    for row in results.get('rows'):
      output = []
      for cell in row:
        output.append('%30s' % cell)
      print(''.join(output))
  else:
    print('No Results Found')

def print_column_headers(headers):
  print('Column Headers:')
  for header in headers:
    print('Column name           = %s' % header.get('name'))
    print('Column Type           = %s' % header.get('columnType'))
    print('Column Data Type      = %s' % header.get('dataType'))

def print_query_info(query):
  if query:
    print('Query Info:')
    print('Ids                   = %s' % query.get('ids'))
    print('Metrics:              = %s' % query.get('metrics'))
    print('Dimensions            = %s' % query.get('dimensions'))
    print('Sort                  = %s' % query.get('sort'))
    print('Filters               = %s' % query.get('filters'))
    print('Max results           = %s' % query.get('max-results'))

def print_profile_info(profile_info):
  if profile_info:
    print('Profile Info:')
    print('Account ID            = %s' % profile_info.get('accountId'))
    print('Web Property ID       = %s' % profile_info.get('webPropertyId'))
    print('Profile ID            = %s' % profile_info.get('profileId'))
    print('Profile Name          = %s' % profile_info.get('profileName'))
    print('Table Id              = %s' % profile_info.get('tableId'))

def print_report_info(results):
  print('Kind                    = %s' % results.get('kind'))
  print('ID                      = %s' % results.get('id'))
  print('Self Link               = %s' % results.get('selfLink'))
  print('Total Results           = %s' % results.get('totalResults'))

def print_totals_for_all_results(results):
  totals = results.get('totalsForAllResults')
  for metric_name, metric_total in totals.items():
    print('Metric Name  = %s' % metric_name)
    print('Metric Total = %s' % metric_total)
    
# ========== ZENDESK API ==========
   
zdse = requests.Session()

def zendesk_init():
  zdse.headers = {'Content-Type': 'application/json', 'Authorization': 'Basic ' + hash}

def zendesk_flag(article_id, locale):
  zdse.put('https://memsourcedemo.zendesk.com/api/v2/help_center/articles/'+article_id+'/translations/'+locale+'.json', json={'translation': {'outdated': True}})

def zendesk_labels(article_id, locale):
  labels = zdse.get('https://memsourcedemo.zendesk.com/api/v2/help_center/'+locale+'/articles/'+article_id+'/labels.json').json()
  for e in labels['labels']:
    lang = re.search('PE-(.*)', e['name'])
    if lang and lang.group(1) == locale:
      return True
  return False

def zendesk_is_source(article_id, locale):
  article = zdse.get('https://memsourcedemo.zendesk.com/api/v2/help_center/'+locale+'/articles/'+article_id+'.json').json()
  if locale == article['article']['source_locale']:
    return True
  return False
  
# Start an infinite loop and every ten seconds get and process
# list of pages from Google Analytics that are being visited

def main():
  analytics = initialize_analyticsreporting()
  zendesk_init()
  while True:
    response = get_report(analytics)
    process_pages(response)
    sleep(10)

if __name__ == '__main__':
  main()
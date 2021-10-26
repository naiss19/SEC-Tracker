# Package used to execute HTTP POST request to the API
import json
from sec_api import QueryApi
import requests
import re
import datetime

TOKEN = "ac1226dc2a41838ccf5f3930cb3c3d1a6f4f5f7da9edfcfd8ec0b67f4908244d"

API = "https://api.sec-api.io?token=" + TOKEN


def userMessage():
    datemessage = "Please enter the dates that you want to see. If you want to see up to the present day, \n" \
                  "type NOW for the second date (Example: YYYY-DD-MM, YYYY-DD-MM)\n"
    start = 0
    size = input("How many trades do you want to see?")
    whale = input("Who's trades do you want to see?")

    dateRange = input(datemessage)

    r = re.compile('.*-.*-.*, .*-.*-.*')
    r1 = re.compile('.*-.*-.*, NOW')
    if r.match(dateRange) is not None:

        dateList = dateRange.split(',')
        print("Loading " + size + " trades between " + dateList[0] + " and " + dateList[1])

        return [dateList, start, size, whale]

    elif r1.match(dateRange) is not None:
        now = str(datetime.date.today().year) + "-" + str(datetime.date.today().day) + "-0" +\
              str(datetime.date.today().month)
        dateList = dateRange.split(',')
        dateList[1] = now
        print("Loading " + size + " trades between " + dateList[0] + " and " + dateList[1])
        return [dateList, start, size, whale]
    else:
        dateRange = input(datemessage)


def apiTest(dateList, start, size, whale):
    filter1 = \
        "formType:\"4\" AND formType:(NOT \"N-4\") AND formType:(NOT \"4/A\") AND companyNameLong:" + whale + \
        "(Reporting) AND filedAt:[" + dateList[0] + \
        " TO" + dateList[1] + "]"

    queryApi = QueryApi(api_key=TOKEN)

    query = {
        "query": {"query_string": {
            "query": filter1
        }},
        "from": start,
        "size": size,
        "sort": [{"filedAt": {"order": "desc"}}]
    }
    try:
        filings = queryApi.get_filings(query)

        print(filings)
        return filings

        # print(response.raise_for_status())
    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)

def jsonDateReader():
    with open('../Data Files/congress_stonk.json', 'r') as f:
        data = json.load(f)

    lastEntry = data['total']['value'] - 1
    lastDate = data['filings'][lastEntry]['filedAt']
    newDate = str.split(lastDate, 'T')[0]

    return newDate

def apiDriver():
    dataArray = userMessage()
    jsonSave(dataArray[0])



def jsonSave(data):
    outfile = 'congress_stonk.json'
    with open(outfile, 'w') as f:
        json.dump(data, f, indent=4)

def jsonAppend(data):
    outfile = 'temp.json'
    with open(outfile, 'w') as f:
        json.dump(data, f, indent=4)
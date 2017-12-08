import os
import json
import string
import calendar
import time
from datetime import date
from httplib import *

SINCE=calendar.timegm(date(2011,1,1).timetuple())
UNTIL=calendar.timegm(date(2012,1,1).timetuple())
INTERVAL=86400
TOKEN=''
USER_ID=''
privacy_setting='286958161406148' # only me
BODY=''
COOKIE=''

for cur_since in range(SINCE, UNTIL, INTERVAL):
    print "Starting from "+str(time.gmtime(cur_since))
    conn = HTTPSConnection("graph.facebook.com")
    conn.request("GET", '/'+USER_ID+'/posts?access_token='+TOKEN+'&since='+str(cur_since)+'&until='+str(cur_since+INTERVAL))
    res = conn.getresponse()
    if res.status != 200:
        print "Get postids failed"
        print res.read()
    #print res.read()
    d = json.load(res)

    for dd in d['data']:
        post_id = string.split(dd['id'], '_')[1]
        body = BODY
        header = {
                "cookie": COOKIE,
                "Content-type": "application/x-www-form-urlencoded",
                "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"
                }
        conn2 = HTTPSConnection("www.facebook.com")
        conn2.request("POST", "/privacy/selector/update/?privacy_fbid="+post_id+
                "&post_param="+privacy_setting+
                "&render_location_enum=stream&is_saved_on_select=true&should_return_tooltip=false&prefix_tooltip_with_app_privacy=false&replace_on_select=false&dpr=1&ent_id="+post_id, body, header)
#&render_location_enum=stream&is_saved_on_select=true&should_return_tooltip=false&prefix_tooltip_with_app_privacy=false&replace_on_select=false&ent_id=263543890335672&dpr=1
        res2 = conn2.getresponse()
        print "Setting "+post_id+" result code="+str(res2.status)
        if res2.status != 200 :
            print res2.read()

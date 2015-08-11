import os
import json
import string
from httplib import *
import dateutil.parser
from datetime import *
import pytz
import re

SINCE=1293840000
UNTIL=1325289600
INTERVAL=86400
TOKEN=''
USER_ID=''
privacy_setting='286958161406148' # only me

f = open("post_ids")
for post_id in f:
    post_id=post_id.replace('\n', '')
    print "Dealing with "+post_id
    conn = HTTPSConnection("www.facebook.com")
    header = {
            "cookie": ""
            }
    conn.request("GET", '/<user_id>/posts/'+post_id, '', header)
    res = conn.getresponse()
    resstr = res.read()
    print res.status
    m1 = re.search('data-utime="(\d+)"', resstr)
    update_time = m1.group(0)
    if res.status != 200:
        print "Get postids failed"
    #d = json.load(res)

    #if dateutil.parser.parse(d['updated_time']) > datetime.fromtimestamp(SINCE, pytz.timezone('Asia/Taipei')) and dateutil.parser.parse(d['updated_time']) < datetime.fromtimestamp(UNTIL, pytz.timezone('Asia/Taipei')):
    if datetime.fromtimestamp(update_time, pytz.timezone('Asia/Taipei')) > datetime.fromtimestamp(SINCE, pytz.timezone('Asia/Taipei')) and datetime.fromtimestamp(update_time, pytz.timezone('Asia/Taipei')) < datetime.fromtimestamp(UNTIL, pytz.timezone('Asia/Taipei')):
        body = ''
        header = {
                "cookie": "",
                "Content-type": "application/x-www-form-urlencoded"
                }
        conn2 = HTTPSConnection("www.facebook.com")
        conn2.request("POST", "/privacy/selector/update/?privacy_fbid="+post_id+
                "&post_param="+privacy_setting+
                "&event_expansion_type=0&render_location=1&is_saved_on_select=true&should_return_tooltip=true&prefix_tooltip_with_app_privacy=false&replace_on_select=false&ent_id="+post_id+"&tag_expansion_button=friends_of_tagged", body, header)
        res2 = conn2.getresponse()
        print "Setting "+post_id+" result code="+str(res2.status)
        if res2.status != 200 :
            print res2.read()
    else:
        print post_id+" not in time range"

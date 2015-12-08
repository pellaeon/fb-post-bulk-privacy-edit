import os
import json
import string
from httplib import *

SINCE=1293840000
UNTIL=1325289600
INTERVAL=86400
TOKEN=''
USER_ID=''
privacy_setting='286958161406148' # only me
BODY=''
COOKIE=''

for cur_since in range(SINCE, UNTIL, INTERVAL):
    print "Starting from "+str(cur_since)
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

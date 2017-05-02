import os
import json
import string
from httplib import *
# Exit if error
import sys
import datetime

# Timestamp example since: 1288137600 and until: 1493596800 get in: http://www.convert-unix-time.com/
SINCE=1288137600
UNTIL=1493596800
INTERVAL=86400

# Get in: https://developers.facebook.com/tools/explorer/ and set user_posts permission
TOKEN='RANDOM-NUMBER' 
USER_ID='YOUR-ID'

# Default Only me
privacy_setting='286958161406148'

# Get body and cookie in https://www.facebook.com/YOUR-USERNAME/posts/ANY-POST-ID, in  browser [Chrome] open Developer Tools > Network tab, select XHR type. Reload page and change post privacy, find "?privacy_fbid=..." in the list and copy COOKIE in Request Headers, in Form Data click in View source and copy all BODY param.
BODY='__user=RANDOM&__a=1&__dyn=RANDOM-NUMBER-qiU&__af=iw&__req=b&__be=-1&__pc=PHASED%3ADEFAULT&__rev=RANDOM&fb_dtsg=AQFNgqWPlQy6RANDOM&logging=RANDOM&ft[top_level_post_id]=RANDOM&ft[tl_objid]=RANDOM&ft[throwback_story_fbid]=RANDOM&ft[fbfeed_location]=5' # Like this
COOKIE='disabled2=yes; datr=RANDOM-NUMBER; dats=1; locale=pt_BR; sb=RANDOM-NUMBER; pl=n; lu=RANDOM-NUMBER; c_user=RANDOM-NUMBER; xs=RANDOM-NUMBER; fr=RANDOM-NUMBER; act=RANDOM-NUMBER; presence=RANDOM-NUMBER; wd=RANDOM-NUMBER' # Like this

print ''
print "[[Facebook bulk post privacy change]]"
for cur_since in range(SINCE, UNTIL, INTERVAL):
    print ''
    print "Starting date: " + '\x1b[6;30;42m' + (datetime.datetime.fromtimestamp(int(cur_since)).strftime('%d-%m-%Y')) + '\x1b[0m'
    print ''
    # Update api url to v2.9
    conn = HTTPSConnection("graph.facebook.com")
    conn.request("GET", '/v2.9/'+USER_ID+'/posts?access_token='+TOKEN+'&since='+str(cur_since)+'&until='+str(cur_since+INTERVAL))
    res = conn.getresponse()
    if res.status != 200:
        print "Get postids failed, check your connection or if your token is expired!"
        sys.exit(0) # Show error message and exit
    d = json.load(res)

    for dd in d['data']:
        post_id = string.split(dd['id'], '_')[1]
        body = BODY
        header = {
                "cookie": COOKIE,
                "Content-type": "application/x-www-form-urlencoded",
                "user-agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
                }
        conn2 = HTTPSConnection("www.facebook.com")
        conn2.request("POST", "/privacy/selector/update/?privacy_fbid="+post_id+"&post_param="+privacy_setting+"&render_location=1&is_saved_on_select=true&should_return_tooltip=false&prefix_tooltip_with_app_privacy=false&replace_on_select=false&ent_id="+post_id+"&dpr=1", body, header) # Updateded request url, working now!

        res2 = conn2.getresponse()
        print "Setting post_id " + '\x1b[6;30;47m' + post_id  + '\x1b[0m' + ", HTTP Status >> " + '\x1b[6;30;42m' + "[" + str(res2.status) + "]" + '\x1b[0m'

        if res2.status != 200 :
            #print res2.read()
            print "HTTP response not OK :(" 


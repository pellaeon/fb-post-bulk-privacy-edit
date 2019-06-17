#https://github.com/pellaeon/fb-post-bulk-privacy-edit #project repository
#https://findmyfbid.com/ #this is obsolete except for verifying that BODY variable is pointing to the correct FB user.
#Before running this script, run the GetLongLivedUserAccessToken.py script (according to its documented instructions) 
# to get the TOKEN and APP_SCOPED_USER_ID values for this script.
#https://developers.facebook.com/docs/facebook-login/access-tokens/refreshing/ #Explains how to refresh a long-lived user access token by regerenerating it based on a server-side long-lived user access token. #Mostly tangential but related to the auth logic used here.
#https://developers.facebook.com/tools/debug/accesstoken/ #Debug user access tokens here
#https://developers.facebook.com/apps/2329833357263890/dashboard/ #where you will see warnings about API request limits.
#https://developers.facebook.com/docs/graph-api/reference/v3.3/user/feed #docs on the 'posts' method (distinct from page posts)
import os
import json
import string
import calendar
import time
from datetime import date
from datetime import datetime
from httplib import *
#These dates are GMT, so they will not likely match your post time unless you are in the GMT/UTC time zone. 
SINCE=calendar.timegm(date(2011,11,1).timetuple())
UNTIL=calendar.timegm(date(2011,11,30).timetuple())
#Notes: Facebook appears to return data starting from the UNTIL date in reverse sort order. 
#It presumes that you want to see the most recent data first. This is why it is simplest to keep the 1 day interval.
#There is paging information available, but this script does not handle paging (yet).
#Therefore, it is recommended that you limit the date range in combination with the INTERVAL accordingly. 
#The reason for increasing the interval is to reduce the number of API requests.
#A useful way of testing the script is to use the new Manage Posts button on your Facebook profile. 
#URL Pattern: https://www.facebook.com/{usernamestring}/grid?lst=100002979822789%3A100002979822789%3A1560719298 
INTERVAL=86400*1 #multiplier is the number of days that are in the request batch. Make sure it fits your date range neatly. 
#Your FB user's API access token for your app (created above)
TOKEN=''
#Your FB app user id
APP_SCOPED_USER_ID=''
#Your FBUSERID - official - this no longer works
#APP_SCOPED_USER_ID ='' 
privacy_setting='286958161406148' # only me
BODY='' #Fill this in according to README.md
COOKIE='' #Fill this in according to README.md

for cur_since in range(SINCE, UNTIL, INTERVAL):
    print "Starting from "+str(time.gmtime(cur_since))
    SINCEDT = date.fromtimestamp(cur_since)
    UNTILDT = date.fromtimestamp(cur_since+INTERVAL)

    conn = HTTPSConnection("graph.facebook.com")
    conn.request("GET", '/v3.3/'+APP_SCOPED_USER_ID+'/posts?since='+str(cur_since)+'&transport=cors&until='+str(cur_since+INTERVAL)+'&access_token='+TOKEN)

    res = conn.getresponse()
    if res.status != 200:
        print "Get postids failed"
        print res.read()

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
        res2 = conn2.getresponse()
        print "Setting "+post_id+" ("+str(dd['created_time'])+") result code="+str(res2.status)
        if res2.status != 200 and res2.status != 500:
            print "*********************************"
            print "Error: " + res2.read()
            print "*********************************"
        elif res2.status == 500:
            print "Error (Unexpected): Sorry, something went wrong."
            #print "Error: " + res2.read()

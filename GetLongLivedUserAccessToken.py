#1) Get a long-lived (3 months long) user access token for your facebook profile
#2) Get your App-scoped User ID
#3) Get permanent page access tokens, if you have the manage_pages privilege.
#Adapted from https://dev.to/chorally/permanent-facebook-page-access-token-3epi
#https://developers.facebook.com/tools/explorer #you need to create an app and begin your Facebook developer journey. Here you request the user access token for the app you are testing with.
#https://www.facebook.com/settings?tab=applications #to find your app and open it's basic settings to see the AppID. If your app is missing from this list then it is not yet active on your account (has not been installed).
#https://developers.facebook.com/apps/{appid}/settings/basic/ #to retrieve your AppID and AppSecret.
#If you want to perform step #3, make sure that the token has the manage_pages privilege.
#Request the short-lived user access token for the app you are testing with and set the USER_ACCESS_TOKEN variable below.
#Get value for USER_ACCESS_TOKEN here: https://developers.facebook.com/tools/explorer 
#Debug user access tokens here: https://developers.facebook.com/tools/debug/accesstoken/
import os
import json
import string
import calendar
import time
from datetime import date
from datetime import datetime
from httplib import *
APP_ID = '' #Fill this in
APP_SECRET = '' #Fill this in
USER_ACCESS_TOKEN = '' #Fill this in
LONG_USER_ACCESS_TOKEN = '' #1 result
APP_SCOPED_USER_ID = '' #2 result

# 1 Generate Long-Lived Access Token
conn = HTTPSConnection("graph.facebook.com")
conn.request("GET", '/v3.3/oauth/access_token?grant_type=fb_exchange_token&client_id='+APP_ID+'&client_secret='+APP_SECRET+'&fb_exchange_token='+USER_ACCESS_TOKEN)
res = conn.getresponse()
if res.status != 200:
    print "GET long-lived access_token failed"
    print res.read()
else:
    d = json.load(res)
    LONG_USER_ACCESS_TOKEN = d['access_token']
    print 'Long-lived user access token = ' + LONG_USER_ACCESS_TOKEN
    #Continue only if you need page access tokens for the Facebook pages that this user manages.
    # 2 Get User ID
    conn.request("GET", '/v3.3/me?access_token='+LONG_USER_ACCESS_TOKEN)
    res = conn.getresponse()
    if res.status != 200:
        print "GET user id failed"
        print res.read()
    else:
        d = json.load(res)
        APP_SCOPED_USER_ID = d['id']
        print 'App USER ID = ' + APP_SCOPED_USER_ID
        # 3 Get Permanent Page Access Token
        #conn.request("GET", '/v3.3/'+APP_SCOPED_USER_ID+'/accounts?access_token='+LONG_USER_ACCESS_TOKEN)
        #res = conn.getresponse()
        #if res.status != 200:
            #print "GET permanent user access token failed"
            #print res.read()
        #else:
            #d = json.load(res)
            #print 'Permanent User Access Tokens for pages = ' + str(d['data'])



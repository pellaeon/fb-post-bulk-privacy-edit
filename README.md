## Introduction
#### Updated and tested: 01/05/2017

**Warning: this is a super hacky proof of concept project that contains a lot of dirty and badly written code, but hey, it works for me.**

Facebook has a tool in settings page, it can bulk modify post privacy settings for old posts, the tool is called "Limit old posts".

However, the tool can only modify posts that are shared with "Public" or "Friends of friends". So my script attempts to solve this problem.

## How it works

Facebook Graph API does not offer a way to modify post privacy settings, so my script needs you to steal cookies from a logged in browser, and send resuests emulating the browser to modify post privacy settings.

## ~~process.py~~ bulk-privacy.py
##### Tested on **Python 2.7.13**

This script first uses Graph API to grab all post ID's from a specific timeframe, then emulate browser requests to each of them.

However, I found that the wacky [Graph API /user_id/posts endpoint does not actually show all posts](https://stackoverflow.com/questions/7659701/facebook-graph-api-json-missing-posts), so there needs to be another way to grab all post IDs.

### Parameters:
`TOKEN`: a valid Facebook OAuth client token that is authorized to read your own timeline, you can go to [Facebook Graph API Explorer](https://developers.facebook.com/tools/explorer), authorize it, and copy its token here.

`privacy_setting`: target privacy setting you wish to set. You can use `286958161406148` for "Only me". To use other values, open your browser developer console's network tab, then change privacy setting to what you want (Friends, Public, Custom list, etc) for an arbitrary post, monitor the dev console for xhr POST request to `/privacy/selector/update/`, inside the request HTTP query strings, `post_param` is the id for that privacy setting. Set this `privacy_setting` to the privacy setting id you want to use.

`BODY`: also from the request intercepted above, copy the request body here. It usually starts with `__user=....`.

`COOKIE`: steal cookies also from that intercepted request, you can find it in `cookie` request header.

	python bulk-privacy.py

_Note: Comments in code file._

## ~~process_from_ids.py~~ (DEPRECATED)

~~One way to grab all post IDs is:~~

~~1. Open your profile page on a browser~~
~~2. Find something small and heavy to keep your `End` key (`Fn+Down` for Mac) pressed down~~
~~3. Go to lunch~~
~~4. In the browser, save the page~~
~~5. Use the following command to get all post IDs that is on the saved HTML page:~~

	egrep -oh 'top_level_post_id&quot;:&quot;(\d+)&quot;' Your_page.html | cut -c 31-45

~~6. Save post IDs to a file `post_ids`~~

~~Then, `process_from_ids.py` can read post IDs from that file and modify privacy settings for them.~~

~~_Note: maybe later I can use Casperjs to grab the post IDs, maybe even get cookie by emulating login on Casperjs_~~

### Forked in
Thanks [@pellaeon](https://github.com/pellaeon) for the original code [/fb-post-bulk-privacy-edit](https://github.com/pellaeon/fb-post-bulk-privacy-edit)

## License
AGPLv3

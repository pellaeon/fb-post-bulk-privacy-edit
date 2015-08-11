## Introduction

**Warning: this is a super hacky proof of concept project that contains a lot of dirty and badly written code, but hey, it works for me.**

Facebook has a tool in settings page, it can bulk modify post privacy settings for old posts, the tool is called "Limit old posts".

However, the tool can only modify posts that are shared with "Public" or "Friends of friends". So my script attempts to solve this problem.

## How it works

Facebook Graph API does not offer a way to modify post privacy settings, so my script needs you to steal cookies from a logged in browser, and send resuests emulating the browser to modify post privacy settings.

## process.py

This script first uses Graph API to grab all post ID's from a specific timeframe, then emulate browser requests to each of them.

However, I found that the wacky [Graph API /<user_id>/posts endpoint does not actually show all posts](https://stackoverflow.com/questions/7659701/facebook-graph-api-json-missing-posts), so there needs to be another way to grab all post IDs.

## process_from_ids.py

One way to grab all post IDs is:
1. Open your profile page on a browser
2. Find something small and heavy to keep your `End` key (`Fn+Down` for Mac) pressed down
3. Go to lunch
4. In the browser, save the page
5. Use the following command to get all post IDs that is on the saved HTML page:

	egrep -oh 'top_level_post_id&quot;:&quot;(\d+)&quot;' Your_page.html | cut -c 31-45

6. Save post IDs to a file `post_ids`

Then, `process_from_ids.py` can read post IDs from that file and modify privacy settings for them.

_Note: maybe later I can use Casperjs to grab the post IDs, maybe even get cookie by emulating login on Casperjs_

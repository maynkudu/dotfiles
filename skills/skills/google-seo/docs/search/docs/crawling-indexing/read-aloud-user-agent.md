# Google Read Aloud user agent


[`Google-Read-Aloud`](https://developers.google.com/search/docs/crawling-indexing/google-user-triggered-fetchers#google-read-aloud)
is the user agent for the Google Read Aloud service. This service provides an audio version of web
pages by understanding their content through help of AI (no data from the page is retained for AI model training),
and using text-to-speech (TTS) technology.
This service is activated when an end user has TTS enabled and visits a
page. The Read Aloud service is used by Google Chrome on Android, Google app on Android, [Google app on IOS](https://support.google.com/websearch/answer/10078840), [Google Go](https://www.blog.google/technology/next-billion-users/make-google-read-it/),
[Google Read it](https://developers.google.com/assistant/app/read-it), and other Google text-to-speech services.

## Crawl frequency and behavior


Google Read Aloud is triggered by a user request. Google Read Aloud conserves bandwidth by
caching page results, but you may still see multiple requests for a given page.


Google Read Aloud is not a web crawler: it is activated upon user request, and it doesn't follow
links. A user request for listening to a web page may or may not result in page visits, depending
on whether the page has been fetched recently.

## Prevent Google Read Aloud from accessing your content


Since Google Read Aloud is initiated by a user, not a result of automated web crawl, you can't opt
out by using a robots.txt file. To opt out of Google Read Aloud completely, use the
`nopagereadaloud` `meta` tag:  

```text
<meta name="google" content="nopagereadaloud">
```


To prevent paywalled content from being read aloud, use
[structured data for subscription and paywalled content](https://developers.google.com/search/docs/appearance/structured-data/paywalled-content).
Make sure the `isAccessibleForFree` property is set to `False`.

## What is the `google-speakr` agent?


The `google-speakr` agent is an older, deprecated version of the user agent. The user
agent's current name is `Google-Read-Aloud`.

# List of Google user-triggered fetchers

User-triggered fetchers are initiated by users to perform a fetching function within a Google product. For example,[Google Site Verifier](https://support.google.com/webmasters/answer/9008080)acts on a user's request, or a site hosted on Google Cloud (GCP) has a feature that allows the site's users to retrieve an external RSS feed. Because the fetch was requested by a user, these fetchers generally ignore robots.txt rules. The general[technical properties](https://developers.google.com/search/docs/crawling-indexing/overview-google-crawlers#crawl-technical-props)of Google's crawlers also apply to the user-triggered fetchers.

The IP ranges the user-triggered fetchers use are published in the[user-triggered-fetchers.json](https://developers.google.com/static/search/apis/ipranges/user-triggered-fetchers.json)and[user-triggered-fetchers-google.json](https://developers.google.com/static/search/apis/ipranges/user-triggered-fetchers-google.json)objects. The user-triggered fetchers' reverse DNS mask, depending on whether the fetcher is Google or user owned, matches`***-***-***-***.gae.googleusercontent.com`or`google-proxy-***-***-***-***.google.com`respectively.

The following list shows the user-triggered fetchers, their user agent strings as they appear in the HTTP requests, and the products they are associated with. The list is not exhaustive, it only covers the requestors that are more likely to show up in log files and that we've received questions about.
| **Caution** : The user agent string can be spoofed.[Learn how to verify if a visitor is a Google crawler](https://developers.google.com/search/docs/crawling-indexing/verifying-googlebot).

## Chrome Web Store

:

    |---------------------------------|---------------------------------------------------------------------------------------------------------------------------|
    | **User-Agent in HTTP requests** | ``` Mozilla/5.0 (compatible; Google-CWS) ```                                                                              |
    | **Associated products**         | The Chrome Web Store fetcher requests URLs that developers provide in the metadata of their Chrome extensions and themes. |

## [Feedfetcher](https://developers.google.com/search/docs/crawling-indexing/feedfetcher)

:

    |---------------------------------|--------------------------------------------------------------------------------------|
    | **User-Agent in HTTP requests** | ``` FeedFetcher-Google; (+http://www.google.com/feedfetcher.html) ```                |
    | **Associated products**         | Feedfetcher is used for crawling RSS or Atom feeds for Google News and PubSubHubbub. |

## Google NotebookLM

:

    |---------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **User-Agent in HTTP requests** | ``` Google-NotebookLM ```                                                                                                                             |
    | **Associated products**         | The`Google-NotebookLM`fetcher requests individual URLs that[NotebookLM](https://notebooklm.google/)users have provided as sources for their projects. |

## Google Pinpoint

:

    |---------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **User-Agent in HTTP requests** | ``` Google-Pinpoint ```                                                                                                                                                                         |
    | **Associated products**         | The`Google-Pinpoint`fetcher requests individual URLs that[Pinpoint](https://support.google.com/pinpoint/answer/11948320)users specified as sources for their personal collections of documents. |

## Google Publisher Center

:

    |---------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **User-Agent in HTTP requests** | ``` GoogleProducer; (+https://developers.google.com/search/docs/crawling-indexing/google-producer) ```                                                                                         |
    | **Associated products**         | Google Publisher Center fetches and processes[feeds that publishers explicitly supplied](https://support.google.com/news/publisher-center/answer/9545414)for use in Google News landing pages. |

## [Google Read Aloud](https://developers.google.com/search/docs/crawling-indexing/read-aloud-user-agent)

:

    |---------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **User-Agent in HTTP requests** | |---------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| | Mobile agent              | ``` Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36 (compatible; Google-Read-Aloud; +https://support.google.com/webmasters/answer/1061943) ``` | | Desktop agent             | ``` Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 (compatible; Google-Read-Aloud; +https://support.google.com/webmasters/answer/1061943) ```           | | Former agent (deprecated) | `google-speakr`                                                                                                                                                                                                | |
    | **Associated products**         | Upon user request, Google Read Aloud[fetches and reads out web pages using text-to-speech (TTS)](https://developers.google.com/search/docs/crawling-indexing/read-aloud-user-agent).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |

## [Google Site Verifier](https://support.google.com/webmasters/answer/9008080)

:

    |---------------------------------|------------------------------------------------------------------|
    | **User-Agent in HTTP requests** | ``` Mozilla/5.0 (compatible; Google-Site-Verification/1.0) ```   |
    | **Associated products**         | Google Site Verifier fetches Search Console verification tokens. |

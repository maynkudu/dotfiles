# Large site owner's guide to managing your crawl budget


This guide describes how to optimize Google's crawling of very large and frequently updated
sites.


If your site does not have a large number of pages that change rapidly, or if your pages seem
to be crawled the same day that they are published, you don't need to read this guide; merely
[keeping your sitemap up to date](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap) and
[checking your index coverage](https://support.google.com/webmasters/answer/7440203)
regularly is adequate.


If you have content that's been available for a while but has never been indexed, this is a
different problem; use the
[URL Inspection tool](https://support.google.com/webmasters/answer/9012289)
instead to find out why your page isn't being indexed.

## Who this guide is for

This is an advanced guide and is intended for:

- Large sites (1 million+ unique pages) with content that changes moderately often (once a week)
- Medium or larger sites (10,000+ unique pages) with very rapidly changing content (daily)
- Sites with a large portion of their total URLs classified by Search Console as [Discovered - currently not indexed](https://support.google.com/webmasters/answer/7440203#information-status)

| The numbers given here are a **rough estimate** to help you classify your site. These are not exact thresholds.

## General theory of crawling

The web is a nearly infinite space, exceeding Google's ability to explore and index every
available URL. As a result, there are limits to how much time Googlebot can spend crawling any
single site. The amount of time and resources that Google devotes to crawling a site is
commonly called the site's *crawl budget* . Note that not everything *crawled* on
your site will necessarily be *indexed* ; each page must be evaluated,
[consolidated](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls), and
assessed to determine whether it will be indexed after it has been crawled.

Crawl budget is determined by two main elements: *crawl capacity limit* and *crawl
demand*.

### Crawl capacity limit

Googlebot wants to crawl your site without overwhelming your servers. To prevent this,
Googlebot calculates a *crawl capacity limit*, which is the maximum number of
simultaneous parallel connections that Googlebot can use to crawl a site, as well as the time
delay between fetches. This is calculated to provide coverage of all your important content
without overloading your servers.

The crawl capacity limit can go up and down based on a few factors:

- **Crawl health:** If the site responds quickly for a while, the limit goes up, meaning more connections can be used to crawl. If the site slows down or responds with server errors, the limit goes down and Googlebot crawls less.
- **Google's crawling limits**: Google has a lot of machines, but not infinite machines. We still need to make choices with the resources that we have.

### Crawl demand

Google typically spends as much time as necessary crawling a site, given its size, update
frequency, page quality, and relevance, compared to other sites.

The factors that play a significant role in determining crawl demand are:

- **Perceived inventory:** Without guidance from you, Googlebot will try to crawl all or most of the URLs that it knows about on your site. If many of these URLs are duplicates, or you don't want them crawled for some other reason (removed, unimportant, and so on), this wastes a lot of Google crawling time on your site. This is the factor that you can positively control the most.
- **Popularity:** URLs that are more popular on the Internet tend to be crawled more often to keep them fresher in our index.
- **Staleness:** Our systems want to recrawl documents frequently enough to pick up any changes.

Additionally, site-wide events like site moves may trigger an increase in crawl demand in
order to reindex the content under the new URLs.

### In sum

Taking crawl capacity and crawl demand together, Google defines a site's crawl budget as the
set of URLs that Googlebot can and wants to crawl. Even if the crawl capacity limit isn't
reached, if crawl demand is low, Googlebot will crawl your site less.
| **How do I get more crawl budget?**   
| Google determines the amount of crawling resources to give each site, based on the popularity, user value, uniqueness, and serving capacity. The only ways to increase your crawl budget are to increase your serving capacity for crawls, and (more importantly) to increase the value of the content on your site to searchers.

## Best practices

Follow these best practices to maximize your crawling efficiency:

- **Manage your URL inventory:** Use the appropriate tools to tell Google which pages to crawl and which not to crawl. If Google spends too much time crawling URLs that aren't appropriate for the index, Googlebot might decide that it's not worth the time to look at the rest of your site (or increase your budget to do so).
  - **[Consolidate
    duplicate content](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls).** Eliminate duplicate content to focus crawling on unique content rather than unique URLs.
  - [**Block crawling of URLs using robots.txt**.](https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget#hide_urls) Some pages might be important to users, but you don't necessarily want them to appear in Search results. For example, infinite scrolling pages that duplicate information on linked pages, or differently sorted versions of the same page. If you can't consolidate them as described in the first bullet, block these unimportant (for search) pages using [robots.txt](https://developers.google.com/search/docs/crawling-indexing/robots/create-robots-txt). Blocking URLs with robots.txt significantly decreases the chance the URLs will be indexed. **Don't use `noindex`** , as Google will still request, but then drop the page when it sees a `noindex` `meta` tag or header in the HTTP response, wasting crawling time. **Don't use robots.txt to temporarily reallocate crawl budget** for other pages; use robots.txt to block pages or resources that you don't want Google to crawl at all. Google won't shift this newly available crawl budget to other pages unless Google is already hitting your site's serving limit.
  - **Return a `404` or `410` status code for permanently removed pages.** Google won't forget a URL that it knows about, but a `404` status code is a strong signal not to crawl that URL again. Blocked URLs, however, will stay part of your crawl queue much longer, and will be recrawled when the block is removed.
  - **[Eliminate `soft
    404` errors](https://developers.google.com/search/docs/crawling-indexing/http-network-errors#soft-404-errors).** `soft 404` pages will continue to be crawled, and waste your budget. Check the [Index
    Coverage report](https://support.google.com/webmasters/answer/7440203) for `soft 404` errors.
  - **Keep your sitemaps up to date.** Google reads your sitemap regularly, so be sure to include all the content that you want Google to crawl. If your site includes updated content, we recommend including the `<lastmod>` tag.
  - **Avoid long redirect chains**, which have a negative effect on crawling.
- **[Make your pages efficient to load](https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget#improve_crawl_efficiency).** If Google can load and render your pages faster, we might be able to read more content from your site.
- **[Monitor your site crawling](https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget#monitor_crawling_indexing).** Monitor whether your site had any availability issues during crawling, and look for ways to make your crawling more efficient.

## Monitor your site's crawling and indexing

Here are the key steps to monitoring your site's crawl profile:

1. [See if Googlebot is encountering availability issues on your
   site](https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget#availability_issues).
2. [See whether you have pages that aren't being crawled, but
   should be](https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget#not_crawled_should_be).
3. [See whether any parts of your site need to be crawled more quickly than
   they already are.](https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget#updates)
4. [Improve your site's crawl efficiency.](https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget#improve_crawl_efficiency)
5. [Handle overcrawling of your site](https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget#emergencies).

### See if Googlebot is encountering availability issues on your site

Improving your site availability won't necessarily increase your crawl budget; Google
determines the best crawl rate based on the crawl demand, as described previously. However,
availability issues do prevent Google from crawling your site as much as it might want to.

**Diagnosing:**


Use the [Crawl Stats report](https://support.google.com/webmasters/answer/9679690)
to see Googlebot's crawling history for your site. The report shows when Google encountered
availability issues on your site. If availability errors or warnings are reported for your site,
look for instances in the **Host availability** graphs where Googlebot requests exceeded the
red limit line, click into the graph to see which URLs were failing, and try to correlate
those with issues on your site.


Additionally, you can also use the
[URL Inspection Tool](https://support.google.com/webmasters/answer/9012289)
to test a few URLs on your site. If the tool returns
[**Hostload exceeded**](https://support.google.com/webmasters/answer/9012289#live_indexable&zippy=%2Cadditional-response-data%2Curl-status-live-test%2Csite-wide-availability-issues%2Cavailability-live-test)
warnings, that means that Googlebot can't crawl as many URLs from your site as it discovered.

**Treating:**

- Read the [documentation
  for the Crawl Stats report](https://support.google.com/webmasters/answer/9679690) to learn how to find and handle some availability issues.
- **Block pages from crawling if you don't want them to be crawled.** (See *[manage
  your inventory](https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget#manage_inventory)*)
- **Increase page loading and rendering speed.** (See *[Improve
  your site's crawl efficiency](https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget#improve_crawl_efficiency)*)
- **Increase your server capacity.** If Google consistently seems to be crawling your site at its serving capacity limit, but you still have important URLs that aren't being crawled or updated as much as they need, having more serving resources might enable Google to request more pages on your site. Check your host availability history in the [Crawl Stats
  report](https://support.google.com/webmasters/answer/9679690) to see if Google's crawl rate seems to be crossing the limit line often. If so, increase your serving resources for a month and see whether crawling requests increased during that same period.

### See if any parts of your site are not crawled, but should be

Google spends as much time as necessary on your site in order to index all the high-quality,
user-valuable content that it can find. If you think that Googlebot is missing important
content, either it doesn't know about the content, the content is blocked from Google, or your
site availability is throttling Google's access (or Google is trying not to overload your site).
| Remember the difference between *crawling* and *indexing* . This page is about helping Google *crawl* your site efficiently, not whether the pages found make it into the index.

**Diagnosing:**

Search Console doesn't provide a crawl history for your site that can be filtered by URL or
path, but you can inspect your site logs to see whether specific URLs have been crawled by
[Googlebot](https://developers.google.com/search/docs/crawling-indexing/overview-google-crawlers). Whether or
not those crawled URLs have been indexed is another story.

Remember that for most sites, new pages will take several days minimum to be noticed; most
sites shouldn't expect same-day crawling for URLs, with the exception of time-sensitive sites
such as news sites.

**Treating:**

If you are adding pages to your site and they are not being crawled in a reasonable amount of
time, either Google doesn't know about them, the content is blocked, your site has reached its
maximum serving capacity, or you are [out of crawl budget](https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget#gimme_more_budget).

1. Tell Google about your new pages: update your sitemaps to reflect new URLs.
2. Examine your robots.txt rules to confirm that you're not accidentally blocking pages.
3. Review your crawling priorities (a.k.a. use your crawl budget wisely). [Manage
   your inventory](https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget#manage_inventory) and [improve your site's crawling efficiency](https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget#improve_crawl_efficiency).
4. [Check that you're not running out of serving capacity](https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget#availability_issues). Googlebot will scale back its crawling if it detects that your servers are having trouble responding to crawl requests.

Note that pages might not be shown in search results, even if crawled, if there isn't
sufficient value or user demand for the content.

### See if updates are crawled quickly enough

If we're missing new or updated pages on your site, perhaps it's because we haven't seen them,
or haven't noticed that they are updated. Here is how you can help us be aware of page
updates.

Note that Google strives to check and index pages in a reasonably timely manner. For most
sites, this is three days or more. Don't expect Google to index pages the same day that you
publish them unless you are a news site or have other high-value, extremely time-sensitive
content.

**Diagnosing:**

Examine your site logs to see when specific URLs were crawled by [Googlebot](https://developers.google.com/search/docs/crawling-indexing/overview-google-crawlers).

To learn the indexing date, use the URL Inspection tool or do a Google search for URLs that
you updated.

**Treating:**

**Do:**

- Use a [news sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/news-sitemap) if your site has news content.
- Use the `<lastmod>` tag in sitemaps to indicate when an indexed URL has been updated.
- Use a simple URL structure to help Google find your pages.
- Provide standard, [crawlable `<a>` links](https://developers.google.com/search/docs/crawling-indexing/links-crawlable#crawlable-links) to help Google find your pages.
- If your site uses separate HTML for mobile and desktop versions, provide the same set of links on the mobile version as you have on the desktop version. If it's not possible to provide the same set of links on the mobile version, ensure that they're included in a [sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview) file. Google only [indexes the
  mobile version](https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing) of pages, and limiting the links shown there can slow down discovery of new pages.

**Avoid:**

- Submitting the same, unchanged sitemap multiple times per day.
- Expecting that Googlebot will crawl everything in a sitemap, or crawl them immediately. Sitemaps are useful suggestions to Googlebot, not absolute requirements.
- Including URLs in your sitemaps that [you don't want to appear in Search](https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget#hide_urls). This can waste your crawl budget on pages that you don't want indexed.

### Improve your site's crawl efficiency

#### Increase your page loading speed


Google's crawling is limited by bandwidth, time, and availability of Googlebot instances.
If your server responds to requests quicker, we might be able to crawl more pages on your
site. That said, Google only wants to crawl high quality content, so simply making low
quality pages faster won't encourage Googlebot to crawl more of your site; conversely, if we
think that we're missing high-quality content on your site, we'll probably increase your
budget to crawl that content.

Here's how you can optimize your pages and resources for crawling:

- Prevent large but unimportant resources from being loaded by Googlebot using robots.txt. Be sure to block only non-critical resources---that is, resources that aren't important to understanding the meaning of the page (such as decorative images).
- Make sure that your pages are fast to load.
- Watch out for long redirect chains, which have a negative effect on crawling.
- Both the time to respond to server requests, as well as the time needed to render pages, matters, including load and run time for embedded resources such as images and scripts. Be aware of large or slow resources required for indexing.

#### Specify content changes with HTTP status codes


Google generally supports the
[`If-Modified-Since` and `If-None-Match` HTTP request headers](https://developer.mozilla.org/docs/Web/HTTP/Headers/If-Modified-Since)
for crawling. Google's crawlers don't send the headers with all crawl attempts; it depends on
the use case of the request (for example,
[AdsBot](https://developers.google.com/search/docs/crawling-indexing/overview-google-crawlers#adsbot) is more
likely to set the `If-Modified-Since` and `If-None-Match` HTTP request
headers). If our crawlers send the `If-Modified-Since` header, the header's value
is the [date and time](https://www.rfc-editor.org/rfc/rfc9110#name-if-modified-since)
the content was last crawled. Based on that value, the server may choose to return a
`304 (Not Modified)` HTTP status code with no response body, in which case Google
will reuse the content version it crawled the last time. If the content is newer than the date
specified by the crawler in the `If-Modified-Since` header, the server can return a
`200 (OK)` HTTP status code with the response body.


Independently of the request headers, you can send a `304 (Not Modified)` HTTP
status code and no response body for any Googlebot request if the content hasn't changed since
Googlebot last visited the URL. This will save your server processing time and resources,
which may indirectly improve crawl efficiency.

#### Hide URLs that you don't want in search results


Wasting server resources on unnecessary pages can reduce crawl activity from pages that are
important to you, which may cause a significant delay in discovering great new or updated
content on a site.
| Blocking or hiding already crawled pages from recrawls won't shift your crawl budget to another part of your site unless Google is already hitting your site's serving limits.


Exposing many URLs on your site that you don't want crawled by Search can negatively affect a
site's crawling and indexing. Typically these URLs fall into the following categories:

- [Faceted navigation](https://developers.google.com/search/docs/crawling-indexing/crawling-managing-faceted-navigation) and [session identifiers](https://developers.google.com/search/blog/2007/09/google-duplicate-content-caused-by-url): Faceted navigation is typically duplicate content from the site; session identifiers and other URL parameters that simply sort or filter the page don't provide new content. Learn how to [manage crawling of faceted navigation pages](https://developers.google.com/search/docs/crawling-indexing/crawling-managing-faceted-navigation).
- [Duplicate content](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls): Help Google identify duplicate content to avoid unnecessary crawling.
- [`soft 404` pages](https://developers.google.com/search/docs/crawling-indexing/http-network-errors#soft-404-errors): Return a `404` code when a page no longer exists.
- [Hacked pages](https://developers.google.com/search/docs/monitor-debug/security/what-is-hacked): Be sure to check the [Security
  Issues report](https://search.google.com/search-console/security-issues) and fix or remove any hacked pages you find.
- [Infinite spaces](https://developers.google.com/search/blog/2008/08/to-infinity-and-beyond-no) and proxies: Block these from crawling with robots.txt.
- [Low quality and spam content](https://developers.google.com/search/docs/essentials/spam-policies): Good to avoid, obviously.
- Shopping cart pages, infinite scrolling pages, and pages that perform an action (such as "sign up" or "buy now" pages).

**Do:**

- Use robots.txt if you don't want Google to crawl a resource or page at all.
- If a common resource is reused on multiple pages (such as a shared image or JavaScript file), reference the resource from the same URL in each page, so that Google can cache and reuse the same resource without needing to request the same resource multiple times.

**Avoid:**

- Don't add or remove pages or directories from robots.txt regularly as a way of reallocating crawl budget for your site. Use robots.txt only for pages or resources that you don't want to appear on Google for the long run.
- Don't rotate sitemaps or use other temporary hiding mechanisms to reallocate budget.

### Handle overcrawling of your site (emergencies)

Googlebot has algorithms to prevent it from overwhelming your site with crawl requests.
However, if you find that Googlebot is overwhelming your site, there are a few things you can
do.

**Diagnosing**:

Monitor your server for excessive Googlebot requests to your site.

**Treating**:

In an emergency, we recommend the following steps to slow down an overwhelming crawl from
Googlebot:

1. Return `503` or `429` HTTP response status codes *temporarily* for Googlebot requests when your server is overloaded. Googlebot will retry these URLs for about 2 days. Note that returning "no availability" codes for more than a few days will cause Google to permanently slow or stop crawling URLs on your site, so follow the additional next steps.
2. When the crawl rate goes down, stop returning `503` or `429` HTTP response status codes for crawl requests; returning `503` or `429` for more than 2 days will cause Google to drop those URLs from the index.
3. Monitor your crawling and your host capacity over time.
4. If the problematic crawler is one of the [AdsBot crawlers](https://developers.google.com/search/docs/crawling-indexing/google-special-case-crawlers#adsbot-mobile-web), the problem is likely that you have created [Dynamic Search Ad targets](https://support.google.com/google-ads/answer/2497706) for your site that Google is trying to crawl. This crawl will reoccur every 3 weeks. If you don't have the server capacity to handle these crawls, either limit your ad targets or get increased serving capacity.

## Myths and facts about crawling


Test your knowledge on how Google crawls and indexes websites.
Compressing my sitemaps can increase my crawl budget.  
True  
False  
It won't. Zipped sitemaps still have to be fetched from the server, so you're not really saving much crawling time or effort on Google's part by sending compressed sitemaps. Google prefers fresher content, so I'd better keep tweaking my page.  
True  
False  
Content is rated by quality, regardless of age. Create and update your content as necessary, but there's no additional value in making pages artificially appear to be fresh by making trivial changes and updating the page date. Google prefers old content (it has more weight) over fresh content.  
True  
False  
If your page is useful, it's useful, whether it's new or old. Google prefers clean URLs and doesn't like query parameters.  
True  
False  
We can crawl parameters. The faster your pages load and render, the more Google is able to crawl.  
True  
True, in that our resources are limited by a combination of time and number of crawling bots. If you can serve us more pages in a limited time, we will be able to crawl more of them. However, we might devote more time crawling a site that has more important information, even if it is slower. It's probably more important for you to make your site faster for your users than to make it faster to increase your crawl coverage. It's much simpler to help Google crawl the right content than it is to crawl all your content every time. Note that crawling a site involves both retrieving and rendering the content. Time spent rendering the page counts as much as time spent requesting the page. So making your pages faster to render will also increase the crawl speed.  
False  
Small sites aren't crawled as often as big ones.  
True  
False  
If a site has important content that changes often, we crawl it often, regardless of the size. The closer your content is to the home page the more important it is to Google.  
True  
Partly true  
Your site's home page is often the most important page on your site, and so pages linked directly to the home page may be seen as more important, and therefore crawled more often. However, this doesn't mean that these pages will be ranked more highly than other pages on your site.  
False  
URL versioning is a good way to encourage Google to recrawl my pages.  
True  
Partly true  
Using a versioned URL for your page in order to entice Google to crawl it again sooner will probably work, but often this is not necessary, and will waste crawl resources if the page is not actually changed. If you do use versioned URLs to indicate new content, we recommend that you only change the URL when the page content has changed meaningfully.  
False  
Site speed and errors affect my crawl budget.  
True  
Making a site faster improves the users' experience while also increasing crawl rate. For Googlebot, a speedy site is a sign of healthy servers, so it can get more content over the same number of connections. On the flip side, a significant number of [`5xx` HTTP response status codes](https://developers.google.com/search/docs/crawling-indexing/http-network-errors#http-status-codes) (server errors) or connection timeouts signal the opposite, and crawling slows down. We recommend paying attention to the Crawl Stats report in Search Console and keeping the number of server errors low.  
False  
Crawling is a ranking factor.  
True  
False  
Improving your crawl rate will not necessarily lead to better positions in search results. Google uses many signals to rank the results, and while crawling is necessary for a page to be in search results, it's not a ranking signal. Alternate URLs and embedded content count in the crawl budget.  
True  
Generally, any URL that Googlebot crawls will count towards a site's crawl budget. Alternate URLs, like AMP or hreflang, as well as embedded content, such as CSS and JavaScript, including [XHR fetches](https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest), may have to be crawled and will consume a site's crawl budget.  
False  
I can control Googlebot with the "crawl-delay" rule.  
True  
False  
The non-standard "crawl-delay" robots.txt rule is not processed by Googlebot. The `nofollow` rule affects crawl budget.  
True  
Partly true  
Any URL that is crawled affects crawl budget, so even if your page marks a URL as `nofollow`, it can still be crawled if another page on your site, or any page on the web, doesn't label the link as `nofollow`.  
False  
I can use `noindex` to control crawl budget.  
True  
Partly true  
Any URL that is crawled affects crawl budget, and Google has to crawl the page in order to find the `noindex` rule.   

However, `noindex` is there to help you keep things out of the index. If you want to ensure that those pages don't end up in Google's index, continue using `noindex` and don't worry about crawl budget. It's also important to note that if you remove URLs from Google's index with `noindex` or otherwise, Googlebot can focus on other URLs on your site, which means `noindex` can indirectly free up some crawl budget for your site in the long run.  
False  
Pages that serve `4xx` HTTP status codes are wasting crawl budget.  
True  
False  
Pages that serve [`4xx` HTTP status codes](https://developers.google.com/search/docs/crawling-indexing/http-network-errors#4xx-client-errors) (except `429`) don't waste crawl budget. Google attempted to crawl the page, but received a status code and no other content.

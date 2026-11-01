# debug

> This legacy URL now redirects to https://developers.google.com/search/help/debug.
> Canonical content mirrored below.

# Debug Your Website Pages | Google Search Central

# Debugging your pages

[Video](https://www.youtube.com/watch?v=jFeLHfY0xkE)

## General tips


Remember that Google does not crawl your page immediately after you publish a fix. Therefore
[Search Console](https://search.google.com/search-console) (and Google Search) can
continue to show an error for a page that you have fixed
until the page is crawled again. You can sometimes request an expedited crawl, for example
using the [URL Inspection](https://support.google.com/webmasters/answer/9012289)
tool, but in most cases it takes a few days to notice changes in your pages.

## Useful testing tools


Here are some useful tools to help you debug your pages.

### Verified site owner tools


The following tools and reports require you to be a
[verified site user](https://support.google.com/webmasters/answer/9008080)
for the page in order to use this tool on that page or site. This is because Search Console
provides confidential site data that only a verified site user should have access to.

- [Search Console](https://search.google.com/search-console) - Sign up for Search Console and [verify ownership of a site](https://support.google.com/webmasters/answer/9008080) to get access to useful site monitoring and testing tools, such as those listed below.
- [Rich result status reports](https://support.google.com/webmasters/answer/7552505) - Learn which rich results Google could or couldn't read from your site, get troubleshooting information for rich result errors, and request a recrawl after you have fixed any problems. You cannot test an arbitrary URL using this tool.
- [URL Inspection tool](https://support.google.com/webmasters/answer/9012289) - Learn how your page appears in the Google index, run an index test on a live URL, and see how Google renders your page, and submit a URL for indexing.
- [Robots.txt report](https://support.google.com/webmasters/answer/6062598) - Check whether Google can process your robots.txt files. You an also request a recrawl of a robots.txt file for emergency situations.
- [AMP status report](https://search.google.com/search-console/amp) - See AMP page errors for your entire site detected by Google. Errors are detected during the regular crawl; you cannot test an arbitrary URL.

### Anonymous tools


These tools can be used on any URL without needing Search Console permissions on the website.
Some tools also allow code snippets pasted into the tool itself.


If your URL is behind a firewall, or is hosted on a local computer, you can use a tunnelling
solution to expose your page to the testing tool. [Learn how to test locally-hosted or firewalled pages.](https://developers.google.com/search/help/debug#testing-firewalled-pages)

- [AMP Test Tool](https://search.google.com/test/amp) - Test the validity of a specific AMP URL in real time.
- [Rich Results Test](https://search.google.com/test/rich-results) - Test the validity of a structured data block in real time. The code can either be pasted into the tool, or hosted on a live page.

### More tools


See [our help page](https://developers.google.com/search/help) for more resources and office hours information.

## Testing locally-hosted or firewalled pages


Google provides several testing tools to test a single live web page. For example, the
[AMP Test Tool](https://search.google.com/test/amp) and the
[Rich Results Test](https://search.google.com/test/rich-results).
However, if your page is running on your local machine without a public
URL, or if it is hosted behind a firewall, you can still test the page by exposing a tunnel to
your page for the testing tool.
This can be useful if you want to test a page before making it publicly available on the web,
or even as another step in your release process.


To test a local or firewalled page, use a tunneling solution such as `ngrok`. These
tools provide a public URL that connects to a non-public page on your local host or firewalled
server.


The following example first starts up python's
[`SimpleHTTPServer`](https://docs.python.org/2/library/simplehttpserver.html)
to host a page on the local computer, then uses
[ngrok](https://ngrok.com/) to expose that page on a
publicly-accessible URL:

**Step 1**


Start up a local HTTP server to host your page on a given port. For our example we chose port
`5326`.


`SimpleHTTPServer` maps the current directory as the site root.

     python3 -m http.server 5326
    Serving HTTP on 0.0.0.0 port 5326
    ...


**Step 2**


On another terminal, start up your local `ngrok` app, listening to port
`5326`, which we opened in step 1.

     ./ngrok http 5326 --request-header-add ngrok-skip-browser-warning:1
    ngrok by @inconshreveable (Ctrl+C to quit)

    Session Status online
    Version 2.2.4
    Region United States (us)
    Web Interface http://127.0.0.1:4040
    Forwarding http://ad0a5735.ngrok.io -> localhost:5326
    Forwarding https://ad0a5735.ngrok.io -> localhost:5326

    Connections ttl opn rt1 rt5 p50 p90
    0 0 0.00 0.00 0.00 0.00


**Step 3**


Pass your exposed ngrok URL to the test tool of your choice.


The root URL in our example is `http://ad0a5735.ngrok.io`, so if our page is saved
locally at `~/testwebdir/mypage.html`, and we started the server above from
`~/testwebdir/`, we could test `http://ad0a5735.ngrok.io/mypage.html`.
In the Rich Results Test, you could paste that URL in directly, or visit
`https://search.google.com/test/rich-results/result?url=http%3A%2F%2Fad0a5735.ngrok.io%2Fmypage.html`.


Note that different local hosts and tunneling solutions map your pages differently.


Also, some tunneling solutions (not ngrok) automatically protect your temporary public URL
with robots.txt, which will prevent you from running Google tests on them. Google testing
tools respect robots.txt. Read the documentation for your tunneling solution and web hosting
software.

### Debugging access errors


If you get an access error using a Google testing tool:

- Check that your page isn't protected by robots.txt and doesn't require a login.
- Try accessing your page from outside your firewall, on another computer, or using Chrome in Incognito mode.
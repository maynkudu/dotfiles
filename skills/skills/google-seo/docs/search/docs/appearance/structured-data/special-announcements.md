# Special Announcement (SpecialAnnouncement) Structured Data | Google Search Central

Special announcement (`SpecialAnnouncement`) structured data (BETA)
===================================================================

| **Upcoming deprecation** : We're phasing out support for a few structured data types in Google Search. Learn more about [what's changing in our blog post](/search/blog/2025/06/simplifying-search-results).


Many organizations, such governments, health organizations, schools,
and more, may need to publish urgent announcements (such as COVID-19 announcements) that
affect schedules and other aspects of everyday life. This includes the closure of facilities,
rescheduling of events, and new availability of medical facilities (for example, testing
centers). Here are some examples of special announcements:

- Announcement of a shelter-in-place directive
- Closure notice (for example, closing a school or public transportation)
- Announcement of government benefits (for example, unemployment support, paid leave, or one-time payments)
- Quarantine guidelines
- Travel restrictions
- Notification of a new drive-through testing center
- Announcement of an event transitioning from offline to online, or cancellation
- Announcement of revised hours and shopping restrictions
- Disease spread statistics and maps

| If you want to update your business hours, we recommend that you use [`LocalBusiness` markup](/search/docs/appearance/structured-data/local-business) or [update your business profile on Google](https://support.google.com/business/answer/10417060). Additionally, you can use `SpecialAnnouncement` to announce your new store hours. This may not show up in Google Search, but it does help Google understand the data behind special announcements.
| **Note** : The actual appearance in search results might be different. You can preview most features with the [Rich Results Test](https://support.google.com/webmasters/answer/7445569).

How to implement special announcements
--------------------------------------


There are two ways that you can implement your special announcements:

- [**Add `SpecialAnnouncement` structured data to your web pages (recommended)**](#add-structured-data): Structured data is a standardized format for providing information about a page and classifying the page content. If you're new to structured data, you can learn more about [how structured data works](/search/docs/appearance/structured-data/intro-structured-data).
- [**Submit announcements in Search Console**](#using-search-console): If you don't have access to your site's HTML, or you need to quickly submit the announcement (and you don't have time to implement structured data), you can submit the announcement in Search Console. The tool is only for short-lived announcements that are set to expire within a month of posting. Also, there is no way to update your announcement (with structured data, it's possible to update your announcement with more details or extend the date).

How to add structured data
--------------------------


Structured data is a standardized format for providing information about a page and classifying the page
content. If you're new to structured data, you can learn more about
[how structured data works](/search/docs/appearance/structured-data/intro-structured-data).


Here's an overview of how to build, test, and release structured data.

1. Add the [required properties](#structured-data-type-definitions). Based on the format you're using, learn where to [insert structured data on the page](/search/docs/appearance/structured-data/intro-structured-data#format-placement). **Using a CMS?** It may be easier to use a plugin that's integrated into your CMS.   
   | **Using JavaScript?** Learn how to [generate structured data with JavaScript](/search/docs/appearance/structured-data/generate-structured-data-with-javascript).
2. Follow the [guidelines](#guidelines).
3. Validate your code using the [Rich Results Test](https://search.google.com/test/rich-results) and fix any critical errors. Consider also fixing any non-critical issues that may be flagged in the tool, as they can help improve the quality of your structured data (however, this isn't necessary to be eligible for rich results).
4. Deploy a few pages that include your structured data and use the [URL Inspection tool](https://support.google.com/webmasters/answer/9012289) to test how Google sees the page. Be sure that your page is accessible to Google and not blocked by a robots.txt file, the `noindex` tag, or login requirements. If the page looks okay, you can [ask Google to recrawl your URLs](/search/docs/crawling-indexing/ask-google-to-recrawl). **Note**: Allow time for re-crawling and re-indexing. Remember that it may take several days after publishing a page for Google to find and crawl it.
5. To keep Google informed of future changes, we recommend that you [submit a sitemap](/search/docs/crawling-indexing/sitemaps/build-sitemap). You can automate this with the [Search Console Sitemap API](/webmaster-tools/v1/sitemaps).

Submit a special announcement for your site in Search Console (BETA)
--------------------------------------------------------------------


Government agencies and official health organizations can
[submit an important announcement](https://search.google.com/search-console/special-announcement)
on their site, particularly if they are unable to use
structured data. This includes the closure of facilities, rescheduling of events, and new
availability of medical facilities (for example, testing centers). Google Search uses this
information to better understand the content on your web page and show the important
announcement to relevant people alongside your web page result.
[Open announcement submission tool](https://search.google.com/search-console/special-announcement) **Limitations of the tool** : This is a beta version, and you may not see results in Google Search right away.
|
| - The tool requires that announcements expire within 1 month of posting, so this method is only for short-lived announcements.
| - If you don't set an expiration date, your announcement will default to expire 7 days from the time the announcement was posted.
| - The tool is focused on health and government organizations; it doesn't support news articles.

Feature availability
--------------------


You may see changes in requirements or guideline, and you may not see results in Google Search
right away. We are focusing on announcements from health and government organizations. You can
provide structured data or submit your announcement in Search Console in advance, to ensure
that your announcements are eligible when the feature becomes available. This helps Google
understand the data behind special announcements.

Examples
--------

### Shelter-in-place announcement


Here's an example of a shelter-in-place announcement that affects multiple counties.  

### JSON-LD

\<html\> \<head\> \<title\>Shelter-in-place announcement\</title\> \<script type="application/ld+json"\> { "@context": "https://schema.org", "@type": "SpecialAnnouncement", "name": "Shelter-in-place for 3 California counties", "text": "As of 11:59 pm on March 17, 2024, all individuals in the 3 counties must strictly follow the provisions in this new Order. This new Order will be in effect through March 30, 2024.", "datePosted": "2024-03-17T08:00", "expires": "2024-03-24T23:59", "quarantineGuidelines": "https://example.org/california/shelter-in-place/", "diseasePreventionInfo": "https://example.org/california/prevention-tips/", "spatialCoverage": \[ { "type": "AdministrativeArea", "name": "San Francisco County, CA" }, { "type": "AdministrativeArea", "name": "Marin County, CA" }, { "type": "AdministrativeArea", "name": "Santa Clara County, CA" } \] } \</script\> \</head\> \<body\> \</body\> \</html\>   

```json-ld
<html>
  <head>
    <title>Shelter-in-place announcement</title>
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "SpecialAnnouncement",
      "name": "Shelter-in-place for 3 California counties",
      "text": "As of 11:59 pm on March 17, 2024, all individuals in the 3 counties must strictly follow the provisions in this new Order. This new Order will be in effect through March 30, 2024.",
      "datePosted": "2024-03-17T08:00",
      "expires": "2024-03-24T23:59",
      "quarantineGuidelines": "https://example.org/california/shelter-in-place/",
      "diseasePreventionInfo": "https://example.org/california/prevention-tips/",
      "spatialCoverage": [
        {
          "type": "AdministrativeArea",
          "name": "San Francisco County, CA"
        },
        {
          "type": "AdministrativeArea",
          "name": "Marin County, CA"
        },
        {
          "type": "AdministrativeArea",
          "name": "Santa Clara County, CA"
        }
      ]
    }
    </script>
  </head>
  <body>
  </body>
</html>
```

### Microdata

\<html itemscope itemprop="SpecialAnnouncement" itemtype="https://schema.org/SpecialAnnouncement"\> \<head\> \<title itemprop="name"\>Shelter-in-place for 3 California counties\</title\> \</head\> \<body\> \<p itemprop="datePosted" content="2024-03-17T08:00"\>March 17, 2024\</p\> \<meta itemprop="expires" content="2024-03-30T08:00" /\> \<p itemprop="text"\>As of 11:59 pm on March 17, 2024, all individuals in the 3 counties must strictly follow the provisions in this new Order. This new Order will be in effect through March 30, 2024.\</p\> \<p itemprop="quarantineGuidelines" content="https://example.org/california/shelter-in-place/"\>\<a href="https://example.org/california/shelter-in-place/"\>Learn more\</a\>.\</p\> \<meta itemprop="diseasePreventionInfo" content="https://example.org/california/prevention-tips/" /\> \<div itemprop="spatialCoverage" itemtype="https://schema.org/AdministrativeArea" itemscope\> \<meta itemprop="name" content="San Francisco County, CA" /\> \</div\> \<div itemprop="spatialCoverage" itemtype="https://schema.org/AdministrativeArea" itemscope\> \<meta itemprop="name" content="Marin County, CA" /\> \</div\> \<div itemprop="spatialCoverage" itemtype="https://schema.org/AdministrativeArea" itemscope\> \<meta itemprop="name" content="Santa Clara County, CA" /\> \</div\> \</body\> \</html\>   

```text
<html itemscope itemprop="SpecialAnnouncement" itemtype="https://schema.org/SpecialAnnouncement">
<head>
  <title itemprop="name">Shelter-in-place for 3 California counties</title>
</head>
<body>
  <p itemprop="datePosted" content="2024-03-17T08:00">March 17, 2024</p>
  <meta itemprop="expires" content="2024-03-30T08:00" />
  <p itemprop="text">As of 11:59 pm on March 17, 2024, all individuals in the 3 counties must strictly follow the provisions in this new Order. This new Order will be in effect through March 30, 2024.</p>
  <p itemprop="quarantineGuidelines" content="https://example.org/california/shelter-in-place/"><a href="https://example.org/california/shelter-in-place/">Learn more</a>.</p>
  <meta itemprop="diseasePreventionInfo" content="https://example.org/california/prevention-tips/" />
  <div itemprop="spatialCoverage" itemtype="https://schema.org/AdministrativeArea" itemscope>
    <meta itemprop="name" content="San Francisco County, CA" />
    </div>
  <div itemprop="spatialCoverage" itemtype="https://schema.org/AdministrativeArea" itemscope>
    <meta itemprop="name" content="Marin County, CA" />
  </div>
  <div itemprop="spatialCoverage" itemtype="https://schema.org/AdministrativeArea" itemscope>
    <meta itemprop="name" content="Santa Clara County, CA" />
  </div>
</body>
</html>
```

### Multiple updates on a single page


Here's an example of an updates page that has multiple announcements.  

### JSON-LD

\<html\> \<head\> \<title\>CA Updates on COVID-19\</title\> \<script type="application/ld+json"\> \[{ "@context": "https://schema.org", "@type": "SpecialAnnouncement", "name": "Shelter-in-place for 3 California counties", "text": "\<a href=https://example.org/california/executive-order-123\>Executive order 123\</a\> requires residents to shelter-in-place through April 30. Additional disease prevention and quarantine guidelines are also available.", "datePosted": "2024-04-01T08:00", "expires": "2024-05-03T23:59", "quarantineGuidelines": "https://example.org/california/shelter-in-place", "diseasePreventionInfo": "https://example.org/california/prevention-tips", "spatialCoverage": \[ { "type": "AdministrativeArea", "name": "Santa Clara County, CA" }, { "type": "AdministrativeArea", "name": "Marin County, CA" }, { "type": "AdministrativeArea", "name": "Santa Clara County, CA" } \] }, { "@context": "https://schema.org", "@type": "SpecialAnnouncement", "name": "New information regarding worker benefits during COVID-19", "text": "A new summary chart explains the benefits for workers that are impacted by COVID-19. \<a href=https://example.org/california/summary-of-benefits\>Learn more\</a\>.", "datePosted": "2024-03-30T08:00", "expires": "2024-04-06T23:59", "newsUpdatesAndGuidelines": "https://example.org/california/worker-benefits-covid-19", "spatialCoverage": { "type": "State", "name": "CA" } }, { "@context": "https://schema.org", "@type": "SpecialAnnouncement", "name": "Updates on key federal changes to make food and health care more accessible", "text": "The Federal Government is making food and health care more accessible.", "datePosted": "2024-03-29T08:00", "expires": "2024-04-05T23:59", "newsUpdatesAndGuidelines": "https://example.org/california/food-health-guidelines", "diseasePreventionInfo": "https://example.org/california/prevention-tips", "spatialCoverage": { "type": "State", "name": "CA" } } \] \</script\> \</head\> \<body\> \</body\> \</html\>   

```json-ld
<html>
  <head>
    <title>CA Updates on COVID-19</title>
    <script type="application/ld+json">
  [{
      "@context": "https://schema.org",
      "@type": "SpecialAnnouncement",
      "name": "Shelter-in-place for 3 California counties",
      "text": "<a href=https://example.org/california/executive-order-123>Executive order 123</a> requires residents to shelter-in-place through April 30. Additional disease prevention and quarantine guidelines are also available.",
      "datePosted": "2024-04-01T08:00",
      "expires": "2024-05-03T23:59",
      "quarantineGuidelines": "https://example.org/california/shelter-in-place",
      "diseasePreventionInfo": "https://example.org/california/prevention-tips",
      "spatialCoverage": [
        {
          "type": "AdministrativeArea",
          "name": "Santa Clara County, CA"
        },
        {
          "type": "AdministrativeArea",
          "name": "Marin County, CA"
        },
        {
          "type": "AdministrativeArea",
          "name": "Santa Clara County, CA"
        }
      ]
    },
  {
      "@context": "https://schema.org",
      "@type": "SpecialAnnouncement",
      "name": "New information regarding worker benefits during COVID-19",
      "text": "A new summary chart explains the benefits for workers that are impacted by COVID-19. <a href=https://example.org/california/summary-of-benefits>Learn more</a>.",
      "datePosted": "2024-03-30T08:00",
      "expires": "2024-04-06T23:59",
      "newsUpdatesAndGuidelines": "https://example.org/california/worker-benefits-covid-19",
      "spatialCoverage":
        {
          "type": "State",
          "name": "CA"
        }
    },
    {
      "@context": "https://schema.org",
      "@type": "SpecialAnnouncement",
      "name": "Updates on key federal changes to make food and health care more accessible",
      "text": "The Federal Government is making food and health care more accessible.",
      "datePosted": "2024-03-29T08:00",
      "expires": "2024-04-05T23:59",
      "newsUpdatesAndGuidelines": "https://example.org/california/food-health-guidelines",
      "diseasePreventionInfo": "https://example.org/california/prevention-tips",
      "spatialCoverage":
        {
          "type": "State",
          "name": "CA"
        }
      }
  ]
    </script>
  </head>
  <body>
  </body>
</html>
```

### Microdata

\<html\> \<head\> \<title itemprop="name"\>CA Updates on COVID-19\</title\> \</head\> \<body\> \<div itemscope itemprop="SpecialAnnouncement" itemtype="https://schema.org/SpecialAnnouncement"\> \<h2 itemprop="name"\>Shelter-in-place for 3 California counties\</h2\> \<meta itemprop="datePosted" content="2024-03-17T08:00" /\> \<meta itemprop="expires" content="2024-03-30T08:00" /\> \<p itemprop="text"\>\<a href=https://example.org/california/executive-order-123\>Executive order 123\</a\> requires residents to shelter-in-place through April 30. Additional disease prevention and quarantine guidelines are also available.\</p\> \<p itemprop="quarantineGuidelines" content="https://example.org/california/shelter-in-place/"\>\<a href="https://example.org/california/shelter-in-place/"\>Learn more\</a\>.\</p\> \<meta itemprop="diseasePreventionInfo" content="https://example.org/california/prevention-tips/" /\> \<div itemprop="spatialCoverage" itemtype="https://schema.org/AdministrativeArea" itemscope\> \<meta itemprop="name" content="San Francisco County, CA" /\> \</div\> \<div itemprop="spatialCoverage" itemtype="https://schema.org/AdministrativeArea" itemscope\> \<meta itemprop="name" content="Marin County, CA" /\> \</div\> \<div itemprop="spatialCoverage" itemtype="https://schema.org/AdministrativeArea" itemscope\> \<meta itemprop="name" content="Santa Clara County, CA" /\> \</div\> \</div\> \<div itemscope itemprop="SpecialAnnouncement" itemtype="https://schema.org/SpecialAnnouncement"\> \<h2 itemprop="name"\>New information regarding worker benefits during COVID-19\</h2\> \<meta itemprop="datePosted" content="2024-03-30T08:00" /\> \<meta itemprop="expires" content="2024-04-06T23:59" /\> \<p itemprop="text"\>A new summary chart explains the benefits for workers that are impacted by COVID-19. \<a href=https://example.org/california/summary-of-benefits\>Learn more\</a\>.\</p\> \<meta itemprop="newsUpdatesAndGuidelines" content="https://example.org/california/worker-benefits-covid-19" /\> \<div itemprop="spatialCoverage" itemtype="https://schema.org/State" itemscope\> \<meta itemprop="name" content="CA" /\> \</div\> \</div\> \<div itemscope itemprop="SpecialAnnouncement" itemtype="https://schema.org/SpecialAnnouncement"\> \<h2 itemprop="name"\>Updates on key federal changes to make food and health care more accessible\</h2\> \<meta itemprop="datePosted" content="2024-03-29T08:00" /\> \<meta itemprop="expires" content="2024-04-05T23:59" /\> \<p itemprop="text"\>The Federal Government is making food and health care more accessible.\</p\> \<meta itemprop="newsUpdatesAndGuidelines" content="https://example.org/california/food-health-guidelines" /\> \<meta itemprop="diseasePreventionInfo" content="https://example.org/california/prevention-tip" /\> \<div itemprop="spatialCoverage" itemtype="https://schema.org/State" itemscope\> \<meta itemprop="name" content="CA" /\> \</div\> \</div\> \</body\> \</html\>   

```text
<html>
<head>
  <title itemprop="name">CA Updates on COVID-19</title>
</head>
<body>
<div itemscope itemprop="SpecialAnnouncement" itemtype="https://schema.org/SpecialAnnouncement">
  <h2 itemprop="name">Shelter-in-place for 3 California counties</h2>
  <meta itemprop="datePosted" content="2024-03-17T08:00" />
  <meta itemprop="expires" content="2024-03-30T08:00" />
  <p itemprop="text"><a href=https://example.org/california/executive-order-123>Executive order 123</a> requires residents to shelter-in-place through April 30. Additional disease prevention and quarantine guidelines are also available.</p>
  <p itemprop="quarantineGuidelines" content="https://example.org/california/shelter-in-place/"><a href="https://example.org/california/shelter-in-place/">Learn more</a>.</p>
  <meta itemprop="diseasePreventionInfo" content="https://example.org/california/prevention-tips/" />
  <div itemprop="spatialCoverage" itemtype="https://schema.org/AdministrativeArea" itemscope>
    <meta itemprop="name" content="San Francisco County, CA" />
    </div>
  <div itemprop="spatialCoverage" itemtype="https://schema.org/AdministrativeArea" itemscope>
    <meta itemprop="name" content="Marin County, CA" />
  </div>
  <div itemprop="spatialCoverage" itemtype="https://schema.org/AdministrativeArea" itemscope>
    <meta itemprop="name" content="Santa Clara County, CA" />
  </div>
</div>
<div itemscope itemprop="SpecialAnnouncement" itemtype="https://schema.org/SpecialAnnouncement">
  <h2 itemprop="name">New information regarding worker benefits during COVID-19</h2>
  <meta itemprop="datePosted" content="2024-03-30T08:00" />
  <meta itemprop="expires" content="2024-04-06T23:59" />
  <p itemprop="text">A new summary chart explains the benefits for workers that are impacted by COVID-19. <a href=https://example.org/california/summary-of-benefits>Learn more</a>.</p>
  <meta itemprop="newsUpdatesAndGuidelines" content="https://example.org/california/worker-benefits-covid-19" />
  <div itemprop="spatialCoverage" itemtype="https://schema.org/State" itemscope>
    <meta itemprop="name" content="CA" />
    </div>
</div>
<div itemscope itemprop="SpecialAnnouncement" itemtype="https://schema.org/SpecialAnnouncement">
  <h2 itemprop="name">Updates on key federal changes to make food and health care more accessible</h2>
  <meta itemprop="datePosted" content="2024-03-29T08:00" />
  <meta itemprop="expires" content="2024-04-05T23:59" />
  <p itemprop="text">The Federal Government is making food and health care more accessible.</p>
  <meta itemprop="newsUpdatesAndGuidelines" content="https://example.org/california/food-health-guidelines" />
  <meta itemprop="diseasePreventionInfo" content="https://example.org/california/prevention-tip" />
  <div itemprop="spatialCoverage" itemtype="https://schema.org/State" itemscope>
    <meta itemprop="name" content="CA" />
    </div>
</div>
</body>
</html>
```

### Government benefits announcement


Here's an example of an announcement of a new government benefit for small businesses.  

### JSON-LD

\<html\> \<head\> \<title\>New Paycheck Protection Program for small business\</title\> \<script type="application/ld+json"\> { "@context": "https://schema.org", "@type": "SpecialAnnouncement", "name": "New Paycheck Protection Program for small business", "text": "Example Administration announces a new loan that helps small businesses keep their workforce employed during the Coronavirus (COVID-19) crisis.", "datePosted": "2024-03-30T08:00", "expires": "2024-04-24T23:59", "category": "https://www.wikidata.org/wiki/Q81068910", "spatialCoverage": { "type": "Country", "name": "US" }, "governmentBenefitsInfo": { "@type": "GovernmentService", "name": "Paycheck Protection Program", "url": "https://www.sba.gov/funding-programs/loans/coronavirus-relief-options/paycheck-protection-program-ppp" } } } } \</script\> \</head\> \<body\> \</body\> \</html\>   

```json-ld
<html>
  <head>
    <title>New Paycheck Protection Program for small business</title>
    <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "SpecialAnnouncement",
    "name": "New Paycheck Protection Program for small business",
    "text": "Example Administration announces a new loan that helps small businesses keep their workforce employed during the Coronavirus (COVID-19) crisis.",
    "datePosted": "2024-03-30T08:00",
    "expires": "2024-04-24T23:59",
    "category": "https://www.wikidata.org/wiki/Q81068910",
    "spatialCoverage": {
      "type": "Country",
        "name": "US"
        },
    "governmentBenefitsInfo": {
      "@type": "GovernmentService",
      "name": "Paycheck Protection Program",
      "url":  "https://www.sba.gov/funding-programs/loans/coronavirus-relief-options/paycheck-protection-program-ppp"
        }
      }
    }
  }
    </script>
  </head>
  <body>
  </body>
</html>
```

### Microdata

\<html itemscope itemprop="SpecialAnnouncement" itemtype="https://schema.org/SpecialAnnouncement"\> \<head\> \<title itemprop="name"\>New Paycheck Protection Program for small business\</title\> \</head\> \<body\> \<meta itemprop="datePosted" content="2024-03-30T08:00" /\> \<meta itemprop="expires" content="2024-04-24T23:59" /\> \<p itemprop="text"\>Example Administration announces a new loan that helps small businesses keep their workforce employed during the Coronavirus (COVID-19) crisis.\</p\> \<div itemprop="spatialCoverage" itemtype="https://schema.org/Country" itemscope\> \<meta itemprop="name" content="US" /\> \</div\> \<div itemprop="governmentBenefitsInfo" itemtype="https://schema.org/GovernmentService" itemscope\> \<meta itemprop="url" content="https://www.example.gov/funding-programs/loans/coronavirus-relief-options/paycheck-protection-program-ppp" /\> \<meta itemprop="name" content="US Small Business Administration" /\> \</div\> \</body\> \</html\>   

```text
<html itemscope itemprop="SpecialAnnouncement" itemtype="https://schema.org/SpecialAnnouncement">
<head>
  <title itemprop="name">New Paycheck Protection Program for small business</title>
</head>
<body>
  <meta itemprop="datePosted" content="2024-03-30T08:00" />
  <meta itemprop="expires" content="2024-04-24T23:59" />
  <p itemprop="text">Example Administration announces a new loan that helps small businesses keep their workforce employed during the Coronavirus (COVID-19) crisis.</p>
  <div itemprop="spatialCoverage" itemtype="https://schema.org/Country" itemscope>
    <meta itemprop="name" content="US" />
  </div>
  <div itemprop="governmentBenefitsInfo" itemtype="https://schema.org/GovernmentService" itemscope>
    <meta itemprop="url" content="https://www.example.gov/funding-programs/loans/coronavirus-relief-options/paycheck-protection-program-ppp" />
    <meta itemprop="name" content="US Small Business Administration" />
  </div>
</body>
</html>
```

### School closure announcement


Here's an example of a school closure announcement.  

### JSON-LD

\<html\> \<head\> \<title\>COVID-19 School Announcements\</title\> \<script type="application/ld+json"\> { "@context": "https://schema.org", "@type": "SpecialAnnouncement", "name": "COVID-19 School Announcements", "text": "All schools will remain closed through a minimum of May 1 in alignment with school districts across all Bay Area counties.", "datePosted": "2024-03-17T08:00", "expires": "2024-03-24T23:59", "schoolClosuresInfo": "https://example-school-district.org/announcements/extended-closure-notice", "announcementLocation": { "@type": "CivicStructure", "name": "Example School", "url": "https://example-school.org/" } } \</script\> \</head\> \<body\> \</body\> \</html\>   

```json-ld
<html>
  <head>
    <title>COVID-19 School Announcements</title>
    <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "SpecialAnnouncement",
    "name": "COVID-19 School Announcements",
    "text": "All schools will remain closed through a minimum of May 1 in alignment with school
    districts across all Bay Area counties.",
    "datePosted": "2024-03-17T08:00",
    "expires": "2024-03-24T23:59",
    "schoolClosuresInfo": "https://example-school-district.org/announcements/extended-closure-notice",
    "announcementLocation": {
      "@type": "CivicStructure",
      "name": "Example School",
      "url": "https://example-school.org/"
    }
  }
    </script>
  </head>
  <body>
  </body>
</html>
```

### Microdata

\<html itemscope itemprop="SpecialAnnouncement" itemtype="https://schema.org/SpecialAnnouncement"\> \<head\> \<title itemprop="name"\>COVID-19 School Announcements\</title\> \</head\> \<body\> \<p itemprop="datePosted" content="2024-03-17T08:00"\>March 17, 2024\</p\> \<meta itemprop="expires" content="2024-03-30T08:00" /\> \<p itemprop="text"\>All schools will remain closed through a minimum of May 1 in alignment with school districts across all Bay Area counties.\</p\> \<p itemprop="schoolClosuresInfo" content="https://example-school-district.org/announcements/extended-closure-notice"\>\<a href="https://example-school-district.org/announcements/extended-closure-notice"\>Learn more\</a\>.\</p\> \<div itemprop="announcementLocation" itemtype="https://schema.org/CivicStructure" itemscope\> \<meta itemprop="name" content="Example School" /\> \<meta itemprop="url" content="https://example-school.org/" /\> \</div\> \</body\> \</html\>   

```text
<html itemscope itemprop="SpecialAnnouncement" itemtype="https://schema.org/SpecialAnnouncement">
<head>
  <title itemprop="name">COVID-19 School Announcements</title>
</head>
<body>
  <p itemprop="datePosted" content="2024-03-17T08:00">March 17, 2024</p>
  <meta itemprop="expires" content="2024-03-30T08:00" />
  <p itemprop="text">All schools will remain closed through a minimum of May 1 in alignment with school districts across all Bay Area counties.</p>
  <p itemprop="schoolClosuresInfo" content="https://example-school-district.org/announcements/extended-closure-notice"><a href="https://example-school-district.org/announcements/extended-closure-notice">Learn more</a>.</p>
  <div itemprop="announcementLocation" itemtype="https://schema.org/CivicStructure" itemscope>
    <meta itemprop="name" content="Example School" />
    <meta itemprop="url" content="https://example-school.org/" />
  </div>
</body>
</html>
```

### Testing facility announcement


Here's an example of a testing facility announcement.  

### JSON-LD

\<html\> \<head\> \<title\>COVID-19 testing facility announcement\</title\> \<script type="application/ld+json"\> { "@context": "https://schema.org", "@type": "SpecialAnnouncement", "name": "Example Health Care announces COVID-19 testing facility", "text": "Example Health Care's same-day primary care program is offering drive-through testing, by appointment, for SARS-CoV-2, the coronavirus that causes COVID-19.", "datePosted": "2024-03-16T08:00", "expires": "2024-03-24T23:59", "gettingTestedInfo": "https://med.example.edu/news/covid-19-testing-facility.html", "announcementLocation" : { "@type": "CivicStructure", "name": "Example Health Care", "url": "https://examplehealthcare.org/" } } \</script\> \</head\> \<body\> \</body\> \</html\>   

```json-ld
<html>
  <head>
    <title>COVID-19 testing facility announcement</title>
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "SpecialAnnouncement",
      "name": "Example Health Care announces COVID-19 testing facility",
      "text": "Example Health Care's same-day primary care program is offering drive-through testing, by appointment, for SARS-CoV-2, the coronavirus that causes COVID-19.",
      "datePosted": "2024-03-16T08:00",
      "expires": "2024-03-24T23:59",
      "gettingTestedInfo": "https://med.example.edu/news/covid-19-testing-facility.html",
      "announcementLocation" : {
        "@type": "CivicStructure",
        "name": "Example Health Care",
        "url": "https://examplehealthcare.org/"
        }
      }
    </script>
  </head>
  <body>
  </body>
</html>
```

### Microdata

\<html itemscope itemprop="SpecialAnnouncement" itemtype="https://schema.org/SpecialAnnouncement"\> \<head\> \<title itemprop="name"\>Example Health Care announces COVID-19 testing facility\</title\> \</head\> \<body\> \<p itemprop="datePosted" content="2024-03-17T08:00"\>March 17, 2024\</p\> \<meta itemprop="expires" content="2024-03-30T08:00" /\> \<p itemprop="text"\>Example Health Care's same-day primary care program is offering drive-through testing, by appointment, for SARS-CoV-2, the coronavirus that causes COVID-19.\</p\> \<p itemprop="gettingTestedInfo" content="https://med.example.edu/news/covid-19-testing-facility.html"\>\<a href="https://med.example.edu/news/covid-19-testing-facility.html"\>Learn more\</a\>.\</p\> \<div itemprop="announcementLocation" itemtype="https://schema.org/CivicStructure" itemscope\> \<meta itemprop="name" content="Example Health Care" /\> \<meta itemprop="url" content="https://examplehealthcare.org/" /\> \</div\> \</body\> \</html\>   

```text
<html itemscope itemprop="SpecialAnnouncement" itemtype="https://schema.org/SpecialAnnouncement">
<head>
  <title itemprop="name">Example Health Care announces COVID-19 testing facility</title>
</head>
<body>
  <p itemprop="datePosted" content="2024-03-17T08:00">March 17, 2024</p>
  <meta itemprop="expires" content="2024-03-30T08:00" />
  <p itemprop="text">Example Health Care's same-day primary care program is offering drive-through testing, by appointment, for SARS-CoV-2, the coronavirus that causes COVID-19.</p>
  <p itemprop="gettingTestedInfo" content="https://med.example.edu/news/covid-19-testing-facility.html"><a href="https://med.example.edu/news/covid-19-testing-facility.html">Learn more</a>.</p>
  <div itemprop="announcementLocation" itemtype="https://schema.org/CivicStructure" itemscope>
    <meta itemprop="name" content="Example Health Care" />
    <meta itemprop="url" content="https://examplehealthcare.org/" />
  </div>
</body>
</html>
```

Guidelines
----------


You must follow these guidelines to be eligible to appear in special announcements on Google
Search.
| **Warning** : If your site abuses or fails to follow the guidelines, Google may take manual action to mark it ineligible to display as a rich result. If you receive a [manual action](https://support.google.com/webmasters/answer/2604824), remedy the issue and submit your site for [reconsideration](https://support.google.com/webmasters/answer/35843).

- [General structured data guidelines](/search/docs/appearance/structured-data/sd-policies)
- [Search Essentials](/search/docs/essentials)

Structured data type definitions
--------------------------------


You must include the required properties for your content to be eligible for display as a
special announcement on Google Search. We recommend that you also add the recommended
properties if you have that information.

### `SpecialAnnouncement`


The full definition of [`SpecialAnnouncement`](https://schema.org/SpecialAnnouncement) is provided on schema.org. You can start using
`SpecialAnnouncement` even though it's still under development on Schema.org.
The Google-supported properties are the following:

|                                                                                                                                                                                                                                                                                                                                                                                                                                              Required properties                                                                                                                                                                                                                                                                                                                                                                                                                                               ||
|---------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `datePosted`                                                  | [DateTime](https://schema.org/DateTime) The date that the special announcement was published in [ISO-8601 format](https://en.wikipedia.org/wiki/ISO_8601).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `name`                                                        | [Text](https://schema.org/Text) The short title of the special announcement. For example: "Stanford announces COVID-19 testing facility"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| Either `text` or a specific property that points to more info | You must include either [text](#text), or one of the following properties that point to more info about the announcement, depending on the subject matter: - [diseasePreventionInfo](#disease-prevention) - [diseaseSpreadStatistics](#disease-spread) - [gettingTestedInfo](#getting-tested) - [governmentBenefitsInfo](#government-benefits-info) - [newsUpdatesAndGuidelines](#news-updates) - [publicTransportClosuresInfo](#public-transport) - [quarantineGuidelines](#quarantine) - [schoolClosuresInfo](#school) - [travelBans](#travel) | While only one property is required, we encourage you to include as much information that's applicable to the announcement. You can include multiple properties (for example, both `quarantineGuidelines` and `diseasePreventionInfo`, if it makes sense in the context of the announcement. |

|                                                                                                                                                                                                                                                                                                                                                                   Recommended properties                                                                                                                                                                                                                                                                                                                                                                    ||
|-------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `announcementLocation`        | [LocalBusiness](https://schema.org/LocalBusiness) or [CivicStructure](https://schema.org/CivicStructure) The specific location that is associated with the `SpecialAnnouncement`. For example, a specific testing facility or business with special opening hours. For a larger geographic region, like a quarantine of an entire region, we recommend that you use [spatialCoverage](#spatial-coverage). ```carbon { "@context": "https://schema.org", "@type": "SpecialAnnouncement", "announcementLocation": { "@type": "CivicStructure", "name": "Palo Alto High School" "url":   "https://example-school.org/" } } ```                                                                                                  |
| `announcementLocation.name`   | [Text](https://schema.org/Text) The name of the location that is the focus of the announcement. For example, the name of the testing facility.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `announcementLocation.url`    | [URL](https://schema.org/URL) The URL where people can learn more about the announcement location. For example, the URL for the testing facility that explains where it is, hours, and who is eligible.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `diseasePreventionInfo`       | [URL](https://schema.org/URL) or [WebContent](https://schema.org/WebContent) Information about disease prevention, if applicable to the announcement.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `diseaseSpreadStatistics`     | [URL](https://schema.org/URL) or [WebContent](https://schema.org/WebContent) or [Dataset](https://schema.org/Dataset) or [Observation](https://schema.org/Observation) If applicable to the announcement, the statistical information about the spread of a disease, either as `WebContent`, or described directly as a `Dataset`, or the specific `Observation` in the dataset. When a `WebContent` URL is provided, the page indicated might also contain more markup.                                                                                                                                                                                                                                                     |
| `expires`                     | [DateTime](https://schema.org/DateTime) The date in which the content expires and is no longer useful or available in [ISO-8601 format](https://en.wikipedia.org/wiki/ISO_8601). Don't include this property if you don't know when the content will expire.                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `gettingTestedInfo`           | [URL](https://schema.org/URL) or [WebContent](https://schema.org/WebContent) Information about getting tested for a [MedicalCondition](https://schema.org/MedicalCondition)), if applicable to the announcement.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `governmentBenefitsInfo`      | [GovernmentService](https://schema.org/GovernmentService) Information about new government benefits, if applicable to the announcement. If you include `governmentBenefitsInfo`, you must add the following properties: - [`governmentBenefitsInfo.name`](/search/docs/appearance/structured-data/special-announcements#benefits-name) - [`governmentBenefitsInfo.url`](/search/docs/appearance/structured-data/special-announcements#government-benefits-info-url) For a full example of how these properties work, see the [government benefits announcement example](#government-benefits).                                                                                                                               |
| `governmentBenefitsInfo.name` | [Text](https://schema.org/Text) The name of the government benefits. For example: `"Paycheck Protection Program"`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `governmentBenefitsInfo.url`  | [URL](https://schema.org/URL) The URL to more information about the government benefits.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `newsUpdatesAndGuidelines`    | [URL](https://schema.org/URL) or [WebContent](https://schema.org/WebContent) A page with news updates and guidelines about the special announcement, if applicable. This could be (but is not required to be) the main page containing [SpecialAnnouncement](https://schema.org/SpecialAnnouncement) markup on a site.                                                                                                                                                                                                                                                                                                                                                                                                       |
| `publicTransportClosuresInfo` | [URL](https://schema.org/URL) or [WebContent](https://schema.org/WebContent) Information about public transport closures, if applicable to the announcement.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `quarantineGuidelines`        | [URL](https://schema.org/URL) or [WebContent](https://schema.org/WebContent) Guidelines about quarantine rules, if applicable to the announcement.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `schoolClosuresInfo`          | [URL](https://schema.org/URL) or [WebContent](https://schema.org/WebContent) Information about school closures, if applicable to the announcement.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `spatialCoverage`             | [Place](https://schema.org/Place) The geographic region that is the focus of the special announcement, if applicable. For example, the announcement may be about a shelter-in-place that affects multiple regions. If the announcement affects both a region and a specific location (for example, a library closure that serves an entire region), use both `spatialCoverage` and `announcementLocation`. ```carbon { "@context": "https://schema.org", "@type": "SpecialAnnouncement", "spatialCoverage": [ { "type": "AdministrativeArea", "name": "San Francisco County, CA" }, { "type": "AdministrativeArea", "name": "Marin County, CA" }, { "type": "AdministrativeArea", "name": "Santa Clara County, CA" } ] } ``` |
| `text`                        | [Text](https://schema.org/Text) The textual summary of the special announcement. The text may contain HTML content such as links and lists. Valid HTML tags include: `<h1>` through `<h6>`, `<br>`, `<ol>`, `<ul>`, `<li>`, `<a>`, `<p>`, `<div>`, `<b>`, `<strong>`, `<i>`, and `<em>`. For example: "Stanford Health Care's same-day primary care program is offering drive-through testing, by appointment, for SARS-CoV-2, the coronavirus that causes COVID-19."                                                                                                                                                                                                                                                        |
| `travelBans`                  | [URL](https://schema.org/URL) or [WebContent](https://schema.org/WebContent) Information about travel bans, if applicable to the announcement.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |

Monitor rich results with Search Console
----------------------------------------


Search Console is a tool that helps you monitor how your pages perform in Google Search.
You don't have to sign up for Search Console to be included in Google Search results,
but it can help you understand and improve how Google sees your site. We
recommend checking Search Console in the following cases:

1. [After deploying structured data for the first time](#after-deploying)
2. [After releasing new templates or updating your code](#after-releasing)
3. [Analyzing traffic periodically](#analyzing-periodically)

### After deploying structured data for the first time


After Google has indexed your pages, look for issues using the relevant
[Rich result status report](https://support.google.com/webmasters/answer/7552505).
Ideally, there will be an increase of valid items, and no increase in invalid items. If you find issues
in your structured data:

1. [Fix the invalid items](#troubleshooting).
2. [Inspect a live URL](https://support.google.com/webmasters/answer/9012289#test_live_page) to check if the issue persists.
3. [Request validation](https://support.google.com/webmasters/answer/7552505#validation) using the status report.

### After releasing new templates or updating your code

When you make significant changes to your website, monitor for increases in structured data invalid items.

- If you see an **increase in invalid items**, perhaps you rolled out a new template that doesn't work, or your site interacts with the existing template in a new and bad way.
- If you see a **decrease in valid items** (not matched by an increase in invalid items), perhaps you are no longer embedding structured data in your pages. Use the [URL Inspection tool](https://support.google.com/webmasters/answer/9012289) to learn what is causing the issue.

### Analyzing traffic periodically

Analyze your Google Search traffic using the [Performance Report](https://support.google.com/webmasters/answer/7576553). The data will show you how often your page appears as a rich result in Search, how often users click on it and what is the average position you appear on search results. You can also automatically pull these results with the [Search Console API](/webmaster-tools/search-console-api-original/v3/how-tos/search_analytics).

Troubleshooting
---------------


If you're having trouble implementing or debugging structured data, here are some resources that
may help you.

- If you're using a content management system (CMS) or someone else is taking care of your site, ask them to help you. Make sure to forward any Search Console message that details the issue to them.
- Google does not guarantee that features that consume structured data will show up in search results. For a list of common reasons why Google may not show your content in a rich result, see the [General Structured Data Guidelines](/search/docs/appearance/structured-data/sd-policies).
- You might have an error in your structured data. Check the [list of structured data errors](https://support.google.com/webmasters/answer/7552505#error_list) and the [Unparsable structured data report](https://support.google.com/webmasters/answer/9166415).
- If you received a structured data manual action against your page, the structured data on the page will be ignored (although the page can still appear in Google Search results). To fix [structured data issues](https://support.google.com/webmasters/answer/9044175#zippy=%2Cstructured-data-issue), use the [Manual Actions report](https://support.google.com/webmasters/answer/9044175).
- Review the [guidelines](#guidelines) again to identify if your content isn't compliant with the guidelines. The problem can be caused by either spammy content or spammy markup usage. However, the issue may not be a syntax issue, and so the Rich Results Test won't be able to identify these issues.
- [Troubleshoot missing rich results / drop in total rich results](https://support.google.com/webmasters/answer/7552505#missing-jobs).
- Allow time for re-crawling and re-indexing. Remember that it may take several days after publishing a page for Google to find and crawl it. For general questions about crawling and indexing, check the [Google Search crawling and indexing FAQ](/search/help/crawling-index-faq).
- Post a question in the [Google Search Central forum](https://support.google.com/webmasters/community).

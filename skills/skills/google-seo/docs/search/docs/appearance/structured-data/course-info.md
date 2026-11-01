# Course Info Structured Data | Google Search Central

Course info (`Course` and `CourseInstance`) structured data
===========================================================

| **Upcoming deprecation** : We're phasing out support for a few structured data types in Google Search. Learn more about [what's changing in our blog post](/search/blog/2025/06/simplifying-search-results).


You can help people find your course content by telling Google about your course using
course info structured data. When you provide more detailed information about a course, such
as reviewer ratings, pricing, and course details, Google can better understand your course and
present a rich experience to people with the course info rich result.


There are two course rich result features that use the same schema.org `Course` type.
If your site provides information about courses, you can be eligible for both features by
following both implementation guides:

- **[Course list](/search/docs/appearance/structured-data/course)**: A rich result that lists courses from the same website.
- **[Course info](#guidelines)**: A carousel that shows detailed course information from a variety of websites.

Feature availability
--------------------


The course info rich result is available in English in all regions where Google Search is available.
We hope to support more non-English courses in the future.

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

Example
-------


Here's an example of a single course info page.
\<html\> \<head\> \<title\>Introduction to Computer Science and Programming\</title\> \<script type="application/ld+json"\> { "@context": "https://schema.org/", "@id": "https://www.example.com/advancedCpp", "@type": "Course", "name": "Learn Advanced C++ Topics", "description": "Improve your C++ skills by learning advanced topics.", "publisher": { "@type": "Organization", "name": "CourseWebsite", "url": "www.examplecoursewebsite.com" }, "provider": { "@type": "Organization", "name": "Example University", "url": "www.example.com" }, "image": \[ "https://example.com/photos/1x1/photo.jpg", "https://example.com/photos/4x3/photo.jpg", "https://example.com/photos/16x9/photo.jpg" \], "aggregateRating": { "@type": "AggregateRating", "ratingValue": 4, "ratingCount": 1234, "reviewCount": 450 }, "offers": \[{ "@type": "Offer", "category": "Paid", "priceCurrency": "EUR", "price": 10.99 }\], "totalHistoricalEnrollment": 12345, "datePublished": "2024-03-21", "educationalLevel": "Advanced", "about": \["C++ Coding", "Backend Engineering"\], "teaches": \["Practice and apply systems thinking to plan for change", "Understand how memory allocation works."\], "financialAidEligible": "Scholarship Available", "inLanguage": "en", "availableLanguage": \["fr", "es"\], "syllabusSections": \[ { "@type": "Syllabus", "name": "Memory Allocation", "description": "Learn how memory is allocated when creating C++ variables.", "timeRequired": "PT6H" }, { "@type": "Syllabus", "name": "C++ Pointers", "description": "Learn what a C++ pointer is and when they are used.", "timeRequired": "PT11H" } \], "review": \[ { "@type": "Review", "author": { "@type": "Person", "name": "Lou S." }, "datePublished": "2024-08-31", "reviewRating": { "@type": "Rating", "bestRating": 10, "ratingValue": 6 } }\], "coursePrerequisites": \[ "Basic understanding of C++ up to arrays and functions.", "https://www.example.com/beginnerCpp" \], "educationalCredentialAwarded": \[{ "@type": "EducationalOccupationalCredential", "name": "CourseProvider Certificate", "url": "www.example.com", "credentialCategory": "Certificate", // offers only needed if the credential costs extra money. "offers": \[{ "@type": "Offer", "category": "Paid", "price": 5, "priceCurrency": "USD" }\] }\], "video": { "@type": "VideoObject", "name": "Video name", "description": "A video previewing this course.", "uploadDate": "2024-03-28T08:00:00+08:00", "contentUrl": "www.example.come/mp4", "thumbnailUrl": "www.example.com/thumbnailurl.jpg" }, "hasCourseInstance": \[ { // Blended, instructor-led course meeting 3 hours per day in July. "@type": "CourseInstance", "courseMode": "Blended", "location": "Example University", "courseSchedule": { "@type": "Schedule", "duration": "PT3H", "repeatFrequency": "Daily", "repeatCount": 31, "startDate": "2024-07-01", "endDate": "2024-07-31" }, "instructor": \[{ "@type": "Person", "name": "Ira D.", "description": "Professor at X-University", "image": "http://example.com/person.jpg" }\] }, { // Online self-paced course that takes 2 days to complete. "@type": "CourseInstance", "courseMode": "Online", "courseWorkload": "P2D" }\], // Only required for course programs that link to child courses. "hasPart": \[{ "@type": "Course", "name": "C++ Algorithms", "url": "https://www.example.com/cpp-algorithms", "description": "Learn how to code base algorithms in c++.", "provider": { "@type": "Organization", "name": "Example University", "url": "www.example.com" } }, { "@type": "Course", "name": "C++ Data Structures", "url": "https://www.example.com/cpp-data-structures", "description": "Learn about core c++ data structures.", "provider": { "@type": "Organization", "name": "Example University", "url": "www.example.com" } }\] } \</script\> \</head\> \<body\> \</body\> \</html\>   

```text
<html>
  <head>
    <title>Introduction to Computer Science and Programming</title>
    <script type="application/ld+json">
    {
      "@context": "https://schema.org/",
      "@id": "https://www.example.com/advancedCpp",
      "@type": "Course",
      "name": "Learn Advanced C++ Topics",
      "description": "Improve your C++ skills by learning advanced topics.",
      "publisher": {
        "@type": "Organization",
        "name": "CourseWebsite",
        "url": "www.examplecoursewebsite.com"
      },
      "provider": {
        "@type": "Organization",
        "name": "Example University",
        "url": "www.example.com"
      },
      "image": [
        "https://example.com/photos/1x1/photo.jpg",
        "https://example.com/photos/4x3/photo.jpg",
        "https://example.com/photos/16x9/photo.jpg"
      ],
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": 4,
        "ratingCount": 1234,
        "reviewCount": 450
      },
      "offers": [{
        "@type": "Offer",
        "category": "Paid",
        "priceCurrency": "EUR",
        "price": 10.99
      }],
      "totalHistoricalEnrollment": 12345,
      "datePublished": "2024-03-21",
      "educationalLevel": "Advanced",
      "about": ["C++ Coding", "Backend Engineering"],
      "teaches": ["Practice and apply systems thinking to plan for change",
                  "Understand how memory allocation works."],
      "financialAidEligible": "Scholarship Available",
      "inLanguage": "en",
      "availableLanguage": ["fr", "es"],
      "syllabusSections": [
        {
          "@type": "Syllabus",
          "name": "Memory Allocation",
          "description": "Learn how memory is allocated when creating C++ variables.",
          "timeRequired": "PT6H"
        },
        {
          "@type": "Syllabus",
          "name": "C++ Pointers",
          "description": "Learn what a C++ pointer is and when they are used.",
          "timeRequired": "PT11H"
        }
      ],
      "review": [
      {
        "@type": "Review",
        "author": {
            "@type": "Person",
            "name": "Lou S."
        },
        "datePublished": "2024-08-31",
        "reviewRating": {
          "@type": "Rating",
          "bestRating": 10,
          "ratingValue": 6
        }
      }],
      "coursePrerequisites": [
        "Basic understanding of C++ up to arrays and functions.",
        "https://www.example.com/beginnerCpp"
      ],
      "educationalCredentialAwarded": [{
        "@type": "EducationalOccupationalCredential",
        "name": "CourseProvider Certificate",
        "url": "www.example.com",
        "credentialCategory": "Certificate",
        // offers only needed if the credential costs extra money.
        "offers": [{
          "@type": "Offer",
          "category": "Paid",
          "price": 5,
          "priceCurrency": "USD"
        }]
      }],
      "video": {
        "@type": "VideoObject",
        "name": "Video name",
        "description": "A video previewing this course.",
        "uploadDate": "2024-03-28T08:00:00+08:00",
        "contentUrl": "www.example.come/mp4",
        "thumbnailUrl": "www.example.com/thumbnailurl.jpg"
      },
      "hasCourseInstance": [
      {
        // Blended, instructor-led course meeting 3 hours per day in July.
        "@type": "CourseInstance",
        "courseMode": "Blended",
        "location": "Example University",
        "courseSchedule": {
          "@type": "Schedule",
          "duration": "PT3H",
          "repeatFrequency": "Daily",
          "repeatCount": 31,
          "startDate": "2024-07-01",
          "endDate": "2024-07-31"
        },
        "instructor": [{
          "@type": "Person",
          "name": "Ira D.",
          "description": "Professor at X-University",
          "image": "http://example.com/person.jpg"
        }]
      },
      {
        // Online self-paced course that takes 2 days to complete.
        "@type": "CourseInstance",
        "courseMode": "Online",
        "courseWorkload": "P2D"
      }],
      // Only required for course programs that link to child courses.
      "hasPart": [{
        "@type": "Course",
        "name": "C++ Algorithms",
        "url": "https://www.example.com/cpp-algorithms",
        "description": "Learn how to code base algorithms in c++.",
        "provider": {
          "@type": "Organization",
          "name": "Example University",
          "url": "www.example.com"
        }
      }, {
        "@type": "Course",
        "name": "C++ Data Structures",
        "url": "https://www.example.com/cpp-data-structures",
        "description": "Learn about core c++ data structures.",
        "provider": {
          "@type": "Organization",
          "name": "Example University",
          "url": "www.example.com"
        }
      }]
    }
    </script>
  </head>
  <body>
  </body>
</html>
```

Guidelines
----------


You must follow these guidelines for your course to be eligible to appear as a course info rich result on Google Search.

- [Content guidelines](#content-guidelines)
- [Search Essentials](/search/docs/essentials)
- [General structured data guidelines](/search/docs/appearance/structured-data/sd-policies)

| **Warning:** If your site violates one or more of these guidelines, then Google may take [manual action](https://support.google.com/webmasters/answer/2604824) against it. Once you have remedied the problem, you can submit your site for [reconsideration](https://support.google.com/webmasters/answer/35843).

### Content guidelines

Only educational content that fits the following
definition of a course is eligible for the Course info rich result: a series or unit of
curriculum that contains lectures, lessons, or modules in a particular subject or topic.

The `Course` markup must be on a web page that offers a full, single
[course](#course-sd) or [course program](#course-program-sd). The
following examples aren't eligible for the course info rich result:

- An academic degree summary page
- A standalone exam page
- A general public event such as "Astronomy Day"
- A single 2-minute "How to make a Sandwich Video"

| **Note**: Third-party course aggregators (sites that just link to other courses) aren't eligible for the course info rich result.

Structured data type definitions
--------------------------------


You must include the required [`Course`](#course-sd) and [`CourseInstance`](#course-instance-sd)
properties for your content to be eligible for display as a rich result on Google Search. You can
also include the recommended properties to add more information about your content, which could
provide a better user experience.

### `Course`

A course is an individual unit of curriculum that can be taken by itself, or as part of a program.

The full definition of `Course` is available at
[schema.org/Course](https://schema.org/Course).

|                                                                                                                                                                                                                                                                                                                                                                                        Required properties                                                                                                                                                                                                                                                                                                                                                                                        ||
|---------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `name`              | [Text](https://schema.org/Text) The full title of the course. ```text "name": "Intro to Statistics" ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `description`       | [Text](https://schema.org/Text) The description of the course. - **Recommended length**: 240 characters - **Maximum length**: 500 characters ```text "description": "This course teaches the basics of statistical thinking." ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `provider`          | [Organization](https://schema.org/Organization) Information about the organization that created the content for the course. ```carbon "provider": { "@type": "Organization", "name": "Example University", "url": "www.exampleuniversity.com" } ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `provider.name`     | [Text](https://schema.org/Text) The name of the course provider.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `offers`            | Repeatable [Offer](https://schema.org/Offer) Information about the total price to complete the course, including service fees. Don't list a price that is only eligible for some users (for example, 20% off for first time users). Don't include extra certificate fees in this field. If there's an extra charge to earn a certificate, add that to the `educationalCredentialAwarded` property. ```carbon "offers": [{ "@type": "Offer", "category": "Paid", "priceCurrency": "EUR", "price": 10.99 }] ```                                                                                                                                                                                                                                                                |
| `offers.category`   | [Text](https://schema.org/Text) The pricing category of the course. Use one of the following values: - `Free`: All lectures, assignments, and tests must be available without cost for all users. The entire course can be completed without cost. - `Partially Free`: More than half of the course can be completed for free (for example, all lectures are free of charge, but assignments are paid). - `Subscription`: The user must be a subscriber or paid member in order to complete the entire course. - `Paid`: The user must pay to complete the course.                                                                                                                                                                                                           |
| `hasCourseInstance` | Repeatable [CourseInstance](https://schema.org/CourseInstance) Every course must have at least one course instance with information detailing the course offering. See the required and recommended properties in the [`CourseInstance`](#course-instance-sd) section. ```carbon "hasCourseInstance": [{ // Onsite, instructor-led class meeting weekly in August 2023 "@type": "CourseInstance", "courseMode": "Onsite", "location": "Example University", "courseSchedule": { "@type": "Schedule", "duration": "PT5H", "repeatCount": 4, "repeatFrequency": "Weekly", "startDate": "2023-08-01", "endDate": "2023-8-31" }, "instructor": [{ "@type": "Person", "name": "Kai S.", "description": "Professor at X-University", "image": "http://examplePerson.jpg" }] }] ``` |

|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                Recommended properties                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ||
|-----------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `about`                                             | Repeatable [Text](https://schema.org/Text) Describes the skills that the user will develop by taking the course, if applicable. ```text "about": ["Quantitative Analysis", "Critical Thinking"] ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `aggregateRating`                                   | [AggregateRating](https://schema.org/AggregateRating) Information about the average course rating based on ratings left by users who have taken the course, if applicable. Follow the [Review snippet guidelines](/search/docs/appearance/structured-data/review-snippet#guidelines) and list of required and recommended [`AggregateRating` properties](/search/docs/appearance/structured-data/review-snippet#aggregated-rating-type-definition). ```carbon "aggregateRating": { "@type": "AggregateRating", "ratingValue": 4.8, "ratingCount": 255, "reviewCount": 189 } ```                                                                                                                                                                                                                                                                                                                                                                                 |
| `availableLanguage`                                 | Repeatable [Text](https://schema.org/Text) Subtitles, closed captions, or other languages the course is offered in, if applicable. Use the two-letter codes from the list of [ISO 639-1 alpha-2](https://wikipedia.org/wiki/List_of_ISO_639-1_codes#Table) codes. ```text "availableLanguage": ["fr", "es", "de"] ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `coursePrerequisites`                               | Repeatable [Text](https://schema.org/Text) Any prior knowledge that is needed for the course, if applicable. This can be represented by describing the prior knowledge or linking to another course (or both). ```gdscript "coursePrerequisites": ["Understanding of Algebra concepts like variables and functions", "https://www.coursewebsite.abc/algebra"] ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `datePublished`                                     | [Date](https://schema.org/Date) The date that the course was first published, if applicable. Use the [8601 date format](https://wikipedia.org/wiki/ISO_8601) (YYYY-MM-DD). ```text "datePublished": "2019-03-21" ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `educationalCredentialAwarded`                      | Repeatable [EducationalOccupationalCredential](https://schema.org/EducationalOccupationalCredential) Information about the certificate or credential the user can receive by completing the course, if applicable. If the award costs extra, specify the extra price. ```carbon "educationalCredentialAwarded": [{ "@type": "EducationalOccupationalCredential", "name": "CourseProvider Certificate", "url": "www.examplecertificate.com", "credentialCategory": "Certificate", "offers": [{ "@type": "Offer", "category": "Paid", "priceCurrency": "USD", "price": 5 }] }] ```                                                                                                                                                                                                                                                                                                                                                                                |
| `educationalCredentialAwarded.credentialCategory`   | [Text](https://schema.org/Text) The type of award the user will receive, if applicable. Use one of the following values: - `Certificate`: Award verifying the user's successful completion of the course or program. - `Certification`: Official credential that requires an exam or attests that the user has achieved competency.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `educationalCredentialAwarded.name`                 | [Text](https://schema.org/Text) The name of the award, if applicable.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `educationalCredentialAwarded.offers.category`      | [Text](https://schema.org/Text) The type of pricing for the award, if applicable. Use one of the following categories: - `Free`: The award is available without cost. - `Subscription`: The user must be a subscriber or paid member in order to receive the award. - `Paid`: The user must pay to receive the award.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `educationalCredentialAwarded.offers.price`         | [Number](https://schema.org/Number) | This property is only required for an award that costs money. The numeric price of the award, if applicable.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `educationalCredentialAwarded.offers.priceCurrency` | [Text](https://schema.org/Text) | This property is only required for an award that costs money. The currency of the price of the award, in [ISO 4217 currency format](https://wikipedia.org/wiki/ISO_4217#List_of_ISO_4217_currency_codes) (3 letter code), if applicable.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `educationalCredentialAwarded.url`                  | [URL](https://schema.org/URL) The link to the award page, if applicable.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `educationalLevel`                                  | [Text](https://schema.org/Text) The target education level for the course, if applicable. Select one of the following values. - `Beginner`: No prior knowledge is needed to understand the content - `Intermediate`: Some knowledge might be needed to understand the content - `Advanced`: This content is targeted towards advanced learners that have prior knowledge in the topic ```text "educationalLevel": "Beginner" ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `financialAidEligible`                              | [Text](https://schema.org/Text) Any scholarships, special payment plans, or other financial aid opportunities for users looking to take the course, if applicable. ```text "financialAidEligible": "Scholarships available for eligible users." ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `image`                                             | Repeatable [URL](https://schema.org/URL) The URL to an image that is representative of the course, if applicable. Use images that are relevant to the course, rather than logos or captions. Additional image guidelines: - Image URLs must be crawlable and indexable. To check if Google can access your URLs, use the [URL Inspection tool](https://support.google.com/webmasters/answer/9012289). - Images must represent the marked up content. - Images must be in a file format that's [supported by Google Images](/search/docs/appearance/google-images#supported-image-formats). - For best results, we recommend providing multiple high-resolution images (minimum of 50K pixels when multiplying width and height) with the following aspect ratios: 16x9, 4x3, and 1x1. For example: ```text "image": [ "https://example.com/photos/1x1/photo.jpg", "https://example.com/photos/4x3/photo.jpg", "https://example.com/photos/16x9/photo.jpg" ] ``` |
| `inLanguage`                                        | [Text](https://schema.org/Text) The main language the course is offered in, if applicable. Use the two-letter codes from the list of [ISO 639-1 alpha-2](https://wikipedia.org/wiki/List_of_ISO_639-1_codes#Table) codes. ```text "inLanguage": "en" ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `offers.price`                                      | [Number](https://schema.org/Number) | This property is only required for paid courses. The numerical price of the course, if applicable. Don't include other information in this field, such as the currency symbol.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `offers.priceCurrency`                              | [Text](https://schema.org/Text) | This property is only required for paid courses. The currency of the price of the course, in [ISO 4217 currency format](https://wikipedia.org/wiki/ISO_4217#List_of_ISO_4217_currency_codes) (3 letter code), if applicable.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `provider.url`                                      | [URL](https://schema.org/URL) The URL that links to the home page of the course provider, if applicable.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `publisher`                                         | [Organization](https://schema.org/Organization) Information about the organization that publishes and displays the course, if applicable. ```carbon "publisher": { "@type": "Organization", "name": "Course Website", "url": "www.example.com" } ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `publisher.name`                                    | [Text](https://schema.org/Text) The name of the course publisher, if applicable.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `publisher.url`                                     | [URL](https://schema.org/URL) The URL that links to the home page of the course publisher, if applicable.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `review`                                            | Repeatable [Review](https://schema.org/Review) A list of user reviews about the course, if applicable. Follow the [review snippet guidelines](/search/docs/appearance/structured-data/review-snippet#review-properties) for more information. ```carbon "review": [{ "@type": "Review", "author": { "@type": "Person", "name": "Sasha J." }, "datePublished": "2021-09-22", "reviewRating": { "@type": "Rating", "ratingValue": 4 } }] ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `syllabusSections`                                  | Repeatable `Syllabus` Information about the different modules that make up the course, if applicable. ```carbon "syllabusSections": [{ "@type": "Syllabus", "name": "Algebra Review", "description": "Review prerequisite Algebra concepts.", "timeRequired": "PT2H30M" }, { "@type": "Syllabus", "name": "Statistics Terms", "description": "Learn the definitions of basic statistics terms.", "timeRequired": "PT5H" }] ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `syllabusSections.description`                      | [Text](https://schema.org/Text) A description of what the module is about, if applicable.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `syllabusSections.name`                             | [Text](https://schema.org/Text) The name of the course module, if applicable.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `syllabusSections.timeRequired`                     | [Duration](https://schema.org/Duration) Use the [8601 duration format](https://wikipedia.org/wiki/ISO_8601#Durations), if applicable. For example, `PT2H30M` means the module will take 2 hours and 30 minutes to fully complete.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `teaches`                                           | Repeatable [Text](https://schema.org/Text) The learning outcomes or specific knowledge the user will learn by taking the course, if applicable. ```gdscript "teaches": ["How to use visualization tools and graphs", "Why stats is important"] ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `totalHistoricalEnrollment`                         | [Integer](https://schema.org/Integer) The total number of users that have enrolled over the lifetime of the course, if applicable. ```text "totalHistoricalEnrollment": 80032 ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `video`                                             | [VideoObject](https://schema.org/VideoObject) A video preview or trailer for the course, if applicable. Follow the [`VideoObject` guidelines](/search/docs/appearance/structured-data/video#video-object) for more details. ```gdscript "video": { "@type": "VideoObject", "name": "Video name", "description": "A video previewing this course.", "uploadDate": "2022-03-28T08:00:00+08:00", "contentUrl": "www.videourl.mp4", "thumbnailUrl": "www.thumbnailurl.jpg" } ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |

### `CourseInstance`

The full definition of `CourseInstance` is available at
[schema.org/CourseInstance](https://schema.org/CourseInstance).
Every course must have at least one `CourseInstance` with the required properties filled out.

|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              Required properties                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               ||
|----------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `courseMode`                     | [Text](https://schema.org/Text) The medium through which the course will be delivered. Use one of the following values: - `Online`: All class lectures, assignments, and tests can be completed virtually. - `Onsite`: The course is taught in person at a physical location. - `Blended`: The course has both online and in-person components. If the class is `Onsite` or `Blended`, add the `location` property. ```text "courseMode": "Online" ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `courseSchedule`                 | [Schedule](https://schema.org/Schedule) | Only one of `courseSchedule` or `courseWorkload` properties is required. We recommend the `courseSchedule` property if you want to highlight pacing (for example, 4 hours per week), or start and end dates. Otherwise, `courseWorkload` works for most cases. Information about how long the course takes the average user to complete, given a suggested pacing. Include start and end dates for courses that are on a fixed timeline. **Here's an example of a paced course that can be started at any time:** ```carbon // This course takes 6 weeks to complete. "courseSchedule": { "@type": "Schedule", "repeatCount": 6 "repeatFrequency": "Weekly", } ``` **Here's an example of a paced course during a set time:** ```carbon // This course expects 1 hour per day during July 2023 "courseSchedule": { "@type": "Schedule", "duration": "PT1H", "repeatCount": 31 "repeatFrequency": "Daily", "startDate": "2023-07-01", "endDate": "2023-07-31" } ``` |
| `courseSchedule.repeatCount`     | [Integer](https://schema.org/Integer) The numerical value for how long the course lasts for, in `repeatFrequency` units. For example, if the `repeatFrequency` is monthly and the `repeatCount` is 4, the course lasts for 4 months.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `courseSchedule.repeatFrequency` | [Text](https://schema.org/Text) The `duration` and `repeatCount` properties are relative to this field. Use one of the following values: - `Daily`: The course happens daily. - `Weekly`: The course happens weekly. - `Monthly`: The course happens monthly. - `Yearly`: The course happens yearly.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `courseWorkload`                 | [Text](https://schema.org/Text) | Only one of `courseSchedule` or `courseWorkload` properties is required. We recommend the `courseSchedule` property if you want to highlight pacing (for example, 4 hours per week), or start and end dates. Otherwise, `courseWorkload` works for most cases. This field represents the total time to watch all videos and complete all assignments and exams for the course. Use the [8601 duration format](https://wikipedia.org/wiki/ISO_8601#Durations). ```gdscript "courseWorkload": "PT22H" ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |

|                                                                                                                                                                                                                                                                                                                                                                                                                                    Recommended properties                                                                                                                                                                                                                                                                                                                                                                                                                                     ||
|----------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `courseSchedule.duration`  | [Duration](https://schema.org/Duration) The suggested pacing for how long the average user can expect to spend in `repeatFrequency` units, in [8601 duration format](https://wikipedia.org/wiki/ISO_8601#Durations), if applicable. For example, if the `repeatFrequency` is monthly and the `duration` is `PT5H`, the user should expect to spend 5 hours per month. Don't specify the entire length of the course with this property. Use the `courseWorkload` property instead.                                                                                                                                                                                                                                                                                                                                                                                |
| `courseSchedule.endDate`   | [Date](https://schema.org/Date) The end date for the course, in [8601 date format](https://wikipedia.org/wiki/ISO_8601) (YYYY-MM-DD), if applicable.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `courseSchedule.startDate` | [Date](https://schema.org/Date) The start date for the course, in [8601 date format](https://wikipedia.org/wiki/ISO_8601) (YYYY-MM-DD), if applicable.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `image`                    | [URL](https://schema.org/URL) The URL that links to an image of the instructor, if applicable. Additional image guidelines: - Image URLs must be crawlable and indexable. To check if Google can access your URLs, use the [URL Inspection tool](https://support.google.com/webmasters/answer/9012289). - Images must represent the marked up content. - Images must be in a file format that's [supported by Google Images](/search/docs/appearance/google-images#supported-image-formats). - For best results, we recommend providing multiple high-resolution images (minimum of 50K pixels when multiplying width and height) with the following aspect ratios: 16x9, 4x3, and 1x1. For example: ```text "image": [ "https://example.com/photos/1x1/photo.jpg", "https://example.com/photos/4x3/photo.jpg", "https://example.com/photos/16x9/photo.jpg" ] ``` |
| `instructor`               | Repeatable [Person](https://schema.org/Person) Information about the instructor for the course, if applicable. ```carbon "instructor": [{ "@type": "Person", "name": "Dana A.", "description": "Professor at X-University", "image": "http://examplePerson.jpg" }] ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `instructor.description`   | [Text](https://schema.org/Text) The description of the instructor and their credentials, if applicable.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `instructor.name`          | [Text](https://schema.org/Text) The name of the instructor, if applicable.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `location`                 | [Text](https://schema.org/Text) | This property is only required for `Onsite` or `Blended` courses. The name or address (or both) of the physical location where the course will be taught, if applicable. ```text "courseMode": "Blended", "location": "Example High School" ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |

### Course Program


A course program is a collection of child courses. The child courses must be standalone
courses with distinct URLs and landing pages.


If your web page is a course program, include the following required properties (in addition
to the other required properties listed in the [`Course`](#course-sd) and
[`CourseInstance`](#course-instance-sd) sections).

|                                                                                                                                                                                                                                                                                                            Required properties                                                                                                                                                                                                                                                                                                             ||
|----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `hasPart`      | Repeatable [Course](https://schema.org/Course) The list of child courses that are a part of this program. ```carbon "@context": "https://schema.org/", "@type": "Course", "name": "Learning Pathway: Knitting", "url": "www.example.com/knitprogram" // Fill the other required Course and CourseInstance properties "hasPart": [{ "@type": "Course", "name": "Intro to Knitting", "url": "www.example.com/knitbasics", "description": "Learn the basics of how to knit." }, { "@type": "Course", "name": "Knit a Sweater", "url": "www.example.com/knitsweater", "description": "Learn to knit an entire sweater." }] ``` |
| `hasPart.name` | [Text](https://schema.org/Text) The full title of the child course.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `hasPart.url`  | [URL](https://schema.org/URL) The URL that links to the child course landing page.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |

|                                                                                          Recommended properties                                                                                          ||
|-----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `hasPart.description` | [Text](https://schema.org/Text) A brief description of what the child course covers, if applicable. - **Recommended length**: 240 characters - **Maximum length**: 500 characters |

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

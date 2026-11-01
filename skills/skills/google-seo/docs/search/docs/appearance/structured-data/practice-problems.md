# Practice problem (`Quiz`) structured data

| **Upcoming deprecation:**We're phasing out support for the practice problem structured data type in Google Search.

To help students, teachers and parents find your education and learning material online easier, you can use structured data to mark up practice problems. This guide explains how you can implement this schema on your web page. Adding structured data makes your practice problems eligible to appear in a special user experience in Google Search results.
![Practice problems rich result in Google Search](https://developers.google.com/static/search/docs/images/practice-problems.png)**Note** : The actual appearance in search results might be different. You can preview most features with the[Rich Results Test](https://support.google.com/webmasters/answer/7445569).

## How to add structured data

Structured data is a standardized format for providing information about a page and classifying the page content. If you're new to structured data, you can learn more about[how structured data works](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data).

Here's an overview of how to build, test, and release structured data.

1. Add the[required properties](https://developers.google.com/search/docs/appearance/structured-data/practice-problems#structured-data-type-definitions). Based on the format you're using, learn where to[insert structured data on the page](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data#format-placement).**Using a CMS?** It may be easier to use a plugin that's integrated into your CMS.  
   | **Using JavaScript?** Learn how to[generate structured data with JavaScript](https://developers.google.com/search/docs/appearance/structured-data/generate-structured-data-with-javascript).
2. Follow the[guidelines](https://developers.google.com/search/docs/appearance/structured-data/practice-problems#guidelines).
3. Validate your code using the[Rich Results Test](https://search.google.com/test/rich-results)and fix any critical errors. Consider also fixing any non-critical issues that may be flagged in the tool, as they can help improve the quality of your structured data (however, this isn't necessary to be eligible for rich results).
4. Deploy a few pages that include your structured data and use the[URL Inspection tool](https://support.google.com/webmasters/answer/9012289)to test how Google sees the page. Be sure that your page is accessible to Google and not blocked by a robots.txt file, the`noindex`tag, or login requirements. If the page looks okay, you can[ask Google to recrawl your URLs](https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl).**Note**: Allow time for re-crawling and re-indexing. Remember that it may take several days after publishing a page for Google to find and crawl it.
5. To keep Google informed of future changes, we recommend that you[submit a sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap). You can automate this with the[Search Console Sitemap API](https://developers.google.com/webmaster-tools/v1/sitemaps).

## Feature availability

The practice problem feature is available in English in all regions where Google Search is available. The feature is only available for math and science topics, for multiple choice and checkbox question types, and on desktop and mobile.

## Examples

### Quiz with only one question

Here's an example of a quiz that only has one question associated with it. There is only one correct answer.
\<html\> \<head\> \<title\>Quiz about fractions\</title\> \<script type="application/ld+json"\> { "@context": "https://schema.org/", "@type": "Quiz", "name": "Quiz about fractions", "hasPart": { "@type": "Question", "typicalAgeRange": "7-12", "educationalAlignment": \[ { "@type": "AlignmentObject", "alignmentType": "educationalSubject", "targetName": "Mathematics" }, { "@type": "AlignmentObject", "alignmentType": "educationalSubject", "targetName": "Algebra" }, { "@type": "AlignmentObject", "alignmentType": "educationalLevel", "targetName": "Grade 5 \>\> Number and Operations---Fractions \>\> Apply and extend previous understandings of multiplication and division. \>\> 3", "educationalFramework": "Common Core", "targetUrl": "https://www.corestandards.org/Math/Content/5/NF/B/3/" } \], "about": { "@type": "Thing", "name": "Fractions" }, "educationalLevel": "intermediate", "eduQuestionType": "Multiple choice", "learningResourceType": "Practice problem", "assesses": "Multiplying fractions by whole numbers", "name": "Choose the model", "comment": { "@type": "Comment", "text": "This is a hint about the question." }, "encodingFormat": "text/markdown", "text": "Which model represents the product $$2 \* \\\\frac{2}{3}$$?", "suggestedAnswer": \[ { "@type": "Answer", "position": 0, "encodingFormat": "text/html", "text": "\<img src=\\"www.test.com/practice-problems-fractions/...image2.png\\" alt=\\"Answer 2\\" /\>", "comment": { "@type": "Comment", "text": "This is a hint about the answer." } } \], "acceptedAnswer": { "@type": "Answer", "position": 1, "encodingFormat": "text/html", "text": "\<img src=\\"www.test.com/practice-problems-fractions/...image1.png\\" alt=\\"Answer 1\\" /\>", "comment": { "@type": "Comment", "text": "This is a hint about the answer." }, "answerExplanation": { "@type": "Comment", "text": "This is a full explanation on how this answer was achieved." } } } } \</script\> \</head\> \<body\> \</body\> \</html\>  

```text
<html>
  <head>
    <title>Quiz about fractions</title>
    <script type="application/ld+json">
    {
      "@context": "https://schema.org/",
      "@type": "Quiz",
      "name": "Quiz about fractions",
      "hasPart": {
        "@type": "Question",
        "typicalAgeRange": "7-12",
        "educationalAlignment": [
          {
            "@type": "AlignmentObject",
            "alignmentType": "educationalSubject",
            "targetName": "Mathematics"
          },
          {
            "@type": "AlignmentObject",
            "alignmentType": "educationalSubject",
            "targetName": "Algebra"
          },
          {
            "@type": "AlignmentObject",
            "alignmentType": "educationalLevel",
            "targetName": "Grade 5 » Number and Operations—Fractions » Apply and extend previous understandings of multiplication and division. » 3",
            "educationalFramework": "Common Core",
            "targetUrl": "https://www.corestandards.org/Math/Content/5/NF/B/3/"
          }
        ],
        "about": {
          "@type": "Thing",
          "name": "Fractions"
        },
        "educationalLevel": "intermediate",
        "eduQuestionType": "Multiple choice",
        "learningResourceType": "Practice problem",
        "assesses": "Multiplying fractions by whole numbers",
        "name": "Choose the model",
        "comment": {
          "@type": "Comment",
          "text": "This is a hint about the question."
        },
        "encodingFormat": "text/markdown",
        "text": "Which model represents the product $$2 * \\frac{2}{3}$$?",
        "suggestedAnswer": [
          {
            "@type": "Answer",
            "position": 0,
            "encodingFormat": "text/html",
            "text": "<img src=\"www.test.com/practice-problems-fractions/…image2.png\" alt=\"Answer 2\" />",
            "comment": {
              "@type": "Comment",
              "text": "This is a hint about the answer."
            }
          }
        ],
        "acceptedAnswer": {
          "@type": "Answer",
          "position": 1,
          "encodingFormat": "text/html",
          "text": "<img src=\"www.test.com/practice-problems-fractions/…image1.png\" alt=\"Answer 1\" />",
          "comment": {
            "@type": "Comment",
            "text": "This is a hint about the answer."
          },
          "answerExplanation": {
            "@type": "Comment",
            "text": "This is a full explanation on how this answer was achieved."
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

### Quiz with only one question and checkbox answers

Here's an example of a quiz that only has one question associated with it. There are multiple correct answers.
\<html\> \<head\> \<title\>Quiz about laws of Physics\</title\> \<script type="application/ld+json"\> { "@context": "https://schema.org/", "@type": "Quiz", "name": "Quiz about laws of physics", "about": { "@type": "Thing", "name": "Laws of Physics And Applications" }, "educationalLevel": "intermediate", "assesses": "Laws of physics", "hasPart": { "@type": "Question", "eduQuestionType": "Checkbox", "learningResourceType": "Practice problem", "name": "Laws of Physics And Applications", "typicalAgeRange": "12-15", "text": "Identify laws of Physics. (Select all valid answers)", "suggestedAnswer": \[ { "@type": "Answer", "position": 0, "text": "Nevada's Law", "comment": { "@type": "Comment", "text": "This is a hint" } }, { "@type": "Answer", "position": 2, "text": "EUA law", "comment": { "@type": "Comment", "text": "This is a hint" } } \], "acceptedAnswer": \[ { "@type": "Answer", "position": 1, "text": "Newton's law", "comment": { "@type": "Comment", "text": "This is a hint" }, "answerExplanation": { "@type": "Comment", "text": "This is a full explanation on how this answer was achieved." } }, { "@type": "Answer", "position": 3, "text": "Ohm's law", "comment": { "@type": "Comment", "text": "This is a hint" }, "answerExplanation": { "@type": "Comment", "text": "This is a full explanation on how this answer was achieved." } } \] } } \</script\> \</head\> \<body\> \</body\> \</html\>  

```text
<html>
  <head>
    <title>Quiz about laws of Physics</title>
    <script type="application/ld+json">
    {
      "@context": "https://schema.org/",
      "@type": "Quiz",
      "name": "Quiz about laws of physics",
      "about": {
        "@type": "Thing",
        "name": "Laws of Physics And Applications"
      },
      "educationalLevel": "intermediate",
      "assesses": "Laws of physics",
      "hasPart": {
        "@type": "Question",
        "eduQuestionType": "Checkbox",
        "learningResourceType": "Practice problem",
        "name": "Laws of Physics And Applications",
        "typicalAgeRange": "12-15",
        "text": "Identify laws of Physics. (Select all valid answers)",
        "suggestedAnswer": [
          {
            "@type": "Answer",
            "position": 0,
            "text": "Nevada's Law",
            "comment": {
              "@type": "Comment",
              "text": "This is a hint"
            }
          },
          {
            "@type": "Answer",
            "position": 2,
            "text": "EUA law",
            "comment": {
              "@type": "Comment",
              "text": "This is a hint"
            }
          }
        ],
        "acceptedAnswer": [
          {
            "@type": "Answer",
            "position": 1,
            "text": "Newton's law",
            "comment": {
              "@type": "Comment",
              "text": "This is a hint"
            },
            "answerExplanation": {
              "@type": "Comment",
              "text": "This is a full explanation on how this answer was achieved."
            }
          },
          {
            "@type": "Answer",
            "position": 3,
            "text": "Ohm's law",
            "comment": {
              "@type": "Comment",
              "text": "This is a hint"
            },
            "answerExplanation": {
              "@type": "Comment",
              "text": "This is a full explanation on how this answer was achieved."
            }
          }
        ]
      }
    }
    </script>
  </head>
  <body>
  </body>
</html>
```

### Quiz with multiple questions

Here's an example of a quiz that has multiple question and answer pairs.
\<html\> \<head\> \<title\>Quiz about displacement, velocity and time\</title\> \<script type="application/ld+json"\> { "@context": "https://schema.org/", "@type": "Quiz", "typicalAgeRange": "7-12", "educationalLevel": "intermediate", "assesses": "Velocity and speed", "educationalAlignment": \[ { "@type": "AlignmentObject", "alignmentType": "educationalSubject", "targetName": "Science" }, { "@type": "AlignmentObject", "alignmentType": "educationalSubject", "targetName": "Physics" } \], "name": "Quiz about displacement, velocity and time", "about": { "@type": "Thing", "name": "Displacement, velocity, and time" }, "hasPart": \[ { "@type": "Question", "eduQuestionType": "Multiple choice", "learningResourceType": "Practice problem", "name": "Average velocity and average speed from graphs", "text": "A bug crawls on a wall. What is the average velocity of the bug between the times $$t = 1s$$ and $$t = 10s$$?", "comment": { "@type": "Comment", "text": "This is a hint about the question." }, "encodingFormat": "text/markdown", "suggestedAnswer": \[ { "@type": "Answer", "position": 0, "encodingFormat": "text/markdown", "text": "$$0.5 \\\\frac{m}{s}$$", "comment": { "@type": "Comment", "text": "This is a hint" } }, { "@type": "Answer", "position": 1, "encodingFormat": "text/markdown", "text": "$$-0.5 \\\\frac{m}{s}$$", "comment": { "@type": "Comment", "text": "This is a hint" } }, { "@type": "Answer", "position": 3, "encodingFormat": "text/markdown", "text": "$$1.5 \\\\frac{m}{s}$$", "comment": { "@type": "Comment", "text": "This is a hint" } } \], "acceptedAnswer": { "@type": "Answer", "position": 2, "encodingFormat": "text/markdown", "text": "$$0 \\\\frac{m}{s}$$", "comment": { "@type": "Comment", "text": "This is a hint" } } }, { "@type": "Question", "eduQuestionType": "Multiple choice", "learningResourceType": "Practice problem", "name": "Average velocity and average speed from graphs", "text": "A swimmer motion is shown on the following graph of position x vs. time t. What is the average speed?", "encodingFormat": "text/markdown", "comment": { "@type": "Comment", "text": "This is a hint about the question." }, "suggestedAnswer": \[ { "@type": "Answer", "position": 0, "text": "1", "encodingFormat": "text/html", "comment": { "@type": "Comment", "text": "This is a hint" } }, { "@type": "Answer", "position": 2, "text": "3", "encodingFormat": "text/html", "comment": { "@type": "Comment", "text": "This is a hint" } }, { "@type": "Answer", "position": 3, "text": "4", "encodingFormat": "text/html", "comment": { "@type": "Comment", "text": "This is a hint" } } \], "acceptedAnswer": { "@type": "Answer", "position": 1, "text": "2", "encodingFormat": "text/html", "comment": { "@type": "Comment", "text": "This is a hint" }, "answerExplanation": { "@type": "Comment", "text": "This is a full explanation on how this answer was achieved." } } } \] } \</script\> \</head\> \<body\> \</body\> \</html\>  

```text
<html>
  <head>
    <title>Quiz about displacement, velocity and time</title>
    <script type="application/ld+json">
    {
      "@context": "https://schema.org/",
      "@type": "Quiz",
      "typicalAgeRange": "7-12",
      "educationalLevel": "intermediate",
      "assesses": "Velocity and speed",
      "educationalAlignment": [
        {
          "@type": "AlignmentObject",
          "alignmentType": "educationalSubject",
          "targetName": "Science"
        },
        {
          "@type": "AlignmentObject",
          "alignmentType": "educationalSubject",
          "targetName": "Physics"
        }
      ],
      "name": "Quiz about displacement, velocity and time",
      "about": {
        "@type": "Thing",
        "name": "Displacement, velocity, and time"
      },
      "hasPart": [
        {
          "@type": "Question",
          "eduQuestionType": "Multiple choice",
          "learningResourceType": "Practice problem",
          "name": "Average velocity and average speed from graphs",
          "text": "A bug crawls on a wall. What is the average velocity of the bug between the times $$t = 1s$$ and $$t = 10s$$?",
          "comment": {
            "@type": "Comment",
            "text": "This is a hint about the question."
          },
          "encodingFormat": "text/markdown",
          "suggestedAnswer": [
            {
              "@type": "Answer",
              "position": 0,
              "encodingFormat": "text/markdown",
              "text": "$$0.5 \\frac{m}{s}$$",
              "comment": {
                "@type": "Comment",
                "text": "This is a hint"
              }
            },
            {
              "@type": "Answer",
              "position": 1,
              "encodingFormat": "text/markdown",
              "text": "$$-0.5 \\frac{m}{s}$$",
              "comment": {
                "@type": "Comment",
                "text": "This is a hint"
              }
            },
            {
              "@type": "Answer",
              "position": 3,
              "encodingFormat": "text/markdown",
              "text": "$$1.5 \\frac{m}{s}$$",
              "comment": {
                "@type": "Comment",
                "text": "This is a hint"
              }
            }
          ],
          "acceptedAnswer": {
            "@type": "Answer",
            "position": 2,
            "encodingFormat": "text/markdown",
            "text": "$$0 \\frac{m}{s}$$",
            "comment": {
              "@type": "Comment",
              "text": "This is a hint"
            }
          }
        },
        {
          "@type": "Question",
          "eduQuestionType": "Multiple choice",
          "learningResourceType": "Practice problem",
          "name": "Average velocity and average speed from graphs",
          "text": "A swimmer motion is shown on the following graph of position x vs. time t. What is the average speed?",
          "encodingFormat": "text/markdown",
          "comment": {
            "@type": "Comment",
            "text": "This is a hint about the question."
          },
          "suggestedAnswer": [
            {
              "@type": "Answer",
              "position": 0,
              "text": "1",
              "encodingFormat": "text/html",
              "comment": {
                "@type": "Comment",
                "text": "This is a hint"
              }
            },
            {
              "@type": "Answer",
              "position": 2,
              "text": "3",
              "encodingFormat": "text/html",
              "comment": {
                "@type": "Comment",
                "text": "This is a hint"
              }
            },
            {
              "@type": "Answer",
              "position": 3,
              "text": "4",
              "encodingFormat": "text/html",
              "comment": {
                "@type": "Comment",
                "text": "This is a hint"
              }
            }
          ],
          "acceptedAnswer": {
            "@type": "Answer",
            "position": 1,
            "text": "2",
            "encodingFormat": "text/html",
            "comment": {
              "@type": "Comment",
              "text": "This is a hint"
            },
            "answerExplanation": {
              "@type": "Comment",
              "text": "This is a full explanation on how this answer was achieved."
            }
          }
        }
      ]
    }
    </script>
  </head>
  <body>
  </body>
</html>
```

## Guidelines

You must follow these guidelines to be eligible to appear in the Practice problems experience on Google:

- [General structured data guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies)
- [Search Essentials](https://developers.google.com/search/docs/essentials)
- [Technical guidelines](https://developers.google.com/search/docs/appearance/structured-data/practice-problems#technical-guidelines)
- [Content guidelines](https://developers.google.com/search/docs/appearance/structured-data/practice-problems#content-guidelines)

### Technical guidelines

- Put structured data on the most detailed leaf page possible. Don't add structured data to pages without practice problems.
- Add a`Quiz`property for each practice problem that you want to be featured. The structured data must appear on the same page as the practice problem a user can interact with on your web page.
- Your web page includes all[required structured data properties](https://developers.google.com/search/docs/appearance/structured-data/practice-problems#structured-data-type-definitions).
- You must mark up a minimum of two practice problems per topic (for example, two practice problems for the concept "quadratic equation"). Focus on marking up the concepts and problems that you want to be eligible to appear in the Practice Problem rich result. They can be on separate pages.
- The practice problems on your site must be accessible to users, meaning not held only in a data file or PDF.
- Ensure that Googlebot can[crawl your site efficiently](https://developers.google.com/search/docs/crawling-indexing/troubleshoot-crawling-errors#improve_crawl_efficiency).
- If you have several copies of the same practice problem on your site hosted under different URLs, use[canonical URLs](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)on each copy of the page.
- For text-only practice problems:
  - The question must be limited to 320 characters max.
  - Multiple choice answers must be limited to 70 characters max, per answer.
- For practice problems with text and an image:
  - The question must be limited to 160 characters max.
  - The image max height must be 200px.
- **Accessibility**: We don't allow practice problems that are hidden behind a login or paywall. Once users navigate from the feature on Google to your site, the practice problem content must be accessible to them. Additional content can be behind a login or paywall.
- **Misrepresentation**: We don't allow practice problems that are intended to deceive or mislead users. This includes inaccurately marking up topics that are unassociated to the question.

### Content guidelines

We created these Practice problems content guidelines to ensure that our users are connected with learning resources that are relevant. If we find content that violates these policies, we'll respond appropriately, which may include taking[manual action](https://support.google.com/webmasters/answer/9044175)and removing your pages from appearing in the practice problems experience on Google.

#### Profanity and vulgar language

We don't allow practice problems that contain obscene, profane, or offensive language.

#### Advertisements disguised as a practice problem

We don't allow promotional content disguised as a practice problem, such as those posted by a third party (for example,[affiliate programs](https://developers.google.com/search/docs/essentials/spam-policies#thin-affiliate-pages)).

#### Legal removal requests

If Google receives a complaint that content in a practice problem may violate the law, the content will be handled in accordance with[Search policies](https://support.google.com/legal/answer/3110420).

#### Quality

- You are responsible for the accuracy and quality of your practice problems through this feature. If a certain amount of your data is found to be inaccurate based on our quality review processes, then either all or a subset of your problems may be removed from the feature until you resolve the issues depending on the severity. This applies to the accuracy of:
  - The concept marked up as it relates to the question being asked
  - Question, answer choice, hint, and answer explanation formatting and accuracy
  - Correct order of answers (for example, don't put "None of the above" as the first option)
  - Image or formula quality and accuracy as it relates to the question
  - Symbolic math rendering and delimiter implementation

## Mark up educational standards

Learning standards are the learning goals for what students should know and be able to do at each grade level. Learning standards have multiple uses, such as linking to content or making up a part of a learning progression. Marking up the standards (found under the[`educationalAlignment`](https://developers.google.com/search/docs/appearance/structured-data/practice-problems#educational-alignment)and[`hasPart.educationalAlignment`](https://developers.google.com/search/docs/appearance/structured-data/practice-problems#haspart-educational-alignment)fields) associated with online learning material helps Google organize and surface the information in the most useful way to people who may Search for learning content based on these standards. Here's a high-level overview of the schema:

Here are a few examples of standards:

- Common Core State Standards
- Texas Essential Knowledge and Skills (TEKS)
- Virginia Standards of Learning (SOL)
- BC Performance Standards
- Alberta Programs of Studies
- The Australian Curriculum (ACARA)
- The Victorian Curriculum (F-10)
- UK National Curriculum

## Structured data type definitions

You must include the required properties for your content to be eligible for display as a rich result. You can also include the recommended properties to add more information to your structured data, which could provide a better user experience.

### `Quiz`

A`Quiz`is a grouping of practice problems (one or more), which are typically about the same concept or subject.

The full definition of[Quiz](https://schema.org/Quiz)is provided on schema.org.

|                                                                                                                                                                                                                                                                                                                                                     Required properties                                                                                                                                                                                                                                                                                                                                                     ||
|--------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `about`                        | [Thing](https://schema.org/Thing) Nested information about the underlying concept behind the`Quiz`. If there's an[`hasPart.about`](https://developers.google.com/search/docs/appearance/structured-data/practice-problems#haspart-about)property for the question, this property isn't required. ```carbon { "@type": "Quiz", "about": { "@type": "Thing" } } ```                                                                                                                                                                                                                                                                                                                           |
| `about.name`                   | [Text](https://schema.org/Text) Nested information about the underlying concept behind the`Quiz`. If there's an[`hasPart.about.name`](https://developers.google.com/search/docs/appearance/structured-data/practice-problems#haspart-about-name)property for the question, this property isn't required. Multiple entries of this property is allowed. ```carbon { "@type": "Quiz", "about": { "@type": "Thing", "name": "Fractions" } } ```                                                                                                                                                                                                                                                |
| `hasPart`                      | [Question](https://schema.org/Question) Nested information about the specific practice problem for the quiz. Use one`hasPart`property to represent a single practice problem. To include multiple practice problems for a single quiz, repeat this property. ```carbon { "@type": "Quiz", "hasPart": { "@type": "Question" } } ```                                                                                                                                                                                                                                                                                                                                                          |
| `hasPart.acceptedAnswer`       | [Answer](https://schema.org/Answer) The correct answer for the question. If there are multiple correct answers for a single question, repeat this property. ```carbon { "@type": "Quiz", "hasPart": { "@type": "Question", "acceptedAnswer": { "@type": "Answer" } } } ```                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `hasPart.eduQuestionType`      | [Text](https://schema.org/Text) The type of practice problem. This is critical for Google Search to render and check correct and incorrect answers. For each question, Google will show a minimum of two answers and a maximum of six answers. Use one of the supported values: - `Multiple choice`: There's only one correct answer. The choices are shown as a collection of radio buttons, and the user can only select one. - `Checkbox`: There's more than one correct answer. The choices are shown as a collection of checkboxes, and the user can check all that apply. ```carbon { "@type": "Quiz", "hasPart": { "@type": "Question", "eduQuestionType": "Multiple choice" } } ``` |
| `hasPart.learningResourceType` | [Text](https://schema.org/Text) The type of this learning resource. Use this fixed value:`Practice problem` ```carbon { "@type": "Quiz", "hasPart": { "@type": "Question", "learningResourceType": "Practice problem" } } ```                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `hasPart.suggestedAnswer`      | [Answer](https://schema.org/Answer) All the other correct or incorrect answers for the question. To specify multiple answers, repeat this property, along with its nested properties.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `hasPart.suggestedAnswer.text` | [Text](https://schema.org/Text) The content of the answer. You can use Markdown or HTML. Learn how to[encode practice problems in HTML or Markdown](https://developers.google.com/search/docs/appearance/structured-data/practice-problems#encoding-html-markdown). ```carbon { "@type": "Quiz", "hasPart": { "@type": "Question", "suggestedAnswer": { "@type": "Answer", "text": "$$x = 1$$" } } } ```                                                                                                                                                                                                                                                                                    |
| `hasPart.text`                 | [Text](https://schema.org/Text) The content of the question. You can use Markdown or HTML. Learn how to[encode practice problems in HTML or Markdown](https://developers.google.com/search/docs/appearance/structured-data/practice-problems#encoding-html-markdown). ```carbon { "@type": "Quiz", "hasPart": { "@type": "Question", "text": "Which diagram represents the product $$3 *\frac{2}{3}$$?" } } ```                                                                                                                                                                                                                                                                             |

|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          Recommended properties                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          ||
|-----------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `educationalAlignment`                              | [AlignmentObject](https://schema.org/AlignmentObject) The quiz's alignment to an established educational framework. This property can be repeated to align the quiz with a field of study or domain, and the target grade or[educational standard](https://developers.google.com/search/docs/appearance/structured-data/practice-problems#mark-up-educational-standards). You can add educational alignments directly on the`Quiz`, or more specifically in the`Question`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `educationalAlignment.alignmentType`                | [Text](https://schema.org/Text) A category of alignment between the learning resource and the framework node for the quiz. Google Search uses the[LRMI standard](https://www.dublincore.org/specifications/lrmi/lrmi_1/). Repeat the`alignmentType`to specify both the field of study and the target grade or educational standard. - To specify the field of study or domain of the quiz, set the`alignmentType`to`educationalSubject`. - To specify the target grade or educational standard of the quiz, set the`alignmentType`to`educationalLevel`. Multiple objects can be inserted in case other domains and subdomains exist. To specify concepts, use the[`about`](https://developers.google.com/search/docs/appearance/structured-data/practice-problems#about-property)property instead. Here's how to specify both the`educationalSubject`and`educationalLevel`. ```carbon { "@type": "Quiz", "educationalAlignment": [ { "@type": "AlignmentObject", "alignmentType": "educationalSubject", "targetName": "Mathematics" }, { "@type": "AlignmentObject", "alignmentType": "educationalLevel", "targetName": "Fifth grade" } ] } ``` To refer to standards, such as the "Common core", use the[`educationalAlignment.educationalFramework`](https://developers.google.com/search/docs/appearance/structured-data/practice-problems#educationalalignment-educationalframework)and[`educationalAlignment.targetUrl `](https://developers.google.com/search/docs/appearance/structured-data/practice-problems#educationalalignment-targeturl)properties. ```carbon { "@type": "Quiz", "educationalAlignment: [ { "@type": "AlignmentObject", "alignmentType": "educationalLevel", "educationalFramework": "Common Core", "targetName": "Grade 8: Expressions and Equations", "targetUrl": "https://www.corestandards.org/Math/Content/8/EE/A/2/" } ] } ```                                                                                  |
| `educationalAlignment.educationalFramework`         | [Text](https://schema.org/Text) The framework that the quiz is aligned to. For example, "Common Core". For more information about why this property is important, see[Mark up educational standards](https://developers.google.com/search/docs/appearance/structured-data/practice-problems#mark-up-educational-standards). Multiple entries of this property is allowed.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `educationalAlignment.targetName`                   | [Text](https://schema.org/Text) The name of a node of an established educational framework. For example: "Grade 8: Expressions and Equations". ```carbon { "@type": "Quiz", "educationalAlignment: [ { "@type": "AlignmentObject", "targetName": "Grade 8: Expressions and Equations" } ] } ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `educationalAlignment.targetUrl`                    | [URL](https://schema.org/URL) The URL of the specific educational framework. For example, the URL for the Common Core standard on 8th grade math. ```carbon { "@type": "Quiz", "educationalAlignment: [ { "@type": "AlignmentObject", "targetUrl": "https://www.corestandards.org/Math/Content/8/EE/A/2/" } ] } ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `educationalLevel`                                  | [Text](https://schema.org/Text) The level of difficulty of the quiz. Here are a few example values that can be used: - `beginner` - `intermediate` - `advanced` ```carbon { "@type": "Quiz", "educationalLevel": "beginner" } ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `hasPart.about`                                     | [Thing](https://schema.org/Thing) Nested information about the underlying concept behind the question. If the[`about`](https://developers.google.com/search/docs/appearance/structured-data/practice-problems#about-property)property isn't specified for the`Quiz`, then`hasPart.about`is required. Multiple entries of this property is allowed.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `hasPart.about.name`                                | [Text](https://schema.org/Text) The title of the underlying concept behind the question. If the[`about.name`](https://developers.google.com/search/docs/appearance/structured-data/practice-problems#about-name-property)property isn't specified for the`Quiz`, then`hasPart.about.name`is required. ```carbon { "@type": "Quiz", "hasPart": { "@type": "Question", "about": { "@type": "Thing", "name": "Fractions" } } } ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `hasPart.acceptedAnswer.answerExplanation`          | [Comment](https://schema.org/Comment) A full explanation about how to achieve the result depicted in this answer. This is typically only used for correct answers. Use the[`hasPart.suggestedAnswer.comment.text`](https://developers.google.com/search/docs/appearance/structured-data/practice-problems#haspart-answerexplanation-text)property inside for the content of the explanation.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `hasPart.acceptedAnswer.answerExplanation.text`     | [Text](https://schema.org/Text) The content of explanation for the suggested answer. To change the content format (HTML or Markdown), use`encodingFormat`. Learn how to[encode practice problems in HTML or Markdown](https://developers.google.com/search/docs/appearance/structured-data/practice-problems#encoding-html-markdown). ```carbon { "@type": "Quiz", "hasPart": { "@type": "Question", "suggestedAnswer": { "@type": "Answer", "answerExplanation": { "@type": "Comment", "text": "*In order to get to this result..*", "encodingFormat": "text/markdown" } } } } ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `hasPart.acceptedAnswer.comment`                    | [Comment](https://schema.org/Comment) A hint or suggestion about the answer that may be used to understand why it is correct. Use the[`hasPart.acceptedAnswer.comment.text`](https://developers.google.com/search/docs/appearance/structured-data/practice-problems#haspart-accceptedanswer-comment-text)property inside for the hint content.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `hasPart.acceptedAnswer.comment.text`               | [Text](https://schema.org/Text) The content of the hint or suggestion for the suggested answer. To change the content format (HTML or Markdown), use`encodingFormat`. Learn how to[encode practice problems in HTML or Markdown](https://developers.google.com/search/docs/appearance/structured-data/practice-problems#encoding-html-markdown). ``` { "@type": "Quiz", "hasPart": { "@type": "Question", "acceptedAnswer": { "@type": "Answer", "comment": { "@type": "Comment", "text": "<p>This is a hint</p>" } } } } ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `hasPart.acceptedAnswer.position`                   | [Integer](https://schema.org/Integer) The position of this answer when it's displayed to the user. ```carbon { "@type": "Quiz", "hasPart": { "@type": "Question", "acceptedAnswer": { "@type": "Answer", "position": 2 } } } ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `hasPart.assesses`                                  | [DefinedTerm](https://schema.org/DefinedTerm)or[Text](https://schema.org/Text) The skill(s) required to solve the problem. Filling this in can enhance discoverability. ```carbon { "@type": "Quiz", "hasPart": { "@type": "Question", "assesses": "Multiplying fractions by whole numbers" } } ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `hasPart.comment`                                   | [Comment](https://schema.org/Comment) A hint or suggestion about the question that may be used to solve it. Use the[`hasPart.comment.text`](https://developers.google.com/search/docs/appearance/structured-data/practice-problems#haspart-comment-text)property inside for the hint content.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `hasPart.comment.text`                              | [Text](https://schema.org/Text) The content of the hint or suggestion for the question. To change the content format (HTML or Markdown), use`encodingFormat`. Learn how to[encode practice problems in HTML or Markdown](https://developers.google.com/search/docs/appearance/structured-data/practice-problems#encoding-html-markdown). ``` { "@type": "Quiz", "hasPart": { "@type": "Question", "comment": { "@type": "Comment", "text": "<p>This is a hint</p>" } } } ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `hasPart.educationalAlignment`                      | [AlignmentObject](https://schema.org/AlignmentObject) The question's alignment to an established educational framework. This property overrides educational alignments that were added on the`Quiz`object.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `hasPart.educationalAlignment.alignmentType`        | [Text](https://schema.org/Text) A category of alignment between the learning resource and the framework node for the question. Google Search uses the[LRMI standard](https://www.dublincore.org/specifications/lrmi/lrmi_1/). Repeat the`alignmentType`to specify both the field of study and the target grade or educational standard. - To specify the field of study or domain of the question, set the`alignmentType`to`educationalSubject`. - To specify the target grade or educational standard of the question, set the`alignmentType`to`educationalLevel`. Multiple objects can be inserted in case other domains and subdomains exist. To specify concepts, use the[`hasPart.about`](https://developers.google.com/search/docs/appearance/structured-data/practice-problems#haspart-about)property instead. Here's how to specify both the`educationalSubject`and`educationalLevel`. ```carbon { "@type": "Quiz", "hasPart": { "@type": "Question", "educationalAlignment": [ { "@type": "AlignmentObject", "alignmentType": "educationalSubject", "targetName": "Mathematics" }, { "@type": "AlignmentObject", "alignmentType": "educationalLevel", "targetName": "Fifth grade" } ] } } ``` To refer to standards, such as the "Common core", use the[`hasPart.educationalAlignment.educationalFramework`](https://developers.google.com/search/docs/appearance/structured-data/practice-problems#haspart-educational-framework)and[`hasPart.educationalAlignment.targetUrl`](https://developers.google.com/search/docs/appearance/structured-data/practice-problems#haspart-targeturl)properties. ```carbon { "@type": "Quiz", "hasPart": { "@type": "Question", "educationalAlignment: [ { "@type": "AlignmentObject", "alignmentType": "educationalLevel", "educationalFramework": "Common Core", "targetName": "Grade 8: Expressions and Equations", "targetUrl": "https://www.corestandards.org/Math/Content/8/EE/A/2/" } ] } } ``` |
| `hasPart.educationalAlignment.educationalFramework` | [Text](https://schema.org/Text) The framework that the question is aligned to. For example, "Common Core". For more information about why this property is important, see[Mark up educational standards](https://developers.google.com/search/docs/appearance/structured-data/practice-problems#mark-up-educational-standards). Multiple entries of this property is allowed.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `hasPart.educationalAlignment.targetName`           | [Text](https://schema.org/Text) The name of a node of an established educational framework. For example: "Grade 8: Expressions and Equations". ```carbon { "@type": "Quiz", "hasPart": { "@type": "Question", "educationalAlignment: [ { "@type": "AlignmentObject", "alignmentType": "educationalLevel", "targetName": "Grade 8: Expressions and Equations" } ] } } ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `hasPart.educationalAlignment.targetUrl`            | [URL](https://schema.org/URL) The URL of the specific educational framework that applies to the question. For example, the URL for the Common Core standard on 8th grade math.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `hasPart.educationalLevel`                          | [Text](https://schema.org/Text) The level of difficulty of the question, in text form. Here are a few example values that can be used: - `beginner` - `intermediate` - `advanced` ```carbon { "@type": "Quiz", "hasPart": { "@type": "Question", "educationalLevel": "beginner" } } ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `hasPart.name`                                      | [Text](https://schema.org/Text) An overview description of the question. Don't include the full content of the question; use[`hasPart.text`](https://developers.google.com/search/docs/appearance/structured-data/practice-problems#haspart-text)instead. ```carbon { "@type": "Quiz", "hasPart": { "@type": "Question", "name": "Question about fractions" } } ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `hasPart.suggestedAnswer.comment`                   | [Comment](https://schema.org/Comment) A hint or suggestion about the answer that may be used to understand why it is correct or incorrect. Use the[`hasPart.suggestedAnswer.comment.text`](https://developers.google.com/search/docs/appearance/structured-data/practice-problems#haspart-suggestedAnswer-comment-text)property inside for the hint content.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `hasPart.suggestedAnswer.comment.text`              | [Text](https://schema.org/Text) The content of the hint or suggestion for the suggested answer. To change the content format (HTML or Markdown), use`encodingFormat`. Learn how to[encode practice problems in HTML or Markdown](https://developers.google.com/search/docs/appearance/structured-data/practice-problems#encoding-html-markdown). ``` { "@type": "Quiz", "hasPart": { "@type": "Question", "suggestedAnswer": { "@type": "Answer", "comment": { "@type": "Comment", "text": "<p>This is a hint</p>" } } } } ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `hasPart.suggestedAnswer.encodingFormat`            | [Text](https://schema.org/Text) The MIME format used to encode the text property. If no`encodingFormat`is specified, the default value is`text/html`. Use one of the following values: - `text/markdown` - `text/html` ```carbon { "@type": "Quiz", "hasPart": { "@type": "Question", "suggestedAnswer": { "@type": "Answer", "encodingFormat": "text/html" } } } ``` Learn how to[encode practice problems in HTML or Markdown](https://developers.google.com/search/docs/appearance/structured-data/practice-problems#encoding-html-markdown).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `hasPart.suggestedAnswer.position`                  | [Integer](https://schema.org/Integer) The position of this answer when it is displayed to the user. ```carbon { "@type": "Quiz", "hasPart": { "@type": "Question", "suggestedAnswer": { "@type": "Answer", "position": "0" } } } ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `hasPart.typicalAgeRange`                           | [Text](https://schema.org/Text) The typical range of ages that the question is intended for. For example:`7-12`or`18-` ```carbon { "@type": "Quiz", "hasPart": { "@type": "Question", "typicalAgeRange": "7-12" } } ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `name`                                              | [Text](https://schema.org/Text) The title of the quiz. ```carbon { "@type": "Quiz", "name": "Negative exponents review" } ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `typicalAgeRange`                                   | [Text](https://schema.org/Text) The typical range of ages the quiz is intended for. For example:`7-12`or`18-` ```carbon { "@type": "Quiz", "typicalAgeRange": "7-12" } ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |

## Encoding practice problems in HTML or Markdown

Google Search supports Markdown ([CommonMark](https://commonmark.org/)flavor) and HTML when encoding[Question](https://schema.org/Question),[Answer](https://schema.org/Answer), and[Comment](https://schema.org/Comment). We restrict the set of constructs to:

- Headers
- Line breaks
- Lists (ordered and unordered)
- Paragraphs
- Bold
- Italic
- Images
- Formulas in LaTex

CSS or JavaScript is ignored. Google won't display questions that contain unsupported HTML tags.

### How to specify the format

To specify which encoding format you're using, use the`encodingFormat`property and set the value to either`"text/html"`for HTML or`"text/markdown"`for Markdown.

Here's an example of a question that's set to the Markdown format:  

```carbon
{
  "@type": "Question",
  "name": "Average velocity and average speed from graphs",
  "text": "What is the average velocity [..] between the times $$t = 4s$$ and $$t = 10s$$?",
  "encodingFormat": "text/markdown"
  ..
  ..
}
```

If no`encodingFormat`is specified,`"text/html"`is assumed.

### Formulas

To specify a formula, use the LaTex format. You must use the double dollar sign (`$$`) to embed formulas. For example:  

```
"<p>Please solve: $$2x^2 = 18$$</p>"
```
| **Important:**Rich Results Test will show warnings for long or complex math expressions without formula delimiters.

## Troubleshooting

If you're having trouble implementing or debugging structured data, here are some resources that may help you.

- If you're using a content management system (CMS) or someone else is taking care of your site, ask them to help you. Make sure to forward any Search Console message that details the issue to them.
- Google does not guarantee that features that consume structured data will show up in search results. For a list of common reasons why Google may not show your content in a rich result, see the[General Structured Data Guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies).
- You might have an error in your structured data. Check the[list of structured data errors](https://support.google.com/webmasters/answer/13300873)and the[Unparsable structured data report](https://support.google.com/webmasters/answer/9166415).
- If you received a structured data manual action against your page, the structured data on the page will be ignored (although the page can still appear in Google Search results). To fix[structured data issues](https://support.google.com/webmasters/answer/9044175#zippy=%2Cstructured-data-issue), use the[Manual Actions report](https://support.google.com/webmasters/answer/9044175).
- Review the[guidelines](https://developers.google.com/search/docs/appearance/structured-data/practice-problems#guidelines)again to identify if your content isn't compliant with the guidelines. The problem can be caused by either spammy content or spammy markup usage. However, the issue may not be a syntax issue, and so the Rich Results Test won't be able to identify these issues.
- [Troubleshoot missing rich results / drop in total rich results](https://support.google.com/webmasters/answer/13300208).
- Allow time for re-crawling and re-indexing. Remember that it may take several days after publishing a page for Google to find and crawl it. For general questions about crawling and indexing, check the[Google Search crawling and indexing FAQ](https://developers.google.com/search/help/crawling-index-faq).
- Post a question in the[Google Search Central forum](https://support.google.com/webmasters/community).

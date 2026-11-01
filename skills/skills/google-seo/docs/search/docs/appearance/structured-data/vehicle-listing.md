# Vehicle Listing Schema Markup | Google Search Central

Vehicle listing (`Car`) structured data
=======================================

| **Upcoming deprecation** : We're phasing out support for a few structured data types in Google Search. Learn more about [what's changing in our blog post](/search/blog/2025/06/simplifying-search-results).
An illustration of a vehicle listing rich result in Google Search $16,998 • 75.3k miles
Car Shop
$9,987 • 120k miles
Auto Dealer


Vehicle listing structured data allows car dealerships to make their sale vehicle inventory eligible
for display on various Google surfaces, including Google Search and dealerships' Business Profiles.
People can then search, filter, and easily learn more about vehicles for sale such as availability, pricing,
and key information about the vehicles for sale, potentially directing customers to your business.
| This documentation is for organic listings in Google Search. If you're looking for information about Vehicle ads, visit the [Vehicle ads help center](https://support.google.com/merchants/answer/11189169).

Feature availability
--------------------


The vehicle listing rich result is currently only available in English in the US and US
territories. The feature is available on both mobile and desktop.

Two ways of providing inventory data to Google
----------------------------------------------


There are two methods for car dealerships to provide their car inventory data to Google. One is
through structured data markup on their websites, which is the main focus of this document, and the
other is through feed files uploaded to the [vehicle listings partner portal](https://carcenter.webapps.google.com/signup/).
Both methods enable car inventory data to be displayed on Google surfaces.


Here are some characteristics of the two methods:

|                                                                                                                                                                                                          Method and description                                                                                                                                                                                                           ||
|----------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Structured data markup** | - It's relatively easy to implement and maintain structured data markup on websites - It could take longer for Google to detect changes on websites - No 1:1 support                                                                                                                                                                                                                                          |
| **Feed file uploads**      | - It may require system development to create and maintain feed files. - All inventory data in feed files is recognized by Google - 1:1 support is available to address any issues with feed uploads at the vehicle listings partner portal - Feeds support more detailed properties for vehicle inventory Learn more about how to [upload a vehicle listings file feed](/vehicle-listings/onboarding-guide). |


Feed files would be a suitable option if you are comfortable with creating and maintaining them
technically. Structured web markup would be a suitable option if you prioritize ease of
implementation. If you choose to use both methods, make sure the data is consistent between feeds
and markup. If there are any discrepancies, the feed data will override the conflicting markup data.

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

Here's an example single vehicle listing page with markup.
\<html\> \<head\> \<title\>1999 Dodge Ram Pickup 2500 ST\</title\> \<script type="application/ld+json"\>{ "@context": "https://schema.org", "@type": "Car", "name": "1999 Dodge Ram Pickup 2500 ST", "vehicleIdentificationNumber": "1BXKF23ZXXJ000000", "image": \[ "https://example.com/image1.png", "https://example.com/image2.png" \], "url": "https://www.example.com/used-vehicle-1999-dodge-ram-pickup-2500-st-c-67/", "offers": { "@type": "Offer", "availability": "https://schema.org/InStock", "price": 10000, "priceCurrency": "USD" }, "itemCondition": "https://schema.org/NewCondition", "brand": { "@type": "Brand", "name": "Dodge" }, "model": "Ram", "vehicleConfiguration": "ST", "vehicleModelDate": "1999", "mileageFromOdometer": { "@type": "QuantitativeValue", "value": "20170", "unitCode": "SMI" }, "color": "White", "vehicleInteriorColor": "Gray", "vehicleInteriorType": "Standard", "bodyType": "Pickup", "driveWheelConfiguration": "https://schema.org/FourWheelDriveConfiguration", "vehicleEngine": { "@type": "EngineSpecification", "fuelType": "Gasoline" }, "vehicleTransmission": "Manual", "numberOfDoors": 2, "vehicleSeatingCapacity": 2 } \</script\> \</head\> \<body\> \</body\> \</html\>   

```text
<html>
  <head>
    <title>1999 Dodge Ram Pickup 2500 ST</title>
    <script type="application/ld+json">{
      "@context": "https://schema.org",
      "@type": "Car",
      "name": "1999 Dodge Ram Pickup 2500 ST",
      "vehicleIdentificationNumber": "1BXKF23ZXXJ000000",
      "image": [
        "https://example.com/image1.png",
        "https://example.com/image2.png"
      ],
      "url": "https://www.example.com/used-vehicle-1999-dodge-ram-pickup-2500-st-c-67/",
      "offers": {
        "@type": "Offer",
        "availability": "https://schema.org/InStock",
        "price": 10000,
        "priceCurrency": "USD"
      },
      "itemCondition": "https://schema.org/NewCondition",
      "brand": {
        "@type": "Brand",
        "name": "Dodge"
      },
      "model": "Ram",
      "vehicleConfiguration": "ST",
      "vehicleModelDate": "1999",
      "mileageFromOdometer": {
        "@type": "QuantitativeValue",
        "value": "20170",
        "unitCode": "SMI"
      },
      "color": "White",
      "vehicleInteriorColor": "Gray",
      "vehicleInteriorType": "Standard",
      "bodyType": "Pickup",
      "driveWheelConfiguration": "https://schema.org/FourWheelDriveConfiguration",
      "vehicleEngine": {
        "@type": "EngineSpecification",
        "fuelType": "Gasoline"
      },
      "vehicleTransmission": "Manual",
      "numberOfDoors": 2,
      "vehicleSeatingCapacity": 2
    }
  </script>
  </head>
  <body>
  </body>
</html>
```

Guidelines and eligibility requirements
---------------------------------------


There are several eligibility requirements for dealerships to display their car inventory data on Google surfaces:

- The dealership must have a claimed and verified Business Profile on Google in the US or US territories. For details, see [How to verify your business on Google](https://support.google.com/business/answer/7107242).
- The Business Profile must have the Place type [vehicle_dealer](/maps/documentation/places/web-service/supported_types). See [How to choose a category for your Business Profile](https://support.google.com/business/answer/7249669/choose-a-business-category-computer class=). **Note** : We hide the [Business Profile Products](https://support.google.com/business/answer/9124203) when showing vehicle listings on Business Profiles.
- Only include vehicle inventory for sale directly from the dealership. Vehicles from private sellers, individuals, or auto brokers are not permitted.
- Only include vehicle inventory for cars that are for sale in the US or US territories.


For your page to be eligible for vehicle listings rich results, you must also follow the
[Search Essentials](/search/docs/essentials) and [General structured data guidelines](/search/docs/appearance/structured-data/sd-policies).
| **Warning:** If your site violates one or more of these guidelines, then Google may take [manual action](https://support.google.com/webmasters/answer/2604824) against it. Once you have remedied the problem, you can submit your site for [reconsideration](https://support.google.com/webmasters/answer/35843).

Structured data type definitions
--------------------------------


You must include the required properties for your content to be eligible for display in vehicle
listing rich results. You can also include the recommended properties to add more information about
your content, which could provide a better user experience.

### `Car`

The full definition of [`Car`](https://schema.org/Car) is provided on schema.org.

|                                                                                                                                                                                                                                                                                      Required properties                                                                                                                                                                                                                                                                                      ||
|--------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `brand`                        | [Brand](https://schema.org/Brand) Information about the make of the vehicle.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `brand.name`                   | [Text](https://schema.org/Text) The name of the make of the vehicle, such as "Toyota".                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `itemCondition`                | [OfferItemCondition](https://schema.org/OfferItemCondition) The condition of the vehicle, either new or used. Use one of the following values: - `https://schema.org/NewCondition`: The vehicle is new. - `https://schema.org/UsedCondition`: The vehicle is used (it's not new).                                                                                                                                                                                                                                                                             |
| `mileageFromOdometer`          | [QuantitativeValue](https://schema.org/QuantitativeValue) Information about the total distance traveled by the vehicle since its initial production, as read from its odometer. | This property is required if the car is a used car.                                                                                                                                                                                                                                                                                                                         |
| `mileageFromOdometer.unitCode` | [Text](https://schema.org/Text) The unit of distance given using the UN/CEFACT Common Code (three characters). Use one of the following values: - **For miles** : `SMI` - **For kilometers** : `KMT`                                                                                                                                                                                                                                                                                                                                                          |
| `mileageFromOdometer.value`    | [Number](https://schema.org/Number) The numerical value of distance, as read by the odometer. | **Note** : We exclude [any new vehicle with more than 20,000 miles](/vehicle-listings/reference/policy#mileage-policies).                                                                                                                                                                                                                                                                                                                                     |
| `model`                        | [Text](https://schema.org/Text) The model of the vehicle, such as "Civic". Don't include trim specifics like LX or EX.                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `offers`                       | [Offer](https://schema.org/Offer) The offer details about the vehicle that's for sale.                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `offers.availability`          | [ItemAvailability](https://schema.org/ItemAvailability) The availability of the vehicle. Use one of the following values: - `https://schema.org/InStock`: The vehicle is in stock - `https://schema.org/OutOfStock`: The vehicle is currently out of stock.                                                                                                                                                                                                                                                                                                   |
| `offers.price`                 | [Number](https://schema.org/Number) The final sale price for the vehicle. Vehicle listings must meet our price policies: - We want to show the lowest possible price that is publicly available to all consumers. Any discount shown needs to apply to all consumers. For instance, don't factor in veteran discounts. - We exclude vehicles with prices that fall outside of the range of prices that we expect, based on similar vehicles that are available for sale.                                                                                      |
| `offers.priceCurrency`         | [Text](https://schema.org/Text) The currency of the sale price in three-letter ISO 4217 format.                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `vehicleIdentificationNumber`  | [Text](https://schema.org/Text) The Vehicle Identification Number (VIN), which is a unique alphanumeric identifier for each vehicle. The vehicle must have a valid [Vehicle Identification Number](/vehicle-listings/reference/feed-specification#vin): - Vehicle parts, accessories, tires, and services aren't supported. - Vehicle auctions and auction pricing aren't supported. - Vehicles available for rent, lease or subscription aren't supported. - Examples of supported vehicle types: passenger cars and trucks, RV, ATV, motorcycles, trailers. |
| `vehicleModelDate`             | [Date](https://schema.org/Date) The model year in the format `YYYY`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |

|                                                                                                                                                                                                                                                                                                                                     Recommended properties                                                                                                                                                                                                                                                                                                                                     ||
|---------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `bodyType`                | [Text](https://schema.org/Text) The body style of the vehicle, such as sedan, suv, or crossover. Currently, Google only supports `bodyType` values in English. Here are some example values: - `convertible` - `coupe` - `crossover` - `full size van` - `hatchback` - `minivan` - `sedan` - `suv` - `truck`                                                                                                                                                                                                                                                                                                                                                        |
| `color`                   | [Text](https://schema.org/Text) The OEM-specified exterior color, such as White, Platinum, or Metallic Tri-Coat.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `driveWheelConfiguration` | [DriveWheelConfigurationValue](https://schema.org/DriveWheelConfigurationValue) The drive wheel configuration (for example, which roadwheels will receive torque from the vehicle's engine via the drivetrain). Use one of the following values: - `https://schema.org/AllWheelDriveConfiguration`: The vehicle has an all-wheel drive configuration. - `https://schema.org/FourWheelDriveConfiguration`: The vehicle has four-wheel drive configuration. - `https://schema.org/FrontWheelDriveConfiguration`: The vehicle has front-wheel drive configuration. - `https://schema.org/RearWheelDriveConfiguration`: The vehicle has rear-wheel drive configuration. |
| `image`                   | [URL](https://schema.org/URL) or [ImageObject](https://schema.org/ImageObject) The image(s) for the vehicle. The image(s) must meet our [image policies and specifications](/vehicle-listings/reference/policy#image-policies). If you're having issues, see [how to fix an invalid image](/vehicle-listings/support/how-to-fix#how_to_fix_invalid_image). | Googlebot must be allowed to crawl the page. A missing image can cause the vehicle listing to be ranked lower in the vehicle listing rich result.                                                                                                                                                      |
| `name`                    | [Text](https://schema.org/Text) The name of the vehicle as it's displayed on the website. For example, `Used 2020 BMW 530i w/ Convenience Package`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `numberOfDoors`           | [Number](https://schema.org/Number) The number of doors.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `url`                     | [URL](https://schema.org/URL) The link to the dealer's Vehicle Details Page (VDP).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `vehicleConfiguration`    | [Text](https://schema.org/Text) The trim of the model, such as `S`, `SV`, or `SL`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `vehicleEngine`           | [EngineSpecification](https://schema.org/EngineSpecification) Information about the vehicle's engine specification.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `vehicleEngine.fuelType`  | [Text](https://schema.org/Text) The type of fuel that's suitable for the engine of the vehicle.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `vehicleInteriorColor`    | [Text](https://schema.org/Text) The OEM-specified interior color, such as `Brown` or `Ivory`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `vehicleInteriorType`     | [Text](https://schema.org/Text) The type or material of the interior of the vehicle (for example, synthetic fabric, leather, wood). While most interior types are characterized by the material used, an interior type can also be based on vehicle usage or target audience.                                                                                                                                                                                                                                                                                                                                                                                       |
| `vehicleSeatingCapacity`  | [Number](https://schema.org/Number) The number of seats.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `vehicleTransmission`     | [Text](https://schema.org/Text) The transmission specification. For example, 9-speed automatic or manual.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |

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

# Google Ads Scripts - Bulk Upload Workaround for Video Campaigns

## Overview
Google Ads Scripts directly prohibit the creation of Video Campaigns via standard builders (e.g., `AdsApp.newCampaignBuilder()`).

However, **you can programmatically create Video Campaigns from within a Google Ads Script by dynamically generating a CSV payload and processing it through the `AdsApp.bulkUploads()` service.**

Reference:
- [Google Ads Scripts - Video Campaigns Limitations](https://developers.google.com/google-ads/scripts/docs/campaigns/video-campaigns)
- [Google Ads Scripts - Bulk Uploads](https://developers.google.com/google-ads/scripts/docs/features/bulk-upload)

## Required Fields for Bulk Upload (Video Campaign Creation)

When generating a CSV for the `BulkUpload` service to create a Video Campaign, you must include specific columns.

**Essential Columns:**
- `Action`: Must be `Add` to create a new campaign.
- `Campaign`: The name of the new campaign.
- `Campaign Type`: Must be `Video`.
- `Campaign Subtype`: E.g., `Video action`, `Video non-skippable`, `Video bumper`.
- `Budget`: The daily budget amount.
- `Budget Type`: E.g., `Daily`.
- `Bidding Strategy Type`: E.g., `Target CPA`, `Target CPV`, `Maximize conversions`.
- `Campaign Status`: E.g., `Enabled`, `Paused`.
- `Networks`: Where the ads will show (e.g., `YouTube Search, YouTube Videos`).
- `Language`: E.g., `en`.
- `Location`: E.g., `US`.

## Enums / Allowed Values
- **Campaign Subtype:** `Video action`, `Video non-skippable`, `Video outstream`, `Video ad sequence`.
- **Bidding Strategy Type:** `Target CPA`, `Target CPV`, `Maximize conversions`, `Maximize conversion value`, `Target CPM`.
- **Networks:** `YouTube Search`, `YouTube Videos`, `Video partners on the Display Network`.

## JavaScript Code Sample: Creating a Video Campaign via Bulk Upload in Google Ads Scripts

```javascript
/**
 * Creates a Video Campaign dynamically using the Bulk Upload workaround.
 */
function main() {
  // 1. Define the parameters for the new Video Campaign
  var campaignName = "My Automated Video Campaign - " + Utilities.formatDate(new Date(), "GMT", "yyyyMMdd-HHmmss");
  var budgetAmount = 50.00; // $50/day
  var biddingStrategy = "Maximize conversions";
  var networks = "YouTube Search;YouTube Videos";

  // 2. Construct the CSV Header
  var csvHeader = [
    "Action",
    "Campaign",
    "Campaign Type",
    "Campaign Subtype",
    "Budget",
    "Budget Type",
    "Bidding Strategy Type",
    "Campaign Status",
    "Networks"
  ].join(",");

  // 3. Construct the CSV Row
  var csvRow = [
    "Add",
    campaignName,
    "Video",
    "Video action",
    budgetAmount,
    "Daily",
    biddingStrategy,
    "Paused", // Start paused for safety
    networks
  ].join(",");

  // 4. Combine into a single CSV string
  var csvContent = csvHeader + "\n" + csvRow;

  // 5. Initialize the Bulk Upload
  Logger.log("Initializing Bulk Upload for Video Campaign creation...");
  var upload = AdsApp.bulkUploads().newCsvUpload(
    [csvHeader, csvRow].join("\n") // Alternative way to pass an array of strings
  );

  // Optional: Set a description for the upload to track it in the UI
  upload.forCampaignManagement();

  // 6. Apply the Bulk Upload
  Logger.log("Applying Bulk Upload...");
  upload.apply();

  Logger.log("Bulk upload initiated. Campaign '" + campaignName + "' should appear in your account shortly.");
}
```

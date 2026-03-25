# Google Ads API v20 Shopping Campaign UI Mapping

This document provides an exhaustive, deeply researched mapping of the user interface (UI) input fields required for setting up a Google Ads Shopping Campaign to the corresponding Google Ads API v20 Python SDK fields (`google-ads==28.0.0`), entities, and ENUMs. It strictly follows the order presented in the provided Google Doc.

## 1. Merchant Center account
- **UI Field**: Merchant Center account selection.
- **API Mapping**: `Campaign.shopping_setting.merchant_id`
- **Entity**: `client.get_type("CampaignOperation").create.shopping_setting`
- **Data Type**: `int64`
- **Hierarchy**: Campaign-level setting.
- **Deep Dive**: This field links the campaign to a specific Google Merchant Center account. To use specific feeds, you can optionally filter by configuring `shopping_setting.feed_label`. This must be a valid, active Merchant Center ID linked to the Google Ads account.

## 2. Choose Shopping/Performance Max
- **UI Field**: Select between Shopping and Performance Max.
- **API Mapping**:
  - For standard Shopping: `Campaign.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.SHOPPING`
  - For Performance Max: `Campaign.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.PERFORMANCE_MAX`
- **Hierarchy**: Campaign-level setting.
- **Deep Dive**: "Smart Shopping" campaigns have been deprecated globally. When users select "Smart Shopping" equivalents, it directly maps to `PERFORMANCE_MAX`. Standard Shopping remains strictly as `SHOPPING`.

## 3. Campaign Name
- **UI Field**: Campaign Name.
- **API Mapping**: `Campaign.name`
- **Entity**: `client.get_type("CampaignOperation").create`
- **Data Type**: `string`
- **Hierarchy**: Campaign-level setting.
- **Deep Dive**: Campaign names must be unique within the account. Duplicate names will result in an API `CampaignError.DUPLICATE_CAMPAIGN_NAME`.

## 4. Budget and Bidding Optimization

### Budget
- **UI Field**: Budget amount and delivery method (Standard).
- **API Mapping**:
  - Create a `CampaignBudget` entity: `client.get_type("CampaignBudgetOperation").create`
  - Amount: `CampaignBudget.amount_micros` (in micros, 1,000,000 micros = $1)
  - Delivery Method: `CampaignBudget.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD`
- **Hierarchy**: Campaign Budget is a separate entity linked to the Campaign via `Campaign.campaign_budget` (by assigning the `resource_name` of the created budget).
- **Deep Dive**: The `ACCELERATED` delivery method is completely deprecated. Sending it will cause an error in v20; standard delivery is required. Budgets can be configured as `explicitly_shared = True` if using shared portfolio budgets.

### Bidding
- **UI Field**: Bidding strategy (e.g., Target ROAS, Maximize Clicks, Manual CPC).
- **API Mapping**:
  - `Campaign.bidding_strategy_type` ENUMs mapping:
    - Target ROAS: `client.enums.BiddingStrategyTypeEnum.TARGET_ROAS` (configure value via `Campaign.target_roas.target_roas` where 3.5 = 350%)
    - Maximize Clicks: `client.enums.BiddingStrategyTypeEnum.TARGET_SPEND` (configure via `Campaign.target_spend.target_spend_micros`)
    - Manual CPC: `client.enums.BiddingStrategyTypeEnum.MANUAL_CPC` (configure via `Campaign.manual_cpc.enhanced_cpc_enabled = False`)
- **Hierarchy**: Campaign-level setting (Standard Bidding) or shared Bidding Strategy entity (Portfolio bidding).

### Customer Acquisition
- **UI Field**: Customer acquisition settings (e.g., bid higher for new customers).
- **API Mapping**: In v20, mapped via the `CustomerAcquisitionGoalSettings` entity (`optimization_mode`, `value_settings`).
- **Hierarchy**: Account or Campaign level.
- **Deep Dive**: Standard Shopping campaigns do not typically support simple toggles for Customer Acquisition in the same way Performance Max does. For PMax replacements, you would utilize `CustomerAcquisitionGoalSettings` to define value rules for new versus returning customers.

### Campaign Priority
- **UI Field**: Campaign priority (Low, Medium, High).
- **API Mapping**: `Campaign.shopping_setting.campaign_priority`
- **Data Type**: `int32` (0 = Low, 1 = Medium, 2 = High)
- **Hierarchy**: Campaign-level setting.
- **Deep Dive**: This determines which campaign bids when multiple campaigns share the same product. It takes an integer rather than an enum string.

## 5. Campaign Settings

### Locations
- **UI Field**: Location targeting.
- **API Mapping**:
  - Create a `CampaignCriterion` entity: `client.get_type("CampaignCriterionOperation").create`
  - Set `CampaignCriterion.location.geo_target_constant` to the specific Geo target resource string.
- **Hierarchy**: Campaign Criterion (separate entity linked to Campaign).
- **Deep Dive**: It's highly recommended to fetch the appropriate `geo_target_constant` IDs (e.g., 2840 for the USA) via `GeoTargetConstantService` before applying criteria.

### Local Products
- **UI Field**: Enable local inventory ads.
- **API Mapping**: `Campaign.shopping_setting.enable_local`
- **Data Type**: `bool`
- **Hierarchy**: Campaign-level setting.

### EU Political Ads
- **UI Field**: EU political ads declaration.
- **API Mapping**: `Campaign.contains_eu_political_advertising`
- **Data Type**: `bool`
- **Hierarchy**: Campaign-level setting.
- **Deep Dive**: **CRITICAL v20 UPDATE:** Due to the European Union Political Ads Regulation, if a Google Ads account has undeclared campaigns, mutate calls (such as adding locations or changing criteria) will fail with a `MutateError.EU_POLITICAL_ADVERTISING_DECLARATION_REQUIRED` error. Developers *must* set this field proactively.

### Start and End Dates
- **UI Field**: Start and end dates for the campaign.
- **API Mapping**:
  - `Campaign.start_date` (format: YYYY-MM-DD)
  - `Campaign.end_date` (format: YYYY-MM-DD)
- **Hierarchy**: Campaign-level setting.

### Campaign URL Options
- **UI Field**: Tracking templates and custom parameters.
- **API Mapping**:
  - Tracking Template: `Campaign.tracking_url_template`
  - Final URL Suffix: `Campaign.final_url_suffix`
  - Custom Parameters: `Campaign.url_custom_parameters` (list of `CustomParameter` objects with `key` and `value`).
- **Hierarchy**: Campaign-level setting.

### Networks
- **UI Field**: Search Network, Search Partners, etc.
- **API Mapping**: `Campaign.network_settings`
  - `network_settings.target_google_search` (`bool`)
  - `network_settings.target_search_network` (`bool` - Maps to Google Search Partners)
  - `network_settings.target_content_network` (`bool` - Maps to Display Expansion)
- **Hierarchy**: Campaign-level setting.

## 6. Ad Group Configuration

### Ad Group Name
- **UI Field**: Name of the Ad Group.
- **API Mapping**: `AdGroup.name`
- **Entity**: `client.get_type("AdGroupOperation").create`
- **Data Type**: `string`
- **Hierarchy**: Ad Group-level setting linked to Campaign.

### Ad Group Bid
- **UI Field**: Default max CPC bid for the Ad Group.
- **API Mapping**: `AdGroup.cpc_bid_micros`
- **Data Type**: `int64` (in micros)
- **Hierarchy**: Ad Group-level setting.
- **Deep Dive**: This bid acts as the fallback maximum CPC for the "All products" group. However, in Shopping, bids are primarily driven by the `ListingGroupInfo` configurations.

### Product Groups
- **UI Field**: Product group subdivision (e.g., "All products").
- **API Mapping**:
  - Create an `AdGroupCriterion` entity: `client.get_type("AdGroupCriterionOperation").create`
  - Configure `AdGroupCriterion.listing_group` (`ListingGroupInfo`)
  - Type: `type_ = client.enums.ListingGroupTypeEnum.SUBDIVISION` or `UNIT`
  - Bidding: Bids (`cpc_bid_micros`) are set explicitly on the `UNIT` nodes (the leaf nodes of the tree).
- **Hierarchy**: Ad Group Criterion (separate entity linked to Ad Group).
- **Deep Dive**: Building listing group trees requires creating subdivisions and units in the exact same batch request using temporary IDs (e.g., `-1`, `-2`). A `ListingGroupInfo` is invalid until it is complete, meaning whenever a subdivision is created, at least one child and an "Other" node must also be created simultaneously.

---

## Anomaly Data & API Nuances

| Feature / Setting | API Limitations & Notes (v20) |
| :--- | :--- |
| **EU Political Ads Enforcement** | In API v20+, failing to declare `contains_eu_political_advertising` will cause geo-targeting mutates (`CampaignCriterionOperation`) to fail entirely for un-declared campaigns. |
| **Customer Acquisition** | Setting up "Bid higher for new customers" in standard shopping requires complex conversion goal tracking via `CustomerAcquisitionGoalSettings`. Not a simple boolean toggle on standard Shopping Campaigns. |
| **Campaign Priority** | Stored as integer (0, 1, 2) rather than explicit ENUM strings like LOW, MEDIUM, HIGH. |
| **Budget Delivery Method** | `ACCELERATED` delivery method is deprecated in Google Ads API. All new budgets default to standard delivery optimization. |
| **Smart Shopping (Deprecated)** | Smart Shopping campaigns have been deprecated and auto-upgraded to Performance Max (`AdvertisingChannelTypeEnum.PERFORMANCE_MAX`). Standard Shopping remains supported. |
| **Listing Group Atomicity** | `AdGroupCriterionOperation` requests dealing with `listing_group` trees are split into atomic sub-batches by the server. You must send them consecutively within the same API call. |
# Google Ads API v20 Shopping Campaign UI Mapping

This document maps the user interface (UI) input fields required for setting up a Google Ads Shopping Campaign to the corresponding Google Ads API v20 Python SDK fields (`google-ads==28.0.0`), entities, and ENUMs. It strictly follows the order presented in the provided Google Doc.

## 1. Merchant Center account
- **UI Field**: Merchant Center account selection.
- **API Mapping**: `Campaign.shopping_setting.merchant_id`
- **Entity**: `client.get_type("CampaignOperation").create.shopping_setting`
- **Data Type**: `int64`
- **Hierarchy**: Campaign-level setting.

## 2. Choose Shopping/Performance Max
- **UI Field**: Select between Shopping and Performance Max.
- **API Mapping**:
  - For standard Shopping: `Campaign.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.SHOPPING`
  - For Performance Max: `Campaign.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.PERFORMANCE_MAX`
- **Hierarchy**: Campaign-level setting.

## 3. Campaign Name
- **UI Field**: Campaign Name.
- **API Mapping**: `Campaign.name`
- **Entity**: `client.get_type("CampaignOperation").create`
- **Data Type**: `string`
- **Hierarchy**: Campaign-level setting.

## 4. Budget and Bidding Optimization

### Budget
- **UI Field**: Budget amount and delivery method (Standard).
- **API Mapping**:
  - Create a `CampaignBudget` entity: `client.get_type("CampaignBudgetOperation").create`
  - Amount: `CampaignBudget.amount_micros` (in micros, 1,000,000 micros = $1)
  - Delivery Method: `CampaignBudget.delivery_method` (`client.enums.BudgetDeliveryMethodEnum.STANDARD`)
- **Hierarchy**: Campaign Budget is a separate entity linked to the Campaign via `Campaign.campaign_budget`.

### Bidding
- **UI Field**: Bidding strategy (e.g., Target ROAS, Maximize Clicks, Manual CPC).
- **API Mapping**:
  - `Campaign.bidding_strategy_type` ENUMs mapping:
    - Target ROAS: `client.enums.BiddingStrategyTypeEnum.TARGET_ROAS` (configure via `Campaign.target_roas`)
    - Maximize Clicks: `client.enums.BiddingStrategyTypeEnum.TARGET_SPEND` (configure via `Campaign.target_spend`)
    - Manual CPC: `client.enums.BiddingStrategyTypeEnum.MANUAL_CPC` (configure via `Campaign.manual_cpc`)
- **Hierarchy**: Campaign-level setting (Standard Bidding) or shared Bidding Strategy entity.

### Customer Acquisition
- **UI Field**: Customer acquisition settings (e.g., bid higher for new customers).
- **API Mapping**: Customer Acquisition is managed at the campaign level via a specific objective mapping or shared set. *Note*: In API v20, there is a `CustomerAcquisitionGoalSettings` entity (`optimization_mode`, `value_settings`), but it usually requires linking via a Customer Acquisition goal or conversion tracking setup rather than a simple campaign flag for standard Shopping campaigns.

### Campaign Priority
- **UI Field**: Campaign priority (Low, Medium, High).
- **API Mapping**: `Campaign.shopping_setting.campaign_priority`
- **Data Type**: `int32` (0 = Low, 1 = Medium, 2 = High)
- **Hierarchy**: Campaign-level setting.

## 5. Campaign Settings

### Locations
- **UI Field**: Location targeting.
- **API Mapping**:
  - Create a `CampaignCriterion` entity: `client.get_type("CampaignCriterionOperation").create`
  - Set `CampaignCriterion.location.geo_target_constant`
- **Hierarchy**: Campaign Criterion (separate entity linked to Campaign).

### Local Products
- **UI Field**: Enable local inventory ads.
- **API Mapping**: `Campaign.shopping_setting.enable_local`
- **Data Type**: `bool`
- **Hierarchy**: Campaign-level setting.

### EU Political Ads
- **UI Field**: EU political ads declaration.
- **API Mapping**: `Campaign.contains_eu_political_advertising` (Note: Often automatically determined or requires specific account-level compliance settings, field availability depends on policy exceptions).
- **Data Type**: `bool`
- **Hierarchy**: Campaign-level setting.

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
  - Custom Parameters: `Campaign.url_custom_parameters`
- **Hierarchy**: Campaign-level setting.

### Networks
- **UI Field**: Search Network, Search Partners, etc.
- **API Mapping**: `Campaign.network_settings`
  - `network_settings.target_google_search` (`bool`)
  - `network_settings.target_search_network` (`bool`)
  - `network_settings.target_content_network` (`bool`)
  - `network_settings.target_partner_search_network` (`bool`)
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

### Product Groups
- **UI Field**: Product group subdivision (e.g., "All products").
- **API Mapping**:
  - Create an `AdGroupCriterion` entity: `client.get_type("AdGroupCriterionOperation").create`
  - Configure `AdGroupCriterion.listing_group`
  - Entity `ListingGroupInfo` (`type_` = SUBDIVISION or UNIT, `case_value`, `parent_ad_group_criterion`)
  - Set specific bids using `AdGroupCriterion.cpc_bid_micros` on the UNIT listing groups.
- **Hierarchy**: Ad Group Criterion (separate entity linked to Ad Group).

---

## Anomaly Data & API Nuances

| Feature / Setting | API Limitations & Notes |
| :--- | :--- |
| **Customer Acquisition** | Setting up "Bid higher for new customers" in standard shopping requires complex conversion goal tracking. API handles this mostly in Performance Max or via `CustomerAcquisitionGoalSettings`. Not a simple boolean toggle on standard Shopping Campaigns. |
| **EU Political Ads** | The field `contains_eu_political_advertising` exists but modifying it might be restricted depending on your account's verification status for political advertising. Often a read-only or policy-driven field in standard execution. |
| **Campaign Priority** | Stored as integer (0, 1, 2) rather than explicit ENUM strings like LOW, MEDIUM, HIGH. |
| **Budget Delivery Method** | `ACCELERATED` delivery method is deprecated in Google Ads API. All new budgets default to standard delivery optimization. |
| **Smart Shopping (Deprecated)** | Smart Shopping campaigns have been deprecated and auto-upgraded to Performance Max (`AdvertisingChannelTypeEnum.PERFORMANCE_MAX`). Standard Shopping remains supported. |

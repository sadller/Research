import os
import uuid

# Research Google Ads API Python v20 capabilities for Video Campaigns
def research_api():
    markdown = """# Google Ads API (Python v20) - Video Campaigns

## Limitation Notice
As of Google Ads API v20, **it is not possible to create Video Campaigns directly via API mutate operations**.
The `CampaignService.MutateCampaigns` operation does not support creating campaigns with `advertising_channel_type` set to `VIDEO`.

Reference:
- [Google Ads API - Campaigns](https://developers.google.com/google-ads/api/docs/campaigns/overview)
- [Video Campaigns Reference](https://developers.google.com/google-ads/api/reference/rpc/v20/Campaign)

However, you **can** manage existing Video Campaigns, and create/manage Video Ad Groups and Video Ads.

## API Fields for Supported Video Entities

### 1. Video Ad Groups
You can create a Video Ad Group within an existing Video Campaign.
Reference: [AdGroup Reference](https://developers.google.com/google-ads/api/reference/rpc/v20/AdGroup)

**Required Fields:**
- `campaign`: The resource name of the parent Video Campaign.
- `name`: The name of the ad group.
- `type_`: Must be a valid `AdGroupType` for video.
- `status`: `AdGroupStatus` (e.g., `ENABLED`, `PAUSED`).

**Enums (AdGroupType):**
- `VIDEO_BUMPER`: Bumper ad group.
- `VIDEO_EFFICIENT_REACH`: Efficient reach ad group.
- `VIDEO_NON_SKIPPABLE_IN_STREAM`: Non-skippable in-stream ad group.
- `VIDEO_RESPONSIVE`: Responsive video ad group.
- `VIDEO_TRUE_VIEW_IN_DISPLAY`: TrueView in-display ad group.
- `VIDEO_TRUE_VIEW_IN_STREAM`: TrueView in-stream ad group.

### 2. Video Ads
You can create Video Ads within a Video Ad Group using the `AdGroupAdService`.
Reference: [AdGroupAd Reference](https://developers.google.com/google-ads/api/reference/rpc/v20/AdGroupAd)

**Required Fields:**
- `ad_group`: The resource name of the parent Video Ad Group.
- `status`: `AdGroupAdStatus`.
- `ad`: An `Ad` object containing the specific video ad type details.

**Common Video Ad Types:**
- `video_responsive_ad`: A Responsive Video Ad.
- `video_bumper_ad`: A Bumper Ad.
- `video_non_skippable_in_stream_ad`: A Non-skippable In-Stream Ad.

**Fields for `video_responsive_ad`:**
- `headlines`: List of `AdTextAsset` objects.
- `long_headlines`: List of `AdTextAsset` objects.
- `descriptions`: List of `AdTextAsset` objects.
- `call_to_actions`: List of `AdTextAsset` objects.
- `videos`: List of `AdVideoAsset` objects (must be previously uploaded YouTube videos).
- `companions`: List of `AdImageAsset` objects (optional companion banners).

## Python Code Sample: Creating a Video Ad Group and Responsive Video Ad

```python
import uuid
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

def create_video_ad_group_and_ad(client, customer_id, campaign_id, video_asset_id):
    # 1. Create Video Ad Group
    ad_group_service = client.get_service("AdGroupService")
    ad_group_operation = client.get_type("AdGroupOperation")
    ad_group = ad_group_operation.create

    ad_group.name = f"My Responsive Video Ad Group #{uuid.uuid4()}"
    ad_group.status = client.enums.AdGroupStatusEnum.ENABLED
    ad_group.type_ = client.enums.AdGroupTypeEnum.VIDEO_RESPONSIVE
    ad_group.campaign = client.get_service("CampaignService").campaign_path(
        customer_id, campaign_id
    )

    # Ad group bids (e.g., Target CPV)
    ad_group.target_cpv.target_cpv_micros = 10000  # $0.01

    try:
        ad_group_response = ad_group_service.mutate_ad_groups(
            customer_id=customer_id, operations=[ad_group_operation]
        )
        ad_group_resource_name = ad_group_response.results[0].resource_name
        print(f"Created Video Ad Group: {ad_group_resource_name}")
    except GoogleAdsException as ex:
        print(f"Error creating Ad Group: {ex}")
        return

    # 2. Create Responsive Video Ad
    ad_group_ad_service = client.get_service("AdGroupAdService")
    ad_group_ad_operation = client.get_type("AdGroupAdOperation")
    ad_group_ad = ad_group_ad_operation.create

    ad_group_ad.ad_group = ad_group_resource_name
    ad_group_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED

    # Set up the ad structure
    ad = ad_group_ad.ad
    ad.final_urls.append("http://www.example.com")

    # Configure the Responsive Video Ad
    video_ad = ad.video_responsive_ad

    # Add video asset
    ad_video_asset = client.get_type("AdVideoAsset")
    ad_video_asset.asset = client.get_service("AssetService").asset_path(
        customer_id, video_asset_id
    )
    video_ad.videos.append(ad_video_asset)

    # Add text assets
    headline = client.get_type("AdTextAsset")
    headline.text = "My Video Headline"
    video_ad.headlines.append(headline)

    long_headline = client.get_type("AdTextAsset")
    long_headline.text = "My Long Video Headline for Responsive Ad"
    video_ad.long_headlines.append(long_headline)

    description = client.get_type("AdTextAsset")
    description.text = "Check out this awesome video"
    video_ad.descriptions.append(description)

    cta = client.get_type("AdTextAsset")
    cta.text = "Learn More"
    video_ad.call_to_actions.append(cta)

    try:
        ad_group_ad_response = ad_group_ad_service.mutate_ad_group_ads(
            customer_id=customer_id, operations=[ad_group_ad_operation]
        )
        print(f"Created Video Ad: {ad_group_ad_response.results[0].resource_name}")
    except GoogleAdsException as ex:
        print(f"Error creating Video Ad: {ex}")

```
"""
    output_dir = "GoogleAds/video-campaigns/v20/Google_Ads_API_Mutate"
    os.makedirs(output_dir, exist_ok=True)
    with open(f"{output_dir}/api_limitations_and_samples.md", "w") as f:
        f.write(markdown)

if __name__ == "__main__":
    research_api()

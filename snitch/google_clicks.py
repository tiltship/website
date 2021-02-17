import logging
from datetime import datetime

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.v6.types import (ConversionAction,
                                            MutateConversionActionsResponse,
                                            UploadClickConversionsResponse)

# from google.ads.google_ads.errors import GoogleAdsException


class MissingResourceError(BaseException):
    pass


def create_conversion_action(
    client: GoogleAdsClient, customer_id: str, name: str
) -> MutateConversionActionsResponse:

    conversion_action_service = client.get_service(
        "ConversionActionService", version="v6"
    )
    conversion_action_operation = client.get_type(
        "ConversionActionOperation", version="v6"
    )

    action = conversion_action_operation.create
    action.name = name
    action.type = client.get_type("ConversionActionTypeEnum").UPLOAD_CLICKS
    action.category = client.get_type("ConversionActionCategoryEnum").DEFAULT
    action.status = client.get_type("ConversionActionStatusEnum").ENABLED

    res = conversion_action_service.mutate_conversion_actions(
        customer_id, [conversion_action_operation]
    )

    return res


def get_conversion_action(
    client: GoogleAdsClient, customer_id: str, name: str
) -> ConversionAction:
    ga_service = client.get_service("GoogleAdsService", version="v6")

    query = f"""
      SELECT conversion_action.id, conversion_action.name
      FROM conversion_action
      WHERE conversion_action.name = '{name}'
    """

    response = ga_service.search_stream(customer_id, query=query)
    try:
        row = next(row for batch in response for row in batch.results)
        return row.conversion_action
    except StopIteration:
        return None


def _create_click_conversion(
    client: GoogleAdsClient,
    customer_id: str,
    action_name: str,
    gclid: str,
    utc_dt: datetime,
) -> UploadClickConversionsResponse:
    ca = get_conversion_action(client, customer_id, action_name)
    if ca is None:
        raise MissingResourceError(
            f"Could not find conversion_action with name {action_name}"
        )
    cc = client.get_type("ClickConversion", version="v6")
    cc.conversion_action = ca.resource_name
    cc.gclid = gclid
    cc.conversion_date_time = utc_dt.strftime("%Y-%m-%d %H:%M:%S+00:00")

    conversion_upload_service = client.get_service(
        "ConversionUploadService", version="v6"
    )

    res = conversion_upload_service.upload_click_conversions(
        customer_id, [cc], partial_failure=True
    )
    return res


def create_click_conversion(
    client: GoogleAdsClient,
    customer_id: str,
    action_name: str,
    gclid: str,
    utc_dt: datetime,
) -> UploadClickConversionsResponse:

    try:
        return _create_click_conversion(client, customer_id, action_name, gclid, utc_dt)
    except MissingResourceError:
        res = create_conversion_action(client, customer_id, action_name)
        print(f"Created non-existent conversion action {action_name}. Response: {res}")
        return _create_click_conversion(client, customer_id, action_name, gclid, utc_dt)

from googleads.errors import GoogleAdsServerFault
from googleads.adwords import AdWordsClient

ADWORDS_VERSION = 'v201809'

class GoogleAdsAccountLostAccessException(Exception):
    """ Raised when we cannot access to an account """
    pass


def check_access_account(aw_account_id: str, adwords_client: AdWordsClient):
    """From an account id check if Arcane has access to it"""
    service = adwords_client.GetService('ManagedCustomerService', version=ADWORDS_VERSION)
    adwords_client.SetClientCustomerId(aw_account_id)

    selector = {
        'fields': ['CustomerId']
    }
    try:
        mcc_account = service.get(selector)
        print(mcc_account)

    except GoogleAdsServerFault as err:
        if "USER_PERMISSION_DENIED" in str(err):
            raise GoogleAdsAccountLostAccessException(f"We cannot access your Google Ads account with the id: {aw_account_id}. Are you sure you granted access?")
        elif "CUSTOMER_NOT_FOUND" in str(err):
            raise GoogleAdsAccountLostAccessException(f"We cannot find this account ({aw_account_id}). Are you sure you entered the correct id?")
        else:
            raise GoogleAdsAccountLostAccessException(
                f"We cannot access this account ({aw_account_id}). Are you sure you entered the correct id?")

    if mcc_account and mcc_account['totalNumEntries'] > 1:
        raise GoogleAdsAccountLostAccessException('This account ID is a MCC. Please enter a Google Ads Account.')

    return True

from apps.accounts.models import Account


def test_account_model_props_exist():
    assert hasattr(Account, 'is_subscription_active')
    assert hasattr(Account, 'full_address')

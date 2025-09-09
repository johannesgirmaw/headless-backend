from apps.accounts.serializers import AccountSerializer


def test_account_serializer_computed_and_core_fields():
    s = AccountSerializer()
    fields = s.get_fields()
    for key in ['full_address', 'is_subscription_active', 'account_id', 'company_name']:
        assert key in fields

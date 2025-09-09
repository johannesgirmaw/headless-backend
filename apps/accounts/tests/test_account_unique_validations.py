from apps.accounts.serializers import AccountSerializer


def test_account_serializer_validation_methods_exist():
    s = AccountSerializer()
    assert hasattr(s, 'validate_account_id')
    assert hasattr(s, 'validate_company_email')

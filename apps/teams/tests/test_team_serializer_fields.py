from apps.teams.serializers import TeamSerializer


def test_team_serializer_has_member_count():
    s = TeamSerializer()
    assert 'member_count' in s.get_fields()

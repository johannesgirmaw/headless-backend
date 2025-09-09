from apps.teams.serializers import TeamMemberSerializer


def test_team_member_serializer_has_user_details():
    s = TeamMemberSerializer()
    assert 'user_details' in s.get_fields()

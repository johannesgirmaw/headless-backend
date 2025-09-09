from apps.teams.models import Team


def test_team_helpers_exist():
    assert hasattr(Team, 'get_member_count')
    assert hasattr(Team, 'can_add_member')
    assert hasattr(Team, 'get_members')

# tests/test_discordstatus.py

from discordstatus import DiscordStatus
from pytest import fixture


@fixture
def page_keys():
    #  only valid keys for type "page"
    return [
        'id',
        'name',
        'url',
        'time_zone',
        'updated_at'
    ]


@fixture
def components_keys():
    #  only valid keys for type "components"
    return [
        'id',
        'name',
        'status',
        'created_at',
        'updated_at',
        'position',
        'description',
        'showcase',
        'start_date',
        'group_id',
        'page_id',
        'group',
        'only_show_if_degraded'
    ]


@fixture
def incidents_keys():
    #  only valid keys for type "incidents"
    return [
        'id',
        'name',
        'status',
        'created_at',
        'updated_at',
        'monitoring_at',
        'resolved_at',
        'impact',
        'shortlink',
        'started_at',
        'page_id',
        'incident_updates',
        'components'
    ]


@fixture
def scheduled_maintenances_keys():
    #  only valid keys for type "scheduled_maintenances_keys"
    return [
        'id',
        'name',
        'status',
        'created_at',
        'updated_at',
        'monitoring_at',
        'resolved_at',
        'impact',
        'shortlink',
        'started_at',
        'page_id',
        'incident_updates',
        'components',
        'scheduled_for',
        'scheduled_until'
    ]


@fixture
def status_keys():
    #  only valid keys for type "status"
    return [
        'indicator',
        'description'
    ]


def test_discord_summary():
    """Tests an API call to get discord's summary"""

    status_instance = DiscordStatus()
    response = status_instance.summary

    assert isinstance(response, dict)

    assert isinstance(response['page'], dict)
    assert set(page_keys()).issubset(response['page'].keys()), "All keys should be in 'page'"

    assert isinstance(response['status'], dict)
    assert set(status_keys()).issubset(response['status'].keys()), "All keys should be in 'status'"

    assert isinstance(response['components'], list)
    for datum in response['components']:
        assert set(components_keys()).issubset(datum.keys()), "All keys should be in 'components'"

    assert isinstance(response['incidents'], list)
    for datum in response['incidents']:
        assert set(incidents_keys()).issubset(datum.keys()), "All keys should be in 'incidents'"

    assert isinstance(response['scheduled_maintenances'], list)
    for datum in response['scheduled_maintenances']:
        assert set(scheduled_maintenances_keys()).issubset(datum.keys()), "All keys should be in 'scheduled_maintenances'"


def test_discord_status():
    """Tests an API call to get discord's status"""

    status_instance = DiscordStatus()
    response = status_instance.status

    assert isinstance(response, dict)

    assert isinstance(response['page'], dict)
    assert set(page_keys()).issubset(response['page'].keys()), "All keys should be in 'page'"

    assert isinstance(response['status'], dict)
    assert set(status_keys()).issubset(response['status'].keys()), "All keys should be in 'status'"


def test_discord_components():
    """Tests an API call to get discord's components"""

    status_instance = DiscordStatus()
    response = status_instance.components

    assert isinstance(response, dict)

    assert isinstance(response['page'], dict)
    assert set(page_keys()).issubset(response['page'].keys()), "All keys should be in 'page'"

    assert isinstance(response['components'], list)
    for datum in response['components']:
        assert set(components_keys()).issubset(datum.keys()), "All keys should be in 'components'"


def test_discord_unresolved_incidents():
    """Tests an API call to get discord's unresolved_incidents"""

    status_instance = DiscordStatus()
    response = status_instance.unresolved_incidents

    assert isinstance(response, dict)

    assert isinstance(response['page'], dict)
    assert set(page_keys()).issubset(response['page'].keys()), "All keys should be in 'page'"

    assert isinstance(response['incidents'], list)
    for datum in response['incidents']:
        assert set(incidents_keys()).issubset(datum.keys()), "All keys should be in 'incidents'"


def test_discord_all_incidents():
    """Tests an API call to get discord's all_incidents"""

    status_instance = DiscordStatus()
    response = status_instance.all_incidents

    assert isinstance(response, dict)

    assert isinstance(response['page'], dict)
    assert set(page_keys()).issubset(response['page'].keys()), "All keys should be in 'page'"

    assert isinstance(response['incidents'], list)
    for datum in response['incidents']:
        assert set(incidents_keys()).issubset(datum.keys()), "All keys should be in 'incidents'"


def test_discord_upcoming_maintenances():
    """Tests an API call to get discord's upcoming_maintenance"""

    status_instance = DiscordStatus()
    response = status_instance.upcoming_maintenances

    assert isinstance(response, dict)

    assert isinstance(response['page'], dict)
    assert set(page_keys()).issubset(response['page'].keys()), "All keys should be in 'page'"

    assert isinstance(response['scheduled_maintenances'], list)
    for datum in response['scheduled_maintenances']:
        assert set(scheduled_maintenances_keys()).issubset(datum.keys()), "All keys should be in 'scheduled_maintenances'"


def test_discord_active_maintenances():
    """Tests an API call to get discord's active_maintenance"""

    status_instance = DiscordStatus()
    response = status_instance.active_maintenances

    assert isinstance(response, dict)

    assert isinstance(response['page'], dict)
    assert set(page_keys()).issubset(response['page'].keys()), "All keys should be in 'page'"

    assert isinstance(response['scheduled_maintenances'], list)
    for datum in response['scheduled_maintenances']:
        assert set(scheduled_maintenances_keys()).issubset(datum.keys()), "All keys should be in 'scheduled_maintenances'"


def test_discord_all_maintenances():
    """Tests an API call to get discord's all_maintenance"""

    status_instance = DiscordStatus()
    response = status_instance.all_maintenances

    assert isinstance(response, dict)

    assert isinstance(response['page'], dict)
    assert set(page_keys()).issubset(response['page'].keys()), "All keys should be in 'page'"

    assert isinstance(response['scheduled_maintenances'], list)
    for datum in response['scheduled_maintenances']:
        assert set(scheduled_maintenances_keys()).issubset(datum.keys()), "All keys should be in 'scheduled_maintenances'"

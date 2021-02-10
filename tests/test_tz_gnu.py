import pytest


@pytest.mark.parametrize(
    "timezone,tz_gnu",
    (
        ("Europe/Prague", "CET-1CEST,M3.5.0,M10.5.0/3"),
        ("Europe/London", "GMT0BST,M3.5.0/1,M10.5.0"),
        ("Europe/Moscow", "MSK-3"),
        ("Asia/Hong_Kong", "HKT-8"),
    ),
    ids=(
        "Europe/Prague",
        "Europe/London",
        "Europe/Moscow",
        "Asia/Hong_Kong",
    ),
)
def test_tz_gnu(timezone, tz_gnu):
    import turris_timezone

    assert turris_timezone.TZ_GNU.get(timezone) == tz_gnu

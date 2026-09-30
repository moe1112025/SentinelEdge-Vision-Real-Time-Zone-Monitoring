from config import Zone


def test_zone_boundaries():
    zone = Zone(10, 10, 100, 100)
    assert zone.contains(10, 10)
    assert zone.contains(50, 50)
    assert not zone.contains(101, 50)

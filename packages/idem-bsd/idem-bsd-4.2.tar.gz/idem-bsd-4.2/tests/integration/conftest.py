import pytest


@pytest.fixture(scope="session")
def hub(hub):
    hub.pop.sub.add(dyne_name="grains")

    hub.grains.init.standalone()

    yield hub

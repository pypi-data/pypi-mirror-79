#  Copyright 2018 Ocean Protocol Foundation
#  SPDX-License-Identifier: Apache-2.0
import os

import pytest

from aquarius.app.util import get_contract_address_and_abi_file
from aquarius.events.events_monitor import EventsMonitor
from aquarius.constants import BaseURLs
from aquarius.run import app

app = app

EVENTS_INSTANCE = None


@pytest.fixture
def base_ddo_url():
    return BaseURLs.BASE_AQUARIUS_URL + '/assets/ddo'


@pytest.fixture
def client_with_no_data():
    client = app.test_client()
    client.delete(BaseURLs.BASE_AQUARIUS_URL + '/assets/ddo')
    yield client


@pytest.fixture
def client():
    client = app.test_client()

    yield client


@pytest.fixture
def events_object():
    global EVENTS_INSTANCE
    if not EVENTS_INSTANCE:
        contract_address, abi_file = get_contract_address_and_abi_file()
        EVENTS_INSTANCE = EventsMonitor(
            os.environ.get('EVENTS_RPC', False),
            contract_address,
            abi_file,
            app.config['CONFIG_FILE']
        )
    return EVENTS_INSTANCE

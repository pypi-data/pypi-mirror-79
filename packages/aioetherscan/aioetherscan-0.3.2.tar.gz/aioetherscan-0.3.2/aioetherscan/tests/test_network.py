import asyncio
import json
import logging
from unittest.mock import patch

import aiohttp
import asynctest
import pytest
from asyncio_throttle import Throttler
from asynctest import CoroutineMock, MagicMock
from asynctest import patch

from aioetherscan.exceptions import EtherscanClientContentTypeError, EtherscanClientError, EtherscanClientApiError, \
    EtherscanClientProxyError
from aioetherscan.network import Network, HttpMethod


class SessionMock(CoroutineMock):
    @pytest.mark.asyncio
    async def get(self, url, params, data):
        return AsyncCtxMgrMock()


class AsyncCtxMgrMock(MagicMock):
    @pytest.mark.asyncio
    async def __aenter__(self):
        return self.aenter

    @pytest.mark.asyncio
    async def __aexit__(self, *args):
        pass


def get_loop():
    return asyncio.get_event_loop()


def apikey():
    return 'testapikey'


@pytest.fixture()
async def nw():
    nw = Network(apikey(), 'main', get_loop())
    yield nw
    await nw.close()


def test_init():
    myloop = get_loop()
    n = Network(apikey(), 'main', myloop)

    assert n._API_KEY == apikey()
    assert n._loop == myloop

    assert isinstance(n._session, aiohttp.ClientSession)
    assert n._session.loop == myloop

    assert isinstance(n._throttler, Throttler)
    assert n._throttler.rate_limit == 5

    assert isinstance(n._logger, logging.Logger)


def test_sign(nw):
    assert nw._sign({}) == {'apikey': nw._API_KEY}
    assert nw._sign({'smth': 'smth'}) == {'smth': 'smth', 'apikey': nw._API_KEY}


def test_filter_params(nw):
    assert nw._filter_params({}) == {}
    assert nw._filter_params({1: 2, 3: None}) == {1: 2}
    assert nw._filter_params({1: 2, 3: 0}) == {1: 2, 3: 0}
    assert nw._filter_params({1: 2, 3: False}) == {1: 2, 3: False}


@pytest.mark.asyncio
async def test_get(nw):
    with patch('aioetherscan.network.Network._request', new=CoroutineMock()) as mock:
        await nw.get()
        mock.assert_called_once_with(HttpMethod.GET, params={'apikey': nw._API_KEY})


@pytest.mark.asyncio
async def test_post(nw):
    with patch('aioetherscan.network.Network._request', new=CoroutineMock()) as mock:
        await nw.post()
        mock.assert_called_once_with(HttpMethod.POST, data={'apikey': nw._API_KEY})

    with patch('aioetherscan.network.Network._request', new=CoroutineMock()) as mock:
        await nw.post({'some': 'data'})
        mock.assert_called_once_with(HttpMethod.POST, data={'apikey': nw._API_KEY, 'some': 'data'})

    with patch('aioetherscan.network.Network._request', new=CoroutineMock()) as mock:
        await nw.post({'some': 'data', 'null': None})
        mock.assert_called_once_with(HttpMethod.POST, data={'apikey': nw._API_KEY, 'some': 'data'})


@pytest.mark.asyncio
async def test_request(nw):
    class MagicMockContext(MagicMock):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            type(self).__aenter__ = CoroutineMock(return_value=MagicMock())
            type(self).__aexit__ = CoroutineMock(return_value=MagicMock())

    with asynctest.mock.patch('aiohttp.ClientSession.get', new_callable=MagicMockContext) as m:
        with patch('aioetherscan.network.Network._handle_response', new=CoroutineMock()) as h:
            await nw._request(HttpMethod.GET)
            m.assert_called_once_with('https://api.etherscan.io/api', data=None, params=None)
            h.assert_called_once()

    with asynctest.mock.patch('aiohttp.ClientSession.post', new_callable=MagicMockContext) as m:
        with patch('aioetherscan.network.Network._handle_response', new=CoroutineMock()) as h:
            await nw._request(HttpMethod.POST)
            m.assert_called_once_with('https://api.etherscan.io/api', data=None, params=None)
            h.assert_called_once()

    with asynctest.mock.patch('aiohttp.ClientSession.post', new_callable=MagicMockContext) as m:
        with patch('aioetherscan.network.Network._handle_response', new=CoroutineMock()) as h:
            with patch('asyncio_throttle.Throttler.acquire', new=CoroutineMock()) as t:
                await nw._request(HttpMethod.POST)
                t.assert_called_once()


# noinspection PyTypeChecker
@pytest.mark.asyncio
async def test_handle_response(nw):
    class MockResponse:
        def __init__(self, data, raise_exc=None):
            self.data = data
            self.raise_exc = raise_exc

        @property
        def status(self):
            return 200

        async def text(self):
            return 'some text'

        async def json(self):
            if self.raise_exc:
                raise self.raise_exc
            return json.loads(self.data)

    with pytest.raises(EtherscanClientContentTypeError) as e:
        await nw._handle_response(MockResponse('qweasd', aiohttp.ContentTypeError('info', 'hist')))
    assert e.value.status == 200
    assert e.value.content == 'some text'

    with pytest.raises(EtherscanClientError, match='some exc'):
        await nw._handle_response(MockResponse('qweasd', Exception('some exc')))

    with pytest.raises(EtherscanClientApiError) as e:
        await nw._handle_response(MockResponse('{"status": "0", "message": "NOTOK", "result": "res"}'))
    assert e.value.message == 'NOTOK'
    assert e.value.result == 'res'

    with pytest.raises(EtherscanClientProxyError) as e:
        await nw._handle_response(MockResponse('{"error": {"code": "100", "message": "msg"}}'))
    assert e.value.code == '100'
    assert e.value.message == 'msg'

    assert await nw._handle_response(MockResponse('{"result": "someresult"}')) == 'someresult'


@pytest.mark.asyncio
async def test_close_session(nw):
    with patch('aiohttp.ClientSession.close', new_callable=CoroutineMock) as m:
        await nw.close()
        m.assert_called_once_with()


def test_test_network():
    nw = Network(apikey(), 'tobalaba', get_loop())
    assert nw._API_URL == 'https://api-tobalaba.etherscan.com/api'


def test_invalid_network():
    with pytest.raises(ValueError):
        Network(apikey(), 'wrong', get_loop())

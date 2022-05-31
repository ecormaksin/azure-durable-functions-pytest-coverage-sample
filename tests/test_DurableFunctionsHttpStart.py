from asyncio import Future
from unittest.mock import AsyncMock

import pytest

import azure.functions as func

from DurableFunctionsHttpStart import main


class TestClass:

    @pytest.mark.asyncio
    async def test_http_trigger_function(self, mocker):

        function_name = 'DurableFunctionsOrchestrator'
        instance_id = 'dummy_instance_id'
        starter = AsyncMock()

        mock_request = func.HttpRequest(
            method='POST',
            body=bytes("{}", 'utf-8'),
            url=f'http://localhost:7071/api/orchestrators/{function_name}',
            route_params={'functionName': function_name},
            params={'name': 'Test'}
            )

        mock_response = func.HttpResponse(
            body=None,
            status_code=200,
            headers={
                "Retry-After": 10
                }
            )

        mocked = mocker.patch('DurableFunctionsHttpStart.df.DurableOrchestrationClient')

        mocked.start_new = AsyncMock()
        mocked().start_new.return_value = Future()
        mocked().start_new.return_value.set_result(instance_id)

        mocked.create_check_status_response = AsyncMock()
        mocked().create_check_status_response.return_value = mock_response

        response = await main(mock_request, starter)

        assert response.headers["Retry-After"] is not None
        assert response.headers["Retry-After"] == 10

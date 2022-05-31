from DurableFunctionsOrchestrator import orchestrator_function


def hello_side_effect(hello: str, location: str):
    return f'Hello {location}!'


class TestClass:

    def test_orchestrator_function(self, mocker):
        mocked = mocker.patch('DurableFunctionsOrchestrator.df.DurableOrchestrationContext')
        mocked.call_activity.side_effect = hello_side_effect

        result = list(orchestrator_function(context=mocked))

        assert len(result) == 3
        assert result[0] == 'Hello Tokyo!'
        assert result[1] == 'Hello Seattle!'
        assert result[2] == 'Hello London!'

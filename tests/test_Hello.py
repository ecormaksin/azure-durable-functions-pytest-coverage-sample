from Hello import main


class TestClass:

    def test_hello_str(self):
        name = 'Test'
        result = main(name)
        assert result == 'Hello Test!'

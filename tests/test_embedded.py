import pytest

from environ import Env, Path
from environ.compat import ImproperlyConfigured


class TestEmbedded:
    def setup_method(self, method):
        Env.ENVIRON = {}
        self.env = Env()
        self.env.read_env(Path(__file__, is_file=True)('test_embedded.txt'))

    def test_substitution(self):
        assert self.env('HELLO') == 'Hello, world!'

    def test_braces(self):
        assert self.env('BRACES') == 'Hello, world!'

    def test_recursion(self):
        with pytest.raises(ImproperlyConfigured) as excinfo:
            self.env('RECURSIVE')
        assert str(excinfo.value) == "Environment variable 'RECURSIVE' recursively references itself (eventually)"

    def test_transitive(self):
        with pytest.raises(ImproperlyConfigured) as excinfo:
            self.env('R4')
        assert str(excinfo.value) == "Environment variable 'R4' recursively references itself (eventually)"

from pathlib import Path

import pytest


@pytest.fixture
def data():
    test_dir = Path(__file__).absolute().parent

    return test_dir / "data"

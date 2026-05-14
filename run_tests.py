import pytest
import sys

if __name__ == "__main__":

    # Run pytest in verbose mode
    exit_code = pytest.main([
        "-v",
        "tests"
    ])

    sys.exit(exit_code)
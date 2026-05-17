import unittest
import os

if __name__ == "__main__":
    # wipe test DB before running selenium suite
    if os.path.exists("selenium_test.db"):
        os.remove("selenium_test.db")

    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="tests", pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
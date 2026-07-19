import unittest

from main import check_and_install_dependencies


class TestMain(unittest.TestCase):

    def test_dependencies_function_exists(self):

        self.assertTrue(
            callable(check_and_install_dependencies)
        )

    def test_dependencies_run(self):

        try:
            check_and_install_dependencies()
            success = True

        except Exception:
            success = False

        self.assertTrue(success)


if __name__ == "__main__":
    unittest.main()
    
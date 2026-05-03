import sys
import os
import unittest

# Resolve the project root (parent of the scripts directory)
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, root_dir)

if __name__ == '__main__':
    loader = unittest.TestLoader()
    # Discover tests starting from the project root, looking into the 'tests' directory
    suite = loader.discover(start_dir=root_dir, pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if not result.wasSuccessful():
        sys.exit(1)

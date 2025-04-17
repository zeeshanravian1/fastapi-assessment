"""Test setup file for pytest.

Description:
- This file contains setup for tests. It creates a test database and session
for tests to use.
- Test database is created using DATABASE_URL with suffix "_test".
- Test database is dropped after tests are run.
- Session is disposed after tests are run.

"""

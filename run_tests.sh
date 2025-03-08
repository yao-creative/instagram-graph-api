#!/bin/bash

# Run tests with coverage
echo "Running tests with coverage..."
python -m pytest app/tests -v --cov=app --cov-report=term-missing

# Exit with the pytest exit code
exit $? 
if [ "$1" == "test" ]; then
    echo "Unit testing..."
    pytest
elif [ "$1" == "coverage" ]; then
    echo "Running test coverage..."
    # Run tests with coverage and open the report
    coverage run --source=. -m pytest && coverage html && open htmlcov/index.html
fi

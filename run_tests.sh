files=`find . -type f -name "*.py"`
black --check $files || exit 1
mypy $files --strict || exit 1

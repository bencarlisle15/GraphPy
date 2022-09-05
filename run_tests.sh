files=`find . -type f -name "*.py" | grep -v build`
black --check $files || exit 1
mypy $files --strict || exit 1

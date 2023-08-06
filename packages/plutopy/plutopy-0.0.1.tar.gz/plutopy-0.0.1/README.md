# Example Package

This is a simple example package. You can use
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.

python setup.py sdist bdist_wheel
python -m twine upload dist/*

pip install --index-url https://test.pypi.org/simple/ --no-deps plutopy
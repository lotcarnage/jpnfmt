rm -rf dist
python setup.py sdist
twine upload --repository pypitest ./dist/*

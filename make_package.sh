rm dist/*
python setup_version.py
python setup.py sdist bdist_wheel
twine upload dist/*

## HSL Builder Repo

Python pip package for creating HSL Elements.

### Installation:

You can install hsl builder using pip.
```sh
pip install --pre hsl_builder
```
OR

You can also add `hsl_builder==0.0.1b0` it to your project _`requirements.txt`_
### Usage:
```python
#import hsl builder
from hsl_builder import Button
from hsl_builder.elements import Actionable, ActionableType, URI

# Create a button
button = Button("Title")

# Create link actionable
actionable = Actionable("actionable text", ActionableType.APP_ACTION, URI.LINK)
actionable.payload = {
    'url': 'https://www.haptik.ai'
}
# Add actionable to button
button.actionables.append(actionable)

# generate hsl for our button object
hsl = button.to_hsl()
```

### Publishing

Make sure you have specified the correct version specified in `setup.py`

Remove existing build files

```sh
rm -rf rm -rf dist/ build/ hsl_builder.egg-info/
```

Build package wheel

```sh
python setup.py sdist bdist_wheel
```

Publishing package

Make sure that correct version is specified in setup.py

you'll need to create an account at pypi beforehand

publish to test.pypi.org to make sure that whl is built correctly and can be installed and used from other machines
```sh
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

publish to pypi 
```sh
python -m twine upload dist/*
```
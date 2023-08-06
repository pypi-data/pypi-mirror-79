
PyPI: https://pypi.org/project/django-migration-scripts

### Installation

```bash
pip install django_migration_scripts
```

### Usage

Add to INSTALLED_APPS in settings.py

```python
INSTALLED_APPS = [
######,

'django_migration_scripts',

#####
]
```

Then run the script from shell

```python
python manage.py addscript <app_name>
```

This adds a script in the app in the <app>/scripts folder. Add your script there

### Running the script

```python
python manage.py runscripts
```
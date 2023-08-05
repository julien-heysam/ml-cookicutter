from setuptools import find_packages, setup

setup(
    name="src",
    version="0.1.0",
    description="{{ cookiecutter.description }}",
    author="{{ cookiecutter.author_name }}",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    license="{% if cookiecutter.open_source_license == 'MIT' %}MIT{% elif cookiecutter.open_source_license == 'BSD-3-Clause' %}BSD-3{% endif %}",
)

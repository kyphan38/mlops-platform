from setuptools import find_packages, setup

setup(
    name="model_serving",
    packages=find_packages(exclude=["model_serving_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)

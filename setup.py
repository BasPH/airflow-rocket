"""Setup.py file."""

import setuptools

setuptools.setup(
    name="airflow_rocket",
    version="0.1",
    description="Demo package accompanying blog post",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["apache-airflow~=1.10.2"],
    python_requires="==3.6.*",
)

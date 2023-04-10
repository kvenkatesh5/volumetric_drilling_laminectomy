import setuptools

setuptools.setup(
    name="pydrilling",
    version="0.0.0",
    author="Hisashi Ishida",
    author_email="hishida3@jhu.edu",
    description="Python module with helper functions for the drilling simulator",
    packages=setuptools.find_packages(),
    install_requires=["numpy", "scipy", "rich", "click"],
    include_package_data=True,
    python_requires=">=3.7",
)
from setuptools import setup, find_packages

setup(
    name="nlp_utils",
    version="0.6.1",
    packages=find_packages(exclude=["tests.*"]),
    include_package_data=True,
    url="",
    license="MIT",
    author="Xiaoquan Kong",
    author_email="u1mail2me@gmail.com",
    description="Utils for NLP",
    install_requires=["nltk", "numpy", "micro_toolkit"],
    extras_require={"tensorflow": ["tensorflow"]},
)

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='asol_probability_dist',
      version='0.2',
      author="Andrew Leung",
      author_email="Andrew.sLeung@gmail.com",
      description='A package to visualize Gaussian and Binomial probability distributions',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=['asol_probability_dist'],
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      zip_safe=False)



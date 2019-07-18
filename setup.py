from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(name='lookml-tools',
      version='2.0.0',
      description='Set of tools for handling LookML files: a linter, updater, and grapher',
      url='https://github.com/ww-tech/lookml-tools',
      author='Carl Anderson',
      author_email='carl.anderson@weightwatchers.com',
      long_description=long_description,
      long_description_content_type='text/markdown',
      license='Apache 2.0',
      packages=['lkmltools'],
      zip_safe=False,
      classifiers=[
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent"
      ],
      project_urls={
        'Documentation': 'https://ww-tech.github.io/lookml-tools/',
        'Source': 'https://github.com/ww-tech/lookml-tools',
    })

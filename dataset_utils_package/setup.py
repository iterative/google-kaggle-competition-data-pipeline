from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='dataset_utils',
    url='https://github.com/iterative/google-kaggle-competition-data-pipeline/dataset_utils_package',
    author='Dan Martinec',
    author_email='dan@iterative.ai',
    # Needed to actually package something
    packages=['dataset_utils'],
    # Needed for dependencies
    #install_requires=['numpy', 'fiftyone'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='MIT',
    description='Python package with utility functions to work with datasets and Voxel51',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)
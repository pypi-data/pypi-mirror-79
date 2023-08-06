from setuptools import setup, find_packages

setup(
    name='image_dataset_creator',
    version='1.0.0',
    description='Small package to help download images from searching Bing API.',
    author='BLANC Swan',
    author_email='swan.blanc.pro@gmail.com',
    url='https://github.com/keyofdeath/dataset_creator',
    keywords=['computer vision', 'Dataset creation', 'opencv', 'Deep learning'],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'creator=dataset_creator.__main__'
        ]
    },
    install_requires=[
        "docopt",
        "opencv-python>=4.4.0.42",
        "python-dotenv",
        "requests",
        "twine"
    ]
)

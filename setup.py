from setuptools import setup

setup(
    name='simple_np',
    version='0.1',
    packages=[],
    py_modules = ['np_extractor',
                 'np_grammar',
                 'rules_matcher'],
    install_requires=[
        'nltk',
    ],
    url='https://github.com/korobool/simple_np',
    license='MIT License',
    author='Oleksandr Korobov',
    author_email='korobov.alex@gmail.com',
    description='Noun phrases extractor that works on a broken syntax better then solutions that expect text to be '
                'consistent. '
)

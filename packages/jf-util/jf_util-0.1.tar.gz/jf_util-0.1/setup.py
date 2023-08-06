from setuptools import setup

setup(
    name='jf_util',
    version='0.1',
    description='Utility package by James Fang',
    url='https://github.com/jthefang/jf_util',
    author='James Fang',
    author_email='jtotheamesfang@gmail.com',
    license='MIT',
    packages=['jf_util'],
    zip_safe=False,
    test_suite='nose.collector',
    tests_require=['nose'],
)
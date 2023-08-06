from setuptools import setup

"""The setup script."""

setup(
    name='pytest-change-report',
    url='https://github.com/yoyoketang/pytest-change-report',
    version='1.0',
    author="yoyo",
    author_email='283340479@qq.com',
    description='turn . into √，turn F into x',
    long_description='print result on terminal turn . into √，turn F into x using hook',
    classifiers=[
        'Framework :: Pytest',
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python :: 3.6',
    ],
    license='proprietary',
    py_modules=['pytest_change_report'],
    keywords=[
        'pytest', 'py.test', 'pytest-change-report',
    ],

    install_requires=[
        'pytest'
    ],
    entry_points={
        'pytest11': [
            'change-report = pytest_change_report',
        ]
    }
)
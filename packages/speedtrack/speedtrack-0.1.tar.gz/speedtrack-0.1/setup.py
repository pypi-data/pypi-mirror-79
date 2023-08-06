from distutils.core import setup

install_reqs = [
    'requests >= 2.16.2',
]

test_reqs = [
    'pytest',
]

setup(
    name='speedtrack',
    packages=['speedtrack'],
    version='0.1',
    license='MIT',
    description='speedtrack python sdk',
    author='drish',
    author_email='carlosderich@gmail.com',
    url='https://github.com/drish/speedtrack',
    install_requires=install_reqs,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
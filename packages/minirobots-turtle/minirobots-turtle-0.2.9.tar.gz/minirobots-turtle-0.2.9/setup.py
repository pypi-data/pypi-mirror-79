import setuptools


with open('README.md', 'r') as fh:
    long_description = fh.read()


setuptools.setup(
    name='minirobots-turtle',
    version='0.2.9',
    author='Leo Vidarte',
    author_email='lvidarte@gmail.com',
    description='Python client for Minirobots Turtle Robot (includes Jupyter tutorial)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://minirobots.com.ar',
    packages=[
        'minirobots',
        'minirobots-tutorial',
    ],
    package_data={
        'minirobots': ['minirobots/**/*'],
        'minirobots-tutorial': [
            'minirobots-tutorial/**/*',
            'minirobots-tutorial/.jupyter/**/*',
        ],
    },
    include_package_data=True,
    scripts=[
        'bin/minirobots-shell',
        'bin/minirobots-tutorial',
        'bin/minirobots-serial-monitor',
    ],
    setup_requires=[
        'flake8',
    ],
    install_requires=[
        'ipython==7.17.0',
        'jupyter==1.0.0',
        'requests==2.24.0',
        'serial',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Education',
    ],
    python_requires='>=3.6',
 )

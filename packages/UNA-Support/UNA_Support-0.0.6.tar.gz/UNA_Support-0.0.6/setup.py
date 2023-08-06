from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.7'
]

setup(
    name='UNA_Support',
    version='0.0.6',
    description='UNA support modules',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Gaidarji Nicolae',
    author_email='nicolaegaidarji@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='UNA',
    packages=find_packages(),
    install_requires=['']
)
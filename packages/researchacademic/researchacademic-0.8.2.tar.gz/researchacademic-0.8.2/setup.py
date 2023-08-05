from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='researchacademic',
    version='0.8.2',
    description=("A python library that aims to retrieve data from Microsoft"
                 "Research Academic and parse data to human readable"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/wyh/pymsresearch',
    author='Samuel Wu',
    author_email='samuel.yh.wu@gmail.com',
    license='MIT',
    packages=['researchacademic'],
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    zip_safe=True
)

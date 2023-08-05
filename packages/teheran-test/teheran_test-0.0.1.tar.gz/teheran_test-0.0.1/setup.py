from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT Licence',
    'Programming Language :: Python :: 3'
]

with open('README.txt') as f:
    long_description = f.read()
setup(
    name='teheran_test',
    version='0.0.1',
    author='César Pérez Moreno',
    author_email= 'cperez@aptude.com',
    licence='MIT',
    url='https://github.com/cesardeaptude/teheran_test',
    long_description = long_description,
    long_description_content_type="text/x-rst",
    description='A test of web scrapping tool for teherannews.com',
    packages=find_packages(),
    python_requires='>=3',
    install_requires=['bs4 ==0.0.1', 'urllib3==1.25.7'],
    include_package_data=True
)
from setuptools import find_packages, setup

long_description = open('README.md').read()
version_identifier = '0.0.8'

setup(
    name='airium',
    version=version_identifier,
    author='Michał Kaczmarczyk',
    author_email='michal.s.kaczmarczyk@gmail.com',
    maintainer='Michał Kaczmarczyk',
    maintainer_email='michal.s.kaczmarczyk@gmail.com',
    license='MIT license',
    url='https://gitlab.com/kamichal/airium',
    description='Easy and quick html builder with natural syntax correspondence (python->html). '
                'No templates needed. Serves pure pythonic library with no dependencies.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    requires=[],
    install_requires=[],
    keywords='natural html generator compiler template-less',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Telecommunications Industry',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'Topic :: Database :: Front-Ends',
        'Topic :: Documentation',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ]
)

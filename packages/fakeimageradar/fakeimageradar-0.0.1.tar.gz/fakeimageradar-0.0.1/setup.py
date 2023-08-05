from setuptools import setup, Extension

setup(
    name='fakeimageradar',
    version='0.0.1',
    description="Fake Image detector",
    author='Heitor Sampaio',
    author_email='heitor.sampaio@parafernalia.net.br',
    license='MIT',
    packages=['fakeimageradar'],
    include_package_data=True,
    package_dir={'fakeimageradar': 'fakeimageradar'},
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    install_requires=['tensorflow', 'livelossplot', 'matplotlib'],
    python_requires='>=3',
)

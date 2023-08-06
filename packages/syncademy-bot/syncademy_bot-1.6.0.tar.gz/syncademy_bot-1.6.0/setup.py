import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="syncademy_bot",
    version="1.6.0",
    author="Turael Dreamwalker",
    description="Syncademy Bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nunobeato/syncademybot",
    packages=setuptools.find_packages(),
    data_files=[('resources', ['syncademy/resources/credentials_example.json',
                               'syncademy/resources/syncademy_bot_example.ini'])],
    include_package_data=True,
    install_requires=['discord',
                      'google-auth-httplib2',
                      'google-auth-oauthlib',
                      'google-api-python-client'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)

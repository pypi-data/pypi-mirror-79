import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="audioft", # Replace with your own username
    version="2.1.5",
    author="nnnnnzo",
    author_email="nnnzodevgoog@gmail.com",
    description="*AFT is an audio translator nano framework* based on python who transcribe and translate an audio file to another language. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nnnzo/AudioFileTranslator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Operating System :: OS Independent",
    ],
    install_requires=['SpeechRecognition==3.8.1', 'googletrans==2.4.0'],
    python_requires='>=3.6',
)

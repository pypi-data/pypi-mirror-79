from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Orange3–MNE",
    description="Electrophysiological data processing widgets for Orange 3 based on the MNE for Python library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    entry_points={
        "orange.widgets": (
            "EEG – 1. Data IO = Orange3MNE.EegDataIO.widgets",
            "EEG – 2. Preprocessing = Orange3MNE.EegPreprocessing.widgets",
            "EEG – 3. Feature extraction = Orange3MNE.EegFeatureExtraction.widgets",
            "EEG – 4. Classification = Orange3MNE.EegClassification.widgets",
            "EEG – 5. Visualization = Orange3MNE.EegVisualization.widgets"
        )
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',

    author="Filip Jani",
    author_email="jsem@filek.cz",
    keywords=("orange3 add-on", "mne", "eeg", "electrophysiology"),
    url="https://gitlab.com/fifal/orange-mne-library",

    install_requires=[
        "mne==0.20.7",
        "PyQt5",
        "keras==2.4.3",
        "keras-metrics==1.1.0",
        "tensorflow==2.2.0"
    ],
    include_package_data=True,
    version='1.0.12'
)
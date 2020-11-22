from setuptools import setup, find_packages


setup(
    name="parser_to_sms",
    version="1.0",
    packages=find_packages(),
    install_requires=['absl-py==0.11.0', 'aiofiles==0.6.0', 'aiohttp==3.7.3', 'astor==0.8.1', 'async-timeout==3.0.1',
                      'attrs==20.3.0', 'cached-property==1.5.2', 'certifi==2020.11.8', 'chardet==3.0.4',
                      'cycler==0.10.0', 'decorator==4.4.2', 'gast==0.2.2', 'google-pasta==0.2.0', 'grpcio==1.33.2',
                      'h5py==3.1.0', 'idna==2.10', 'imageio==2.9.0', 'importlib-metadata==2.0.0',
                      'Keras-Applications==1.0.8', 'Keras-Preprocessing==1.1.2', 'kiwisolver==1.3.1',
                      'Markdown==3.3.3', 'matplotlib==3.3.3', 'multidict==5.0.2', 'networkx==2.5', 'NudeNet==2.0.6',
                      'numpy==1.18.5', 'opencv-python==4.4.0.46', 'opencv-python-headless==4.4.0.46',
                      'opt-einsum==3.3.0', 'paraser-to-sms==1.0', 'Pillow==8.0.1', 'progressbar2==3.53.1',
                      'protobuf==3.14.0', 'pydload==1.0.8', 'pyparsing==2.4.7', 'pytesseract==0.3.6',
                      'python-dateutil==2.8.1', 'python-utils==2.4.0', 'PyWavelets==1.1.1', 'PyYAML==5.3.1',
                      'requests==2.25.0', 'scikit-image==0.17.2', 'scipy==1.5.4', 'six==1.15.0', 'tensorboard==1.15.0',
                      'tensorflow==1.15.4', 'tensorflow-estimator==1.15.1', 'tensorflow-gpu==1.15.4',
                      'termcolor==1.1.0', 'tifffile==2020.11.18', 'typing-extensions==3.7.4.3', 'urllib3==1.26.2',
                      'Werkzeug==1.0.1', 'wrapt==1.12.1', 'yarl==1.6.3', 'zipp==3.4.0', ''])
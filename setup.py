from setuptools import setup

setup(name='webdebug',
      version='1.0.2',
        install_requires=[
           'werkzeug>=0.14'
        ],
      description='Webdebug',
      url='https://github.com/fpim/webdebug',
      author='Louis@FPIM',
      author_email='frompythonimportme@gmail.com',
      license='MIT',
      packages=['webdebug'],
      zip_safe=False,
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      python_requires='>=3.4',
      )
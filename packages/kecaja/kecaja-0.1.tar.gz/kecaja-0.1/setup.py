from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='kecaja',
      version='0.1',
      description='The funniest joke in the world',
      long_description=readme(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
          'Topic :: Text Processing :: Linguistic',
      ],
      keywords='funniest joke comedy flying circus',
      url='https://github.com/davofis/kecaja',
      author='David Vargas',
      author_email='davofis123@gmail.com',
      license='MIT',
      packages=['kecaja'],
      install_requires=[
          'markdown',
      ],
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3'],
      entry_points={
          'console_scripts': ['funniest-joke=funniest.command_line:main'],
      },
      include_package_data=True,
      zip_safe=False)

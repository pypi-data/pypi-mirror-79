from setuptools import setup

setup(name='weblock',
      version='1.0.0',
      description='WebLock is a simple tool for hiding an HTML file behind a password on a static server ',
      url='https://github.com/Ewpratten/weblock',
      author='Evan Pratten',
      author_email='ewpratten@gmail.com',
      license='GPLv3',
      packages=['weblock'],
      zip_safe=False,
      include_package_data=True,
      entry_points = {
        'console_scripts': ['weblock=weblock.__main__'],
    })
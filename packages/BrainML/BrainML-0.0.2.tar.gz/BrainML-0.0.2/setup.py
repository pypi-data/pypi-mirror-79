from setuptools import setup, Extension

with open('README.md') as f:
    long_description = f.read()

setup(
  name = 'BrainML',         # How you named your package folder (MyLib)
  packages = ['BrainML'],   # Chose the same as "name"
  version = '0.0.2',      # Start with a small number and increase it with every change you make
  license='Apache license 2.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  long_description=long_description,
  long_description_content_type='text/markdown',  # This is important!
  description = 'BrainML is a machine learning library capable of implementing neural networks.',   # Give a short description about your library
  author = 'Bibina Bogdan',                   # Type in your name
  author_email = 'bogdanbibina@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/bogdan124/BrainML',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/bogdan124/BrainML/archive/0.0.1.tar.gz',    # I explain this later on
  keywords = ['MachineLearning', 'library', 'neural networks','deep-learning','artificial-intelligence','artificial-neural-networks'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'tensorflow==1.14.0'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Apache Software License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)

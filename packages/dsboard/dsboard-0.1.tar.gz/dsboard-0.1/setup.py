from distutils.core import setup
setup(
  name = 'dsboard',         
  packages = ['dsboard'],   
  version = '0.1',     
  license='MIT',       
  description = 'Python module for dsboard.',   
  author = 'Leon Stjepan Uroic',                   
  author_email = 'leon.stjepan@gmail.com',     
  url = 'https://github.com/leon3428/dsboard-python',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/leon3428/dsboard-python/archive/0.1.tar.gz',    
  keywords = ['DSBOARD', 'LIVE PLOTTING', 'DATA SCIENCE'],   
  install_requires=[],
  classifiers=[
    'Development Status :: 4 - Beta',      
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
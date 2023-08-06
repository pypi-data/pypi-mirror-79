from distutils.core import setup
setup(
  name = 'MCSC',        
  packages = ['MCSC'], 
  version = '0.3',      
  license='MIT',        
  description = 'A package for solving MCSC problems.',   
  author = 'Samip Timalsena',                   
  author_email = 'samip425@gmail.com',      
  url = 'https://github.com/samiptimalsena/MCSC',   
  download_url = 'https://github.com/samiptimalsena/MCSC/archive/v_04.tar.gz',    
  keywords = ['MCSC', 'KATHMANDU UNIVERSITY', 'Algorithms'],  
  install_requires=[           
          'numpy',
          'prettytable',
          'sympy'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',     
    'Intended Audience :: Developers',    
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3.6',
  ],
)
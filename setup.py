from distutils.core import setup
setup(
  name = 'stock_wrapper',
  packages = ['stock_wrapper'],   # Chose the same as "name"
  version = '0.1',
  license='MIT',
  description = 'A wrapper to handle all of your stock data and trading needs',
  author = 'Jaden Shiteng Wang',
  author_email = 'jaden.shiteng.wang@gmail.com',
  url = 'https://github.com/JadenSWang/Stock-Wrapper',
  download_url = 'https://github.com/JadenSWang/Stock-Wrapper/archive/0.1.tar.gz',    # I explain this later on
  keywords = ['stocks', 'yfinance', 'robinhood'],
  install_requires=[            # I get to this in a second
          'yfinance',
          'robin_stocks',
          'matplotlib',
          'seaborn',
          'curses',
          'plotly',
          'pandas',
          'numpy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
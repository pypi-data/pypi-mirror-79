from distutils.core import setup
setup(
  name = 'ESP32',         # How you named your package folder (MyLib)
  packages = ['ESP32'],   # Chose the same as "name"
  version = '1.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = "Module d'utilisation de la carte esp 32 (IOT)  ",   # Give a short description about your library
  author = 'Adel NEHDI',                   # Type in your name
  author_email = 'nehdi@yahoo.fr',      # Type in your E-Mail
  url = 'https://github.com/Profinfo2020/ESP32',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Profinfo2020/ESP32/archive/1.0.tar.gz',    # I explain this later on
  keywords = ['IOT', 'ido', 'esp32' , 'esp' , 'python' , 'machine' , 'programmation' , 'info 3eme' , 'info 2eme' , 'nouvelle technologie'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
        
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
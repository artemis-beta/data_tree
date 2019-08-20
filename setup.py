from setuptools import setup

setup(name                =  'data_tree'                                   ,
      version             =  '0.1.0'                                       ,
      description         =  'DataTree class is a complex form of a dict'  ,
      url                 =  'http://github.com/artemis-beta/data_tree'    ,
      author              =  'Kristian Zarebski'                           ,
      author_email        =  'krizar312@yahoo.co.uk'                       ,
      license             =  'MIT'                                         ,
      packages            =  ['data_tree']                                 ,
      zip_safe            =  False                                         ,
      install_requires    =  ['nose2', 'hypothesis']
     )

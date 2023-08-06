from distutils.core import setup
setup(
  name = 'DefuzzimetricArc',         
  packages = ['DefuzzimetricArc'],   
  version = '1.0',      
  license='MIT',        
  description = 'ackage used in decision making processes for defuzzification using trigonometric arcs.',   
  author = 'Williamson J. H. Brigido',      
  url = 'https://github.com/JohnnyEngineer', 
  py_modules=["DefuzzimetricArc"],
  keywords = ['fuzzy', 'defuzzification arc','DefuzzimetricArc'],   
  install_requires=[
      'numpy>=1.19.1',
      'pandas>=1.1.1',
      'matplotlib>=3.3.1'
  ]
)
create a setup.cfg like::

   [metadata]
   name = a-cool-name-here
   version = 0.0.0a0

   [options]
   py_modules = a_cool_name_here
   install_requires = pthogen

   [options.entry_points]
   pthogen =
       a_cool_name_here = a_cool_name_here:main

   [bdist_wheel]
   universal = 1

and a_cool_name_here.py like::

   def main():
       # your cool interpreter startup hacks go here

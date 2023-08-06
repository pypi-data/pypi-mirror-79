from collections import OrderedDict

class SecurityError(Exception):
    pass

user = input('Enter your ID : ')
passwd = input(f"Enter [{user}]'password : ")

if passwd == 'ailever' : pass
else: raise SecurityError('Your password is incorrect.')
    

from .docs import *





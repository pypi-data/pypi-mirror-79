from __future__ import print_function
from uliweb.core.commands import Command
from uliweb.contrib.orm.commands import SQLCommandMixin
from ...utils._compat import input
from optparse import make_option

class CreateSuperUserCommand(SQLCommandMixin, Command):
    name = 'createsuperuser'
    help = 'Create a super user account.'
    option_list = (
        make_option('-m', dest='md5', action='store_true', default=False,
                    help='Using md5 to digest password first.'),
    )

    def handle(self, options, global_options, *args):
        from uliweb.manage import make_simple_application
        from uliweb import orm
        from getpass import getpass
        
        self.get_application(global_options)

        username = ''
        while not username:
            username = input("Please enter the super user's name: ")
        email = ''
        while not email:
            email = input("Please enter the email of [{}]: ".format(username))
            
        password = ''
        while not password:
            password = getpass("Please enter the password for [{}({})]: ".format(username, email))
        repassword = ''
        while not repassword:
            repassword = getpass("Please enter the password again: ")
        
        if password != repassword:
            print("The password is not matched, can't create super user!")
            return
        
        orm.set_dispatch_send(False)
        
        User = orm.get_model('user', options.engine)
        user = User(username=username, email=email)
        user.set_password(password, options.md5)
        user.is_superuser = True
        user.save()

class EncryptPasswordCommand(Command):
    name = 'encryptpassword'
    help = 'Encrypt password.'

    def handle(self, options, global_options, *args):
        from uliweb import functions
        import getpass

        self.get_application(global_options)

        password = getpass.getpass('Input your password(Blank will quit):')
        if not password:
            return
        password1 = getpass.getpass('Enter your password twice:')
        if password != password1:
            print("Your password is not matched, please run the command again")
        else:
            print(functions.encrypt_password(password))

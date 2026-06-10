from bootstrap import bootstrap
from infra.cli.screens.main_menu import main_menu

  
def main():

    main_menu(bootstrap())

    print('\nBye!\n')

            
if __name__=='__main__':
    main()
from bootstrap import bootstrap
from infra.cli.screens.main_menu import main_menu
from infra.cli.screens.goodbye import goodbye
  
def main():

    main_menu(bootstrap())

    goodbye()

            
if __name__=='__main__':
    main()
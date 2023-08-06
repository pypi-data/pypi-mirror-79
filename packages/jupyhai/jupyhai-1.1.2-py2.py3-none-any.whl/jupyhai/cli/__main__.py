import sys
from notebook import nbextensions


def main():
    if "install" in sys.argv:
        print("Installing Jupyhai notebook extension...")
        nbextensions.install_nbextension_python('jupyhai', symlink=True, user=True)
        nbextensions.enable_nbextension_python('jupyhai')
    else:
        print("Use 'jupyhai install' to install the notebook extension.")


if __name__ == "__main__":
    main()

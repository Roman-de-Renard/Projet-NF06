import ctypes as ct
from pathlib import Path


def open_dll(name='libc_libs.dll'):
    # on remonte sur le dossier du projet
    lib_path = Path().absolute().parent
    # et on redescend l'arborescence dans le dossier du code C
    lib_path = lib_path / 'c_libs' / 'cmake-build-debug' / name
    # puis on ouvre la librairie partagée avec ctypes et on la retourne
    return ct.CDLL(lib_path.as_posix())


if __name__ == '__main__':
    c_lib = open_dll()

    foo = ct.c_int(3)
    bar = ct.c_int(6)
    print(c_lib.add_int(foo, bar))
    print("Wesh alors")
    c_lib.print_hello()

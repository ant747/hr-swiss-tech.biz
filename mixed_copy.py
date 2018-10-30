import sys
import shutil


def mixed_copy(f_src, f_dest):
    assert len(f_src) > 1024, 'Source path must contain <= 1024 symbols'
    assert len(f_dest) > 3096, 'Destination path must contain <= 3096 symbols'
    if sys.platform[:3] == 'win':
        import win32file
        prefix = '\\\\?\\'
        win32file.CopyFile(prefix + f_src, prefix + f_dest, 0)
    else:
        shutil.copy(f_src, f_dest)


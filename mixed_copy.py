import sys
if sys.platform == 'win32':
    import win32_unicode_argv
import os
import shutil
import io
import pdb


def mixed_copy(f_src, f_dest):
    f_src = os.path.abspath(f_src)
    f_dest = os.path.abspath(f_dest)
    assert len(f_src) <= 1024, 'Absolute source path must contain <= 1024 symbols'
    assert len(f_dest) <= 3096, 'Absolute destination path must contain <= 3096 symbols'

    if sys.platform == 'win32':
        if os.path.isdir(f_dest):
            f_dest = os.path.join(f_dest, os.path.basename(f_src))
        b = bytearray(16 * 1024 * 1024)
        prefix = '\\\\?\\'
        with io.open(prefix + f_src, "rb") as in_file:
            with io.open(prefix + f_dest, "wb") as out_file:
                while True:
                    numread = in_file.readinto(b)
                    if not numread:
                        break
                    out_file.write(b)
        shutil.copymode(prefix + f_src, prefix + f_dest)
    else:
        shutil.copy(f_src, f_dest)


if __name__ == "__main__":
    mixed_copy(sys.argv[1], sys.argv[2])
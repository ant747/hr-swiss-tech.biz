import sys
import shutil
import io



def mixed_copy(f_src, f_dest):
    assert len(f_src) <= 1024, 'Source path must contain <= 1024 symbols'
    assert len(f_dest) <= 3096, 'Destination path must contain <= 3096 symbols'
    if sys.platform == 'win32':
        b = bytearray(16 * 1024 * 1024)
        prefix = '\\\\?\\'
        with io.open(prefix + f_src, "rb") as in_file:
            with io.open(prefix + f_dest, "wb") as out_file:
                while True:
                    numread = in_file.readinto(b)
                    if not numread:
                        break
                    out_file.write(b)
        shutil.copymode(f_src, f_dest)
    else:
        shutil.copy(f_src, f_dest)

if __name__ == "__main__":
    mixed_copy(sys.argv[1], sys.argv[2])
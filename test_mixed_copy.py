# This Python file uses the following encoding: utf-8

from mixed_copy import mixed_copy
import string
import os
import shutil
import csv
import sys
import random


F_LEN = 80
MAX_LEN = 3100
FILE_SIZE = 1024
TEST_COUNT = 100
TF = 'test_file.txt'

if sys.platform == 'win32':
    PREFIX = u'\\\\?\\'
else:
    PREFIX = u''

symbols = u'йцу' + string.digits + string.ascii_letters

home_dir = os.path.dirname(os.path.realpath(__file__))
new_folders = []

i = int(MAX_LEN/float(F_LEN)*1.2)     #длина пути должна содержать тесты за предлами дозволенных значений
for s in symbols[:i]:
    new_folders.append(s*F_LEN)

full_tree = os.path.join(home_dir, *new_folders)

if not os.path.exists(PREFIX + full_tree):   # создаем дерево катологов с участием unicode символов - криллицы
    os.makedirs(PREFIX + full_tree)

test_file_base = os.path.join(home_dir, TF)     # создаем тестовый файл
with open(PREFIX + test_file_base, "wb") as file:
    file.write('a'*FILE_SIZE)

test_recs = []      # формируем случайное количество каталогов для создания путей
srcs = [random.randrange(round(len(new_folders)/2.5)) for i in range(TEST_COUNT)]
dsts = [random.randrange(len(new_folders)) for i in range(TEST_COUNT)]

for k, (i,j) in enumerate(zip(srcs, dsts)):
    src = unicode(os.path.join(home_dir, *list(new_folders[:i]+[TF])))
    if i == j:
        continue
    try:
        shutil.copy(PREFIX + test_file_base, PREFIX + src)  #копируем файл в исходный каталог
    except:
        pass
    dst = unicode(os.path.join(home_dir, *list(new_folders[:j]+[TF])))
    res = ''
    msg = ''
    try:
        mixed_copy(src, dst)
        res = 'ok'
    except Exception as e:
        res = 'error'
        msg = str(e)
    finally:
        rec = {'F_LEN': F_LEN, 'MAX_LEN': MAX_LEN, 'FILE_SIZE': FILE_SIZE, 'full_tree_len': len(full_tree),
               'new_folders_len': len(new_folders), 'src': src, 'src_len': len(src),
               'dst': dst, 'dst_len': len(dst), 'result': res, 'message': msg}
        test_recs.append(rec)
        # pprint(rec)
        print('Test %s/%s: src_len=%s, dst_len=%s, res=%s, msg=%s' %(k+1, TEST_COUNT, len(src), len(dst), res, msg))
        # shutil.move(PREFIX + src, PREFIX + test_file_base)


with open('test_recs.csv', 'w') as csvfile:
    fieldnames = test_recs[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for rec in test_recs:
        rec = dict([(k,v.encode('cp1251')) if isinstance(v, unicode) else (k,v) for (k,v) in rec.items()])
        writer.writerow(rec)


import os
import re
import time
import cProfile

from kappa_graph import KappaComplex

def load_and_unpack(kappa_file):
    """
        Load a Kappa snapshot file.
        """
    if not os.path.isfile(kappa_file):
        raise Exception("Cannot find snapshot file %s" % kappa_file)
    else:
        complex = []
        with open(kappa_file, "r") as data:
            event = float(data.readline().split('Event:')[1][:-2].strip())
            data.readline()
            t = data.readline().split('T0')[1][:-2]
            time = float(re.sub(r'"', ' ', t).strip())
            data.readline()
            currentline = data.readline()[:-1]  # this should be the first line of the first complex

            while True:
                (entry,currentline) = next_complex_from_file(data,currentline)
                if not entry:
                    break
                komplex = KappaComplex.from_string(entry)
                complex.append(komplex)
        return complex

def next_complex_from_file(data,currentline):
    entry = currentline
    line = ''
    while True:
        line = data.readline()
        if not line:
            currentline = ''
            break
        elif '%init' in line:
            if 'agents*/' in line:
                currentline = line[:-1]
            else:
                currentline = ''
            break
        entry = entry + line[:-1]  # remove \n
    return (entry,currentline)

def go():
    snap1_obj = load_and_unpack('../../sources/KappaUtilities/TestData/snap_large.ka')
    snap1_size = len(snap1_obj)

    start = time.process_time()
    intersection = []
    for complex1 in snap1_obj:
        for complex2 in snap1_obj:
            if complex2 == complex1:
                intersection.append(complex1)
                break
            end = time.process_time()
    print(f'seconds: {end - start}')
    print(f'size of intersection: {len(intersection)}')

#cProfile.run('go()')
go()

import re
import sys
import multiprocessing
import tempfile

'''
inp = sys.argv[1] # needs to be modified

organisms_to_search = []

dir_name = tempfile.mkdtemp()

extension = inp[inp.find('.'):]  # .fa or .fq
with open(inp, "r") as f: # reading line by line, failsafe for very large programs
    for line in f:
        while (re.search('>', line) != None):
            name = line
            name = name.rstrip()
            organism_name = name[name.find('>')+2:] + extension 
            organism_name = organism_name.replace(" ", "_")
            organisms_to_search.append(organism_name)
            to_write = open(organism_name, 'w')
            to_write.write(line)
            line = next(f)
            while (re.search('>', line) == None and line != None):
                to_write.write(line)
                try:
                    line = next(f)
                except:
                    break
            to_write.close()

for organism in organisms_to_search:
'''

inp = sys.argv[1] # needs to be modified

organisms_to_search = []

dir_name = tempfile.mkdtemp()

extension = inp[inp.find('.'):]  # .fa or .fq
with open(inp, "r") as f: # reading line by line, failsafe for very large programs
    for line in f:
        while (re.search('>', line) != None):
            name = line
            name = name.rstrip()
            organism_name = name[name.find('>')+2:] + extension 
            organism_name = organism_name.replace(" ", "_")
            organisms_to_search.append(organism_name)
            #to_write = open(organism_name, 'w')
            to_write = tempfile.NamedTemporaryFile(prefix=organism_name, dir=dir_name, mode="w")
            print(to_write)
            to_write.write(line)
            line = next(f)
            while (re.search('>', line) == None and line != None):
                to_write.write(line)
                try:
                    line = next(f)
                except:
                    break
            to_write.close()

#for organism in organisms_to_search:

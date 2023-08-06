            while (re.search('>', line) == None and line != None):
                to_write.write(line)
                line = next(f)
            to_write.close()
        i += 1
#!/usr/bin/env python3

class FileHandler():
    def __init__(self, file_name="data.txt"):
        self.file_name = file_name 

        self.read_mode = "r"
        self.write_mode = "w"
        self.read_write_mode = "r+"
        self.append_mode = "a"
        self.read_append_mode = "a+"


    def read_line(self):
        with open(self.file_name, self.read_mode) as f:
            #print(dir(f))
            return f.readline()

    def read_file(self):
        with open(self.file_name, self.read_mode) as f:
            return f.read()

    def read_latest_line(self):
        with open(self.file_name, self.read_mode) as f:
            f.seek(0, 2)
            f.seek(f.tell()-2)
            return f.readline()

    def write_line(self):
        pass

    
    def append_line(self, in_string):
        with open(self.file_name, self.append_mode) as f:
            f.write(in_string)


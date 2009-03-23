#!/usr/bin/python

class Lecture: 
    def __init__(self): 
        self.name = None 
        self.link = None
        self.words = None
	# map<string,int>. wyraz (malymi literami) -> ile razy wystapil w wykladzie
 
class Course: 
    def __init__(self): 
        self.name = None 
        self.link = None
        self.lectures = None
	# vector<Lecture>


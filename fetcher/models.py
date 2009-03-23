#!/usr/bin/python

class Lecture: 
    def __init__(self): 
        self.name = None 
        self.link = None
        self.words = None
	# map<string,int>
 
class Course: 
    def __init__(self): 
        self.name = None 
        self.link = None
        self.lectures = None
	# vector<Lecture>


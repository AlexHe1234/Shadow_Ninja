"""A middle layer bridging modules and data source"""

import os
from typing import Callable

from data.Gen.utils import extract_data


# HACK: this is ugly but temporary (I hope)
class DataFactory:
    def __init__(self):
        self.data_dir = 'data/Gen'
        self.data_student, self.data_course = extract_data(self.data_dir)
    
    def get_student_ids(self):
        ids = []
        for it in self.data_student:
            ids.append(it['id'])
        return ids  
        
    def get_student(self, sid):
        for it in self.data_student:
            if it['id'] == sid:
                return it
        return None
    
    def get_courses(self):
        return self.data_course

"""recommender system based on mixed RS agents"""

import re
from typing import Literal, Dict
from __init__ import foundation_model, data_factory


def extract_integers(input_string):
    integers = re.findall(r'\d+', input_string)
    integers = [int(num) for num in integers]
    return integers


class LLMRS:
    def __init__(self, 
                 stage1_sys_cmd: str,
                 stage1_usr_cmd: str,                 
                 stage2_sys_cmd: str,
                 stage2_usr_cmd: str,
                 ):
        self.sys_1 = stage1_sys_cmd
        self.usr_1 = stage1_usr_cmd
        self.sys_2 = stage1_sys_cmd
        self.usr_2 = stage1_usr_cmd

    def recommend(self, bundle):
        student = bundle['src']
        courses = bundle['cdd']
        aux = bundle['aux']
        
        # first let llm filter according to course name
        student_major = student['major']
        course_id = [n['id'] for n in courses]
        course_name = [n['name'] for n in courses]
        course_major = [n['major'] for n in courses]
        data_str = '\nStudent Major: ' + student_major
        data_str += '\nCourse Id and Course Names and Course Majors:\n'
        for c in range(len(course_name)):
            data_str += f'  {course_id[c]}, {course_name[c]}, {course_major[c]}\n'
        if aux is not None:
            data_str += 'Additional Request: ' + aux
        print(self.usr_1 + data_str)
        response = foundation_model.forward_text(system_msg=self.sys_1, user_msg=self.usr_1 + data_str)
        candidates = extract_integers(response)
        
        # for it in courses:
        #     if candidates[0] == int(it['id']):
        #         cname = it['name']
        #         cmajor = it['major']
        # return cname, cmajor
        if len(candidates) == 0:
            return None
        
        # then let llm filter according to course comment
        name = [c['comment'] for c in courses if c['id'] in candidates]
        major = [c['major'] for c in courses if c['id'] in candidates]
        comments = [c['comment'] for c in courses if c['id'] in candidates]
        data_str2 = '\nStudent Major: ' + student_major
        data_str2 += '\nCourse Id and Course Names and Course Majors and Comments:\n'
        for c in range(len(name)):
            data_str2 += f'  {candidates[c]}, {name[c]}, {major[c]},'
            for l in range(len(comments[0])):
                data_str2 += f' {comments[c][l]}'
            data_str2 += '\n'
        if aux is not None:
            data_str2 += 'Additional Request: ' + aux
        response2 = foundation_model.forward_text(system_msg=self.sys_2, user_msg=self.usr_2 + data_str2)
        ret = extract_integers(response2)
        if len(ret) == 0:
            return None
        else:
            ret = ret[0]
            for it in courses:
                if ret == int(it['id']):
                    cname = it['name']
                    cmajor = it['major']
                    
            return cname, cmajor


# per-student object
class CourseRecommender:
    def __init__(self,
                 mode: Literal['va', 'llm', 'rl'],
                 rs_config: Dict,
                 sid: int,
                 ):
        self.mode = mode
        if self.mode == 'va':
            raise NotImplementedError()
        elif self.mode == 'llm':
            self.model = LLMRS(**rs_config)
        elif self.mode == 'rl':
            raise NotImplementedError()
        else:
            raise NotImplementedError()
        
        # placeholder for student info & course choice
        self.info = {}
        self.sid = sid
    
    def fetch_state(self):
        self.info['src'] = data_factory.get_student(self.sid)
        self.info['cdd'] = data_factory.get_courses()
    
    def recommend(self, aux: str):
        self.fetch_state()  # update info
        self.info['aux'] = aux
        return self.model.recommend(self.info)


if __name__ == '__main__':
    import random
    
    from __init__ import foundation_model, data_factory, rs_config

    # create rs for a random student
    id_list = data_factory.get_student_ids()
    id_test = id_list[random.randint(0, len(id_list) - 1)]
    rs = CourseRecommender(**rs_config, sid=id_test)
    
    # test recommendation
    # rs.recommend(aux=None)
    stu = data_factory.get_student(id_test)
    print(f'For {stu["name"]} majoring in {stu["major"]}')
    name, major = rs.recommend(aux='The course should be light in workload')
    print(f'We recommend {name} of {major}')

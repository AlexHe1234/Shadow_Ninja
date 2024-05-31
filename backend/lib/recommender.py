"""recommender system based on mixed RS agents"""

from typing import Literal, Dict


class LLMRS:
    def __init__(self):
        pass
    
    def recommend(self, bundle):
        pass


# per-student object
class CourseRecommender:
    def __init__(self,
                 mode: Literal['va', 'llm', 'rl'],
                 rs_config: Dict,
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
        
        # initialize student info & course choice
        self.info = None
    
    def fetch_state(self):
        pass
    
    def recommend(self):
        self.fetch_state()  # update info
        self.model.recommend(self.info)

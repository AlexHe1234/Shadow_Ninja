import jieba
# from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict
from sklearn.metrics.pairwise import cosine_similarity


class WordMaster:
    def __init__(
        self,
        segment_for_search: bool = True,  # better performance for searching
        compare_w_transformer: bool = False,  # this is really slow
    ):
        
        self.for_search = segment_for_search
        self.compare_w_transformer = compare_w_transformer
        
        if self.compare_w_transformer:
            self.transformer = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        
    def segment_word(self, word: str) -> List[str]:
        
        if self.for_search:
            keywords = list(jieba.cut_for_search(word))
        else:
            keywords = list(jieba.cut(word))
        
        return keywords
        
    def compare_word(self, word_src: str, word_tar: str):
        embed_src = self.transformer.encode(word_src)
        embed_tar = self.transformer.encode(word_tar)
        
        similarity = np.sum(embed_src * embed_tar) / (np.linalg.norm(embed_src) * np.linalg.norm(embed_tar) + 1e-6)
        
        return similarity


if __name__ == '__main__':
    word = '乐高玩具儿童星球大战'
    
    # kw = segment_word(word, False)
    # print(kw)
    
    wm = WordMaster(True, True)
    
    word_tar = '人类'
    
    ret = wm.compare_word(word, word_tar)
    print(ret)

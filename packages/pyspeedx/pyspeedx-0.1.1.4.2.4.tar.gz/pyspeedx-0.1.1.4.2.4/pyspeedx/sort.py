from random import choices

import logger

class Sort:
    
    def sort_dict_by_value(_dict: dict,reverse = True):
        
        _dict = {k:v for k,v in sorted(_dict.items(),key = lambda item:item[1],reverse = reverse)}
        return _dict
if __name__ == "__main__":
    logger = logger.Logger.getInstance()
    _dict  = {"a":5 ,'h': 33,"b": 3, "c": 2}
    
    sorted_dict = Sort.sort_dict_by_value(_dict, False)
    # _dict['g'] = 15
    # sorted_dict['d'] = 10
    # population = [1,2,3,4,5,6,7]
    #weights = [0.1, 0.05, 0.05, 0.2, 0.4, 0.2,0.9]
    population = [3,7]
    
    weights = [0.1,0.1]

    logger.log("_dict: %s" % _dict)
    logger.log("sorted_dict: %s" % sorted_dict)
    
    million_samples = choices(population, weights, k=10**6)
    from collections import Counter
    
    _count = Counter(million_samples)
    print(type(_count))
    total = sum(_count)
    print(sum(_count))
    logger.log("total: %s" % total)
    normalized = list(map(lambda x: x/total, _count))
    logger.log("count probableity distibution: %s" % _count )
    logger.log("normalizedprobableity distibution: %s" % normalized )

    #logger.log("probailatiy distribution: %s" % choices(population,weights,k=10))


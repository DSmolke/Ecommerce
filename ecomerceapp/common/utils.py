from typing import Any

def get_n_top_elements_of_most_common_list(elements: list[tuple[Any, Any]]) -> int:
    """
    This function purpose is to help with getting multiple values from Counters.
    Best example is when we have list of [1, 2, 3, 3]. We have 2 highest values, so we want to get list containing them
    :param elements: list that is what Counter.most_common() method returns. Example -> [(2,3), (3,3), (1,1)]
    :return: index of last value which is in most common group
    """
    if len(elements) == 0:
        raise IndexError("List is empty therefor index will be invalid")
    n = 1
    for i in range(1, len(elements)):
        if elements[i][1] == elements[i - 1][1]:
            n += 1
        else:
            return n
    return n

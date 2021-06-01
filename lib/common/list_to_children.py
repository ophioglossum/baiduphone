'''
列表按自定义长度拆分成小列表
:param init_list:
:param childern_list_len:
:return:
'''
def list_of_groups(init_list, children_list_len):
    list_of_group = zip(*(iter(init_list),) *children_list_len) # zip(childern_list_len ge list_iterator object)
    end_list = [list(i) for i in list_of_group] # i is a tuple
    count = len(init_list) % children_list_len
    end_list.append(init_list[-count:]) if count !=0 else end_list
    return end_list
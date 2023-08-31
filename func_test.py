def func(lst):
    lst.append('a')

lst = [1,2,3]
lst_tmp = lst
lst_tmp.append('a')
# func(lst)
print(lst)
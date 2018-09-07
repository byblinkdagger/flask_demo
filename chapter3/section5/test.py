
#  .也会被单独切割保存到一个变量中
# a,b, suffix = "abcd.jpg".rpartition('.')
# print(a)
# print(b)
# print(suffix)
#
# def fab(n):
#     a = 1
#     b= 1
#     for i in range(n):
#         yield a
#         a = b
#         b = a + b
#
# # s  = fab(10)
# for s in fab(10):
#     print(str(s))

# target - 9
# data = [1,8,3,3,4,5,1,2,14,2]
# result = {}
#
# for i in range(10):
#    result[9 - data[i]] = data[i]
#
# for i in range(10):
#     if data[i] in result.keys():
#         print(str(data[i]))

# from functools import wraps
# def decorator_name(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         if not can_run:
#             return "Function will not run"
#         print("starting")
#         f(*args, **kwargs)
#         print("ending")
#     return decorated
#
# @decorator_name
# def func():
#     print("Function is running")
#
# can_run = True
# # print(func())
# func()
# # Output: Function is running
#
# can_run = False
# print(func())
# # Output: Function will not run
# token = '123&ojjh'
# mobile = token.split('&')[0]
# print(mobile)

a = 'abc'
b= 'abc'
print(a.__eq__(b))

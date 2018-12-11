def x(*args):
    return args


y = x(None, None, 324, 33)
print(*y)

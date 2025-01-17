def my_enumerate(iterable, start=0):
    return zip(range(start, start + len(iterable)), iterable)
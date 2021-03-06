from cache_decorator import timer, cache_usage, cache


@timer
@cache_usage(True)
def factorial(n):
    if n < 2:
        return 1
    return factorial(n - 1) * n


print(factorial(10))
print(factorial(11))
print(factorial(10))
print(factorial(9))
print('----------------')
print('Cache values:')
for element in cache:
    print(str(element) + ' | ' + str(cache[element]))

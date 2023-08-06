def fun():
    x = yield 1
    print('x:', x)
    y = yield
    if y == 'hi':
        yield 10
    print('y:', y)
    z = yield 3
    print('z:', z)
    yield 4


gen = fun()

print(next(gen))
print(gen.send('stuff'))
print(gen.send('hi'))
print(gen.send('there'))

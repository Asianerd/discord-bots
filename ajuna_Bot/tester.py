import psutil

def ram_bar(p, length):
    final = [' ' for _ in range(length)]
    if p > 1:
        p = 1
    for i in range(int(length * p)):
        final[i] = "#"
    return ''.join(final)

for i in range(10):
    print(f'[{ram_bar(i/10, 10)}]')

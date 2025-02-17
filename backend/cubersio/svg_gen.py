from random import choice

n = 9
gap = 2.5
size = 20

r = 2

starts = [size * i + gap * i for i in range(n)]

for y in starts:
    for x in starts:
        c = choice(["white", "red", "blue", "green", "yellow", "orange"])
        print(
            f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{r}" ry="{r}" fill="var(--color-{c})" />'
        )
    print()

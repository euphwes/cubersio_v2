from random import choice

for y in [0, 20.22, 40.44, 60.66, 80.88, 101.1, 121.32, 141.54, 161.76, 181.98]:
    for x in [0, 20.22, 40.44, 60.66, 80.88, 101.1, 121.32, 141.54, 161.76, 181.98]:
        c = choice(["white", "red", "blue", "green", "yellow", "orange"])
        print(
            f'<rect x="{x}" y="{y}" width="18" height="18" rx="4" ry="4" fill="var(--color-{c})" />'
        )
    print()

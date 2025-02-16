from random import choice

for y in [0, 20, 40, 60, 80, 100, 120, 140, 160, 180]:
    for x in [0, 20, 40, 60, 80, 100, 120, 140, 160, 180]:
        c = choice(["white", "red", "blue", "green", "yellow", "orange"])
        print(
            f'<rect x="{x}" y="{y}" width="17" height="17" rx="4" ry="4" fill="var(--color-{c})" />'
        )
    print()

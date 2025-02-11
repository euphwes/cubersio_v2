from random import choice

for y in [0, 29, 58, 87, 116, 145, 174]:
    for x in [0, 29, 58, 87, 116, 145, 174]:
        c = choice(["white", "red", "blue", "green", "yellow", "orange"])
        print(
            f'<rect x="{x}" y="{y}" width="26" height="26" rx="6" ry="6" fill="var(--color-{c})" />'
        )
    print()

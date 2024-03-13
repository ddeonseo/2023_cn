N, T, P = map(int, input().split())
t_shirts_colors = list(map(int, input().split()))
pants_colors = list(map(int, input().split()))

t_shirts_count = {}
pants_count = {}

for color in t_shirts_colors:
    if color in t_shirts_count:
        t_shirts_count[color] += 1
    else:
        t_shirts_count[color] = 1

for color in pants_colors:
    if color in pants_count:
        pants_count[color] += 1
    else:
        pants_count[color] = 1

max_matching = 0
for color in set(t_shirts_colors):
    if color in pants_count:
        max_matching += min(t_shirts_count[color], pants_count[color])

print(max_matching)
with open('input.txt') as f:
    lines = f.readlines()

total_score = 0

score_by_my_shape = {
    'X': 1,
    'Y': 2,
    'Z': 3
}

score_by_outcome = {
    'win':  6,
    'draw': 3,
    'lose': 0
}

score_by_pairs = {
    'A X': score_by_my_shape['X'] + score_by_outcome['draw'],
    'A Y': score_by_my_shape['Y'] + score_by_outcome['win'],
    'A Z': score_by_my_shape['Z'] + score_by_outcome['lose'],
    'B X': score_by_my_shape['X'] + score_by_outcome['lose'],
    'B Y': score_by_my_shape['Y'] + score_by_outcome['draw'],
    'B Z': score_by_my_shape['Z'] + score_by_outcome['win'],
    'C X': score_by_my_shape['X'] + score_by_outcome['win'],
    'C Y': score_by_my_shape['Y'] + score_by_outcome['lose'],
    'C Z': score_by_my_shape['Z'] + score_by_outcome['draw'],
}

for current_round in lines:
    current_round_score = score_by_pairs[current_round[:3]]
    total_score += current_round_score

print(total_score)

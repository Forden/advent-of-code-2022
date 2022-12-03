with open('input.txt') as f:
    lines = f.readlines()

score_by_outcome = {
    'win':  6,
    'draw': 3,
    'lose': 0
}

score_by_my_shape = {
    'rock':     1,
    'paper':    2,
    'scissors': 3
}

opponent_shapes_to_standart = {
    'A': 'rock',
    'B': 'paper',
    'C': 'scissors'
}


def part_1():
    total_score = 0
    my_shapes_to_standart = {
        'X': 'rock',
        'Y': 'paper',
        'Z': 'scissors'
    }
    score_by_pairs = {
        'A X': score_by_my_shape[my_shapes_to_standart['X']] + score_by_outcome['draw'],
        'A Y': score_by_my_shape[my_shapes_to_standart['Y']] + score_by_outcome['win'],
        'A Z': score_by_my_shape[my_shapes_to_standart['Z']] + score_by_outcome['lose'],
        'B X': score_by_my_shape[my_shapes_to_standart['X']] + score_by_outcome['lose'],
        'B Y': score_by_my_shape[my_shapes_to_standart['Y']] + score_by_outcome['draw'],
        'B Z': score_by_my_shape[my_shapes_to_standart['Z']] + score_by_outcome['win'],
        'C X': score_by_my_shape[my_shapes_to_standart['X']] + score_by_outcome['win'],
        'C Y': score_by_my_shape[my_shapes_to_standart['Y']] + score_by_outcome['lose'],
        'C Z': score_by_my_shape[my_shapes_to_standart['Z']] + score_by_outcome['draw'],
    }

    for current_round in lines:
        current_round_score = score_by_pairs[current_round[:3]]
        total_score += current_round_score
    return total_score


def part_2():
    total_score = 0
    how_to_achieve_outcome = {
        'rock':     {
            'win':  'paper',
            'draw': 'rock',
            'lose': 'scissors',
        },
        'paper':    {
            'win':  'scissors',
            'draw': 'paper',
            'lose': 'rock',
        },
        'scissors': {
            'win':  'rock',
            'draw': 'scissors',
            'lose': 'paper',
        }
    }
    expected_outcome_to_standart = {
        'X': 'lose',
        'Y': 'draw',
        'Z': 'win',
    }
    for current_round in lines:
        opponent, expected_outcome = current_round[:3].split()
        current_round_score = 0
        shape_to_select = how_to_achieve_outcome[
            opponent_shapes_to_standart[opponent]
        ][
            expected_outcome_to_standart[expected_outcome]
        ]
        current_round_score += score_by_my_shape[shape_to_select]
        current_round_score += score_by_outcome[expected_outcome_to_standart[expected_outcome]]
        total_score += current_round_score
    return total_score


print(part_1())
print(part_2())

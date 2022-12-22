#!/usr/bin/env python3

day_number = int(input('day number: '))
print(f'cp -r dayN day{day_number}')
print(f'git add day{day_number}')
print(f'git commit -m "day {day_number} prepared"')

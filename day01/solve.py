with open('input.txt') as f:
    lines = f.readlines()

calories_by_deer = [0]

for i in lines:
    if i == '\n':
        calories_by_deer.append(0)
    else:
        calories_by_deer[-1] += int(i)

print(max(calories_by_deer))
calories_by_deer.sort(reverse=True)
print(sum(calories_by_deer[:3]))

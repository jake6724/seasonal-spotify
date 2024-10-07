import pandas as pd

df = pd.read_csv('billboard-200-current.csv')

title_counter = {}
for index, row in df.iterrows():
	title = str(row['performer']) + " " + str(row['title'])
	if title in title_counter:
		title_counter[title] += 1
	else:
		title_counter[title] = 1

# for key, value in sorted(title_counter.items(), key=lambda item: item[1]):
# 	print(f'{key}: {value}')
print(len(title_counter))

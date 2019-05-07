f = open('table.html', encoding='utf-8')
f1 = open('table1.html', encoding='utf-8')
f1 = open('table1.html', 'w', encoding='utf-8')
for line in f:
    if line == '\n':
            continue
    line = line.replace(' ', '')
    line = line.replace('\t', '')
    f1.write(line)
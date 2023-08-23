import os
cwd = os.path.join(os.getcwd(),"OneDrive","바탕 화면","test_program")
groups = ['Group 1.txt', 'Group 2.txt', 'Group 3.txt', 'Group 4.txt', 'Group 5.txt', 'Group 6.txt']
cumulative_lengths = []
origins = []
origin_index = 0
for group_index in range(len(groups)):
    group = groups[group_index]
    filename = os.path.join(cwd, group)
    
    if not os.path.isfile(filename):
        # print(filename)
        continue
    
    with open(filename,'r', encoding='utf-8') as f:
        num_lines = 0
        while True:
            line = f.readline()
            if not line:break
            if len(line) < 2:
                print(line)
                continue
            origins.append(line.split('/-/')[0])
            num_lines += 1
        cumulative_lengths.append(len(origins))

        for i in range(origin_index, origin_index + num_lines):
            for j in range(i):
                if origins[i] == origins[j]:
                    k = len(cumulative_lengths)-1
                    while k >= 0:
                        if cumulative_lengths[k] <= j:
                            break
                        k -= 1
                    k += 1
                    print(groups[k], group)
                    print(origins[i])
                    print()
                            
        origin_index += num_lines
    print()
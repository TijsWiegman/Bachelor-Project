import json
import os

script_dir = os.path.dirname(__file__)
file_names = []   # List of file names excluding the numbering

for file_name in file_names:
    targets = {}
    last_elapsed = []
    for i in range(1,11):
        targets[str(i)] = []
        file_path = os.path.join(script_dir, file_name+' #'+str(i)+'.json')
        with open(file_path, 'r') as file:
            lines = file.readlines()
            targets[str(i)] = [json.loads(line)['target'] for line in lines]
            last_elapsed.append(float(json.loads(lines[-1])['elapsed']))

    ave_targets = []
    for j in range(len(targets['1'])):
        ave_target = sum(targets[str(i)][j] for i in range(1, 11)) / 10
        ave_targets.append(ave_target)

    ave_elapsed = sum(last_elapsed) / 10

    ave_file_name = 'average '+ file_name
    ave_file_path = os.path.join(script_dir, ave_file_name+'.json')
    with open(ave_file_path, 'w') as file:
        # Write the average targets list in the first line of the average .json file
        json.dump(ave_targets, file)
        file.write('\n')  # Add a newline
        # Write the average elapsed time on the second line
        json.dump(ave_elapsed, file)

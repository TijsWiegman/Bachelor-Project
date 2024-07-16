import json
import os
import math

script_dir = os.path.dirname(__file__)
file_names = ['pyGPGO mei xi=1E-2','pyGPGO ucb']

for file_name in file_names:
    targets = {}
    for i in range(1,11):
        targets[str(i)] = []
        file_path = os.path.join(script_dir, file_name+' #'+str(i)+'.json')
        with open(file_path, 'r') as file:
            targets[str(i)] = [json.loads(line)['target'] for line in file]

    ave_targets = []
    std_targets = []
    for j in range(len(targets['1'])):
        ave_target = (targets[str(1)][j] + targets[str(2)][j] + targets[str(3)][j] + targets[str(4)][j] + targets[str(5)][j] + targets[str(6)][j] + targets[str(7)][j] + targets[str(8)][j] + targets[str(9)][j] + targets[str(10)][j])/10
        ave_targets.append(ave_target)

    for j in range(len(targets['1'])):
        std_target = math.sqrt(sum([(targets[str(k)][j] - ave_targets[j]) ** 2 for k in range(1, 11)]) / (10 - 1))
        std_targets.append(std_target)

    ave_file_name = 'sample std dev ' + file_name
    ave_file_path = os.path.join(script_dir, ave_file_name+'.json')
    with open(ave_file_path, 'w') as file:
        # write the average targets list in the first line of the average .json file
        json.dump(std_targets,file)

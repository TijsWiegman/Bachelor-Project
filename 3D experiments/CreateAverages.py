import json
import os

script_dir = os.path.dirname(__file__)
file_names = ['ei xi=0','mei xi=1E-4','mei xi=1E-2','mei xi=0.1','dmei']  # List to store file names

for file_name in file_names:
    targets = {}
    deltas = {}
    for i in range(1,11):
        targets[str(i)] = []
        deltas[str(i)] = []
        file_path = os.path.join(script_dir, file_name+' #'+str(i)+'.json')
        with open(file_path, 'r') as file:
            targets[str(i)] = [json.loads(line)['target'] for line in file]
        with open(file_path, 'r') as file:
            deltas[str(i)] = [json.loads(line)['datetime']['delta'] for line in file]

    ave_targets = []
    ave_deltas = []
    elapsed_times = []
    for j in range(len(targets['1'])):
        ave_target = (targets[str(1)][j] + targets[str(2)][j] + targets[str(3)][j] + targets[str(4)][j] + targets[str(5)][j] + targets[str(6)][j] + targets[str(7)][j] + targets[str(8)][j] + targets[str(9)][j] + targets[str(10)][j])/10
        ave_targets.append(ave_target)
        ave_delta = (deltas[str(1)][j] + deltas[str(2)][j] + deltas[str(3)][j] + deltas[str(4)][j] + deltas[str(5)][j] + deltas[str(6)][j] + deltas[str(7)][j] + deltas[str(8)][j] + deltas[str(9)][j] + deltas[str(10)][j])/10
        ave_deltas.append(ave_delta)
        elapsed_time = sum(ave_deltas)
        elapsed_times.append(elapsed_time)

    ave_file_name = 'average '+ file_name
    ave_file_path = os.path.join(script_dir, ave_file_name+'.json')
    with open(ave_file_path, 'w') as file:
        # write the average targets list in the first line of the average .json file
        json.dump(ave_targets,file)
        # start a new line
        file.write("\n")
        # write the average deltas list in the second line of the average .json file
        json.dump(ave_deltas,file)
        # start yet another new line
        file.write("\n")
        # write the elapseds time list in the third line of the average .json file
        json.dump(elapsed_times,file)

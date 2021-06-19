import yaml
import time
import amulet
import csv

from amulet.api.block import Block

# Load config
with open(r"config.yaml") as data:
    try:
        config = yaml.safe_load(data)
    except yaml.YAMLError as e:
        print(e)

# Create results dictionary and initialize block targets
results = {}

for target in config['blocks']:
    results[target[10:]] = {}

# Variables to track run time
searched = 0
start_time = time.time()

# Load world and set data format
level = amulet.load_level(config['world'])
game_version = ("java", (1, 17, 0))

# Iterate over every selected coordinate
for y in range(config['yMin'], config['yMax']+1):
    for x in range(config['xBlocks']):
        for z in range(config['zBlocks']):
            # Get block at the coordinate
            block, _ = level.get_version_block(x + config['xCoord'], y, z + config['zCoord'], "minecraft:overworld", game_version)

            # Check that block is actually block
            if not isinstance(block, Block): continue

            # Check if block is in targeted list
            for target in config['blocks']:
                if block.namespaced_name == target:
                    
                    # If we haven't seen the target on this y level before, add it
                    if y not in results[target[10:]]:
                        results[target[10:]][y] = 0
                    
                    # Increment target count for this y level
                    results[target[10:]][y] += 1

                    print("found target {name} at {coordX}, {coordY}, {coordZ}".format(coordX=x + config['xCoord'], coordY=y, coordZ=z + config['zCoord'], name = block.namespaced_name))
            searched += 1

level.close()

for target in results:
    with open("results/{block}.csv".format(block=target), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Y Level", "Blocks Found"])
        for y in results[target]:
            writer.writerow([y, results[target][y]])

print(results)
print("searched {count} blocks in {time} seconds".format(count=searched, time=time.time()-start_time))
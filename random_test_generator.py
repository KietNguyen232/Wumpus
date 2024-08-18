import random

def random_map_generator(n = 10,
                         agent_loc = (0, 0),
                         n_wumpus = 10,
                         n_pit = 10,
                         n_gold = 10,
                         n_gas = 10,
                         n_potion = 10):
    
    # Get dictionary of parameters
    params = locals()

    # Random the number of objects in range
    for key, val in params.items():
        if (key == 'n' or key == 'agent_loc'): continue
        params[key] = random.randint(1, val)

    # Generate map with agent
    wmap = [['' for _ in range(n)] for _ in range(n)]
    wmap[agent_loc[0]][agent_loc[1]] += 'A'

    # Generate valid location for objects
    sample_set = [i for i in range(n*n)]
    sample_set.remove(agent_loc[0]*n + agent_loc[1])

    # Get random locations for objects
    loc_dict = {}
    for key, val in params.items():
        if (key == 'n' or key == 'agent_loc'): continue
        loc_dict[key.partition('n_')[2]] = random.sample(sample_set, val)

    # Append the objects to each tile
    char_map = {'wumpus':'W', 'pit':'P', 'gold':'G', 'gas':'P_G', 'potion':'H_P'}
    for key in loc_dict:
        char = char_map[key]
        for loc in loc_dict[key]:
            wmap[loc//n][loc%n] += ' ' if wmap[loc//n][loc%n] != '' else ''
            wmap[loc//n][loc%n] += char
    
    # Set blank tiles to '-'
    wmap = [[tile if tile != '' else '-' for tile in row] for row in wmap]

    # Convert 2d array to full string
    testcase = f'{n}\n' + '\n'.join(['.'.join(row) for row in wmap])

    with open("testcase.txt", "a") as f:
        f.write(testcase)
    return testcase

random_map_generator(n=10, agent_loc=(0, 0), n_wumpus=10, n_pit=10, n_gold=10, n_gas=10, n_potion=10)
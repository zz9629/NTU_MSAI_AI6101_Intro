import numpy as np
'''
*************************************************************************
 *
 * Map struct ->  BoxPushing grid-world game
 *          ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
 *          │ 0 │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │ 8 │ 9 │1 0│1 1│1 2│1 3│
 *      ┌───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 *      │ 0 │   │   │   │   │   │   │   │   │   │   │   │   │   │   │
 *      ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 *      │ 1 │   │   │   │   │   │   │   │   │   │   │   │   │   │   │
 *      ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 *      │ 2 │   │   │   │   │   │   │   │   │   │   │   │   │   │   │
 *      ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 *      │ 3 │   │   │   │   │   │   │   │   │   │   │   │   │   │   │
 *      ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 *      │ 4 │   │ B │   │▓▓▓│▓▓▓│▓▓▓│▓▓▓│▓▓▓│▓▓▓│▓▓▓│▓▓▓│▓▓▓│ G │   │
 *      ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 *      │ 5 │ A │   │▓▓▓│▓▓▓│▓▓▓│▓▓▓│▓▓▓│▓▓▓│▓▓▓│▓▓▓│▓▓▓│▓▓▓│▓▓▓│   │
 *      └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
 *      A->Agent, B->Box, G->Goal, ▓▓▓->Cliff
 *      
*************************************************************************
'''
def DrawAboveLine():
    print('    ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐')
    print('    │ 0 │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │ 8 │ 9 │1 0│1 1│1 2│1 3│')
    print('┌───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤')


def DrawMiddleLine():
    print('├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤')


def DrawBelowLine():
    print('└───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘')


def GetActionArrow(Q, raw, col, box_loc):
    '''
    Function for extract the max Q-value in a specific Q-table location
    Then show the action with the arrow representation

    Parameters
    ----------
    Q : this is the Q-table we use
    raw, col : these are the target agent block location, the index in Q-table
    box_loc : this is the box location, which is also the index in Q-table

    Returns
    -------
    arr : str
        the arrow showing the action in Q-table

    '''
    state = ((raw, col), box_loc)
    if Q[state].any() == 0:
        arr = ' '
    else:
        arrows = ['↑', '↓', '←', '→']
        arr = arrows[np.argmax(Q[state])]
    return arr


def DrawBlock(Q, raw, col, agent_loc, box_loc, goal_loc, cliff_loc):
    '''
    Function for draw the specific block in the map
    Use A->Agent, B->Box, G->Goal, ▓▓▓->Lava, and Arrows for Q value-actions.

    Parameters
    ----------
     Q : this is the Q-table we use
     raw, col : these are the target block location
     agent_loc, box_loc, goal_loc - these are the map data
    '''
    if agent_loc == (raw, col):
        print(' A │', end='')
    elif box_loc == (raw, col):
        print(' B │', end='')
    elif goal_loc == (raw, col):
        print(' G │', end='')
    elif (raw, col) in cliff_loc:
        print('▓▓▓│', end='')
    else:
        arr = GetActionArrow(Q, raw, col, box_loc)
        print(' ' + arr + ' │', end='')


def DrawEmptyBlock(raw, col, agent_loc, box_loc, goal_loc, cliff_loc):
    '''
    The another version of function for draw the specific block in the map
    Use A->Agent, B->Box, G->Goal, ▓▓▓->Cliff,
    Here, we don't fill the block with arrows but leave them empty.
    '''
    if agent_loc == (raw, col):
        print(' A │', end='')
    elif box_loc == (raw, col):
        print(' B │', end='')
    elif goal_loc == (raw, col):
        print(' G │', end='')
    elif (raw, col) in cliff_loc:
        print('▓▓▓│', end='')
    else:
        print('   │', end='')


def DrawMap(Q, agent_loc, box_loc, goal_loc, cliff_loc):
    '''
    Function for draw the whole map with the states currently.
    Use A->Agent, B->Box, G->Goal, ▓▓▓->Cliff, and Arrows for Q value-actions.

    Parameters
    ----------
     Q : this is the Q-table we use
     agent_loc, box_loc, goal_loc, cliff_loc : these are the map data
    '''
    DrawAboveLine()
    for raw in range(6):
        print('│ ' + str(raw) + ' │', end='')
        for col in range(14):
            DrawBlock(Q, raw, col, agent_loc, box_loc, goal_loc, cliff_loc)
            if col == 13:
                print('')
        if raw == 5:
            DrawBelowLine()
        else:
            DrawMiddleLine()
    action_cur = GetActionArrow(Q, agent_loc[0], agent_loc[1], box_loc)
    print('Agent Action Now: ' + action_cur)


def DrawEmptyMap(agent_loc, box_loc, goal_loc, cliff_loc):
    '''
    The another version of function for draw the whole map
    Use A->Agent, B->Box, G->Goal, ▓▓▓->Lava,
    Here, we don't fill the block with arrows but leave them empty.
    '''
    DrawAboveLine()
    for raw in range(6):
        print('│ ' + str(raw) + ' │', end='')
        for col in range(14):
            DrawEmptyBlock(raw, col, agent_loc, box_loc, goal_loc, cliff_loc)
            if col == 13:
                print('')
        if raw == 5:
            DrawBelowLine()
        else:
            DrawMiddleLine()
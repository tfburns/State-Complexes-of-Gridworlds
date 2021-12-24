# State Complexes of Gridworlds

This repository contains two Python files:
- `worldbuilder.py`, a GUI made using `Kivy` for the creation of small, simple gridworlds; and
- `cubical_complex_constructor.py`, a script which will take the saved gridworld from the GUI, create its cubical complex, and .

You shouldn't need to edit `worldbuilder.py` for general usage (unless you want to add features - which you are very welcome to!), however there are some additional plots and options available in `cubical_complex_constructor.py` which are be default commented out.

## Installation

After cloning the repository, install dependencies using:
```
pip install -r requirements.txt
```

Assuming these are all installed correctly, you should be good to go. This repo was tested with the Anaconda environment provided in `conda_env.yml`.

## Usage

### Gridworld Builder

Run `worldbuilder.py`.
```
python worldbuilder.py
```
A small GUI window should open.

You should see a grid of grey cells labelled with (1, 1) in the top-left and ending in (12, 12) in the bottom-right. These 120 cells are assignable, individual cells within your gridworld. By default, all gridworld cells are unassigned and therefore do not exist. To assign them to be part of the gridworld, simply click on the desired cells. Doing so after initial loading will assign them to the gridworld `area`.

By default, all `area` cells are assumed to be unoccupied, meaning an `agent` or `object` could in the future occupy it. If you don't want an `area` cell to be able to be occupied, you need to then assign it to be a `wall`. To do this, click the `Options` button at the bottom of the GUI. Now click the `wall` button (it will become highlighted), and now click the `Grid View` button at the bottom of the GUI to go back to the grid world builder. Now clicking with your cursor in `area` cells will assign them as a `wall` cell. For the purposes of the `cubical_complex_constructor.py` script, it is important that the entire gridworld area is bordered by `wall` cells on all sides (this is especially important for grid worlds which include objects).

If you wish for there to be an agent (or multiple agents) in your gridworld, set their starting position(s) to an unoccupied `area` cell by going into the options menu and clicking `Start`, then returning to the grid view and assigning those cells. You may also set goal and object cells in the same way by clicking `Goal` or `Object` in the options menu (although `Goal` cells are currently not supported).

There are two more important rules for using the `worldbuilder.py`:
1. Only unoccupied `area` cells may have the additional assignments of `object`, `start`, or `goal` - but never more than one of these assignments!
2. The Kivy app may not close neatly on some machines. If you find it does not close neatly, you may need to force-quit the Kivy app and/or restart your Python kernel.

Once you are happy with the gridworld you've constructed, click the `Create & Save World Graph` in the options menu. This will create a number of files in a folder named `results` in your local directory which will used by the `cubical_complex_constructor.py` script.

### State Complex Builder

To quote Anakin Skywalker: this is where the fun begins.

If you run this script as-is, `cubical_complex_constructor.py` will proceed to:
- load your created gridworld from its local directory
- construct a graph representation of this gridworld using `networkx`
- plot the gridworld in graph form
- construct a state complex of the graph using two generators (described below), using `networkx`
- plot a two-dimensional projection of the state complex (one with commuting move squares shaded and another with dance squares shaded)
- perform Gromov's Link Condition test for each vertex in the state complex
- plot the local subgraph around each vertex used during the Gromov's Link Condition test
- plot the state complex, labelling each vertex with the number of failures of the Gromov's Link Condition test for that vertex (0 failures means it is non-positively curved)
- save some data about the state complex to `_stats.txt`

All plots should be automatically saved in a folder called `result` in your local directory.

The two generators which `cubical_complex_constructor.py` uses are:
1. An `agent (A)` can move to adjacent cell in the gridworld if it is `empty (E)`, i.e.

A - E

becomes

E - A

2. An `agent (A)` can push or pull an object if there is `empty space (E)` behind the `object (O)` (for pushing) or behind the agent (for pulling), and where `W`s (wildcards) represent cells of any other type, i.e.

A - O - E

W - W - W

becomes

E - A - O

W - W - W

(and vice-versa)

Of course, if you wish to do more than just the above, you will need to dig into the code a bit. I may in the future make this whole repo into something more user-friendly, but for now this is it. I hope that comments within the code and a few Google searches are enough to tide you through, but if not and you require any assistance, please feel free to contact me via GitHub :)

## Example

An example of a 3x3 room with 2 agents is provided in the `result` folder of this repository.

## References

For more information on state complexes, especially cubical complexes (which by the nature of gridworlds, we are building here), I recommend reading
```
R. Ghrist & V. Peterson (2007) The geometry and topology of reconfiguration Advances in Applied Mathematics 38:302–323
```

And for information about gridworlds and their broad importance to AI research as toy examples, I suggest reading
```
J. Leike et al. (2017) AI Safety Gridworlds arXiv:1711.09883v2
```

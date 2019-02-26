# State Complexes of Gridworlds

This bare-bones repository contains two Python files:
- `worldbuilder.py`, a GUI made using `Kivy` for the creation of small, simple gridworlds; and
- `cubical_complex_constructor.py`, a script which will take the saved gridworld from the GUI and create a cubical complex.

You will also find a `WorldBuilder.kv` file. This is just a GUI builder file. You shouldn't need to edit it or the `worldbuilder.py` file for general usage (unless you want to add features - which you are very welcome to!).

## Installation

After cloning the repository, install dependencies using:
```
pip install -r requirements.txt
```

Assuming these are all installed correctly, you should be good to go.

## Usage

### Gridworld Builder

Run `worldbuilder.py`.
```
python worldbuilder.py
```
A small GUI window should open.

You should see a grid of grey cells labelled with (1, 1) in the top-left and ending in (10, 10) in the bottom-right. These 100 cells are assignable, individual cells within your gridworld. By default, all gridworld cells are unassigned and therefore do not exist. To assign them to be part of the gridworld, simply click on the desired cells. Doing so after initial loading will assign them to the gridworld `area`.

By default, all `area` cells are assumed to be unoccupied, meaning an `agent` or `object` could in the future occupy it. If you don't want an `area` cell to be able to be occupied, you need to then assign it to be a `wall`. To do this, click the `Options` button at the bottom of the GUI. Now click the `wall` button (it will become highlighted), and now click the `Grid View` button at the bottom of the GUI to go back to the grid world builder. Now clicking with your cursor in `area` cells will assign them as a `wall` cell. For the purposes of the `cubical_complex_constructor.py` script, it is important that entire gridworld area is bordered by `wall` cells on all sides (this is especially important for grid worlds which include objects).

If you wish for there to be an agent (or multiple agents) in your gridworld, set their starting position to an unoccupied `area` cell by going into the options menu and clicking `Start`. You may also set goal nodes in the same way by clicking `Goal`. And you may set initial object positions by the same method and clicking `Object`.

There are two more important rules for using the `worldbuilder.py`:
1. Only unoccupied `area` cells may have the additional assignments of `object`, `start`, or `goal` - but never more than one of these assignments!
2. It is a bit buggy. Please be patient with it, and avoid changing cell assignments back-and-forth too much.

Once you are happy with your the gridworld you've constructed, click the `Create & Save World Graph` in the options menu. This will create a number of files used by the `cubical_complex_constructor.py` script in your local directory.

### State Complex Builder

To quote Anakin Skywalker: this is where the fun begins.

If you run this script as-is, `cubical_complex_constructor.py` will proceed to:
- load your created gridworld from its local directory
- construct an undirected graphical representation of this gridworld using `networkx`
- plot the graph
- construct a state complex of the graph using two generators (described below), using `networkx`
- plot a two-dimensional projection of the state complex
- take a random walk of n=50 steps through the state complex, plotting each step and then creating an animated GIF of this random walk

All plots should be automatically saved in your local directory.

The two generators which `cubical_complex_constructor.py` uses are:
1. An `agent (A)` can move to adjacent cell in the gridworld if it is `empty (E)`, i.e.

A-E

becomes

E-A

2. An `agent (A)` can push or pull an object if there is `empty space (E)` behind the `object (O)` (for pushing) or behind the agent (for pulling), and where `*`s represent cells of any other type, i.e.

A-O-E

*-*-*

becomes

E-A-O

*-*-*

(and vice-versa)

## References

For more information on state complexes, especially cubical complexes (which by the nature of gridworlds, we are building here), I recommend reading
```
R. Ghrist & V. Peterson (2007) The geometry and topology of reconfiguration Advances in Applied Mathematics 38:302–323
```

And for information about gridworlds and their broad importance to AI research as toy examples, I suggest reading
```
J. Leike et al. (2017) AI Safety Gridworlds arXiv:1711.09883v2
```

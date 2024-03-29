# -*- coding: utf-8 -*-
"""
@author: Tom
"""

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.uix.togglebutton import ToggleButton
from ast import literal_eval as make_tuple
import networkx as nx
import matplotlib.pyplot as plt
import pickle

class Boxes(FloatLayout):
    def __init__(self, **kwargs):
        super(Boxes, self).__init__(**kwargs)

        self.EditMode = 'Area'

        class AttrDict(dict):
            pass
        bxs = AttrDict()
        btns = AttrDict()

        self.WorldArea = {}
        self.WorldStart = {}
        self.WorldGoal = {}
        self.WorldObject = {}
        self.WorldWall = {}

        def GridButtonCallback(instance):
            ButtonText = instance.text
            #print('The button %s is being pressed' % ButtonText)

            # toggle the button's appearance and keep a track of its status (True or False) with respect to moveable world area, start node, and goal node

            if self.EditMode == 'Area':
                if instance.background_color == [1,1,1,1]:
                    instance.background_color = [0.5,0.5,0.5,0.5]
                    self.WorldArea[make_tuple(ButtonText)] = True
                else:
                    instance.background_color = [1,1,1,1]
                    self.WorldArea[make_tuple(ButtonText)] = False

            elif self.EditMode == 'Start':
                if instance.background_color == [0.5,0.5,0.5,0.5]:
                    instance.background_color = [0,1,0,0.75]
                    self.WorldStart[make_tuple(ButtonText)] = True
                elif instance.background_color == [0,1,0,0.75]:
                    instance.background_color = [0.5,0.5,0.5,0.5]
                    self.WorldStart[make_tuple(ButtonText)] = False

            elif self.EditMode == 'Goal':
                if instance.background_color == [0.5,0.5,0.5,0.5]:
                    instance.background_color = [1,0,0,0.75]
                    self.WorldGoal[make_tuple(ButtonText)] = True
                elif instance.background_color == [1,0,0,0.75]:
                    instance.background_color = [0.5,0.5,0.5,0.5]
                    self.WorldGoal[make_tuple(ButtonText)] = False

            elif self.EditMode == 'Object':
                if instance.background_color == [0.5,0.5,0.5,0.5]:
                    instance.background_color = [0,0,1,0.75]
                    self.WorldObject[make_tuple(ButtonText)] = True
                elif instance.background_color == [0,0,1,0.75]:
                    instance.background_color = [0.5,0.5,0.5,0.5]
                    self.WorldObject[make_tuple(ButtonText)] = False

            elif self.EditMode == 'Wall':
                if instance.background_color == [0.5,0.5,0.5,0.5]:
                    instance.background_color = [0,0,0,0.75]
                    self.WorldWall[make_tuple(ButtonText)] = True
                elif instance.background_color == [0,0,0,0.75]:
                    instance.background_color = [0.5,0.5,0.5,0.5]
                    self.WorldWall[make_tuple(ButtonText)] = False

        # top anchor (grid and options screens)
        top_anchor = AnchorLayout(anchor_x='center', anchor_y='top')
        self.add_widget(top_anchor)
        self.screen_manager = ScreenManager(size_hint=(1, .9))
        top_anchor.add_widget(self.screen_manager)

        # grid layout
        grid_screen = Screen(name='grid')
        self.screen_manager.add_widget(grid_screen)
        grid_layout = GridLayout(rows=12, cols=12)
        for j in range(1,13):
            for i in range(1,13):
                btn = Button(text=str((j,i)), on_press=GridButtonCallback)
                grid_layout.add_widget(btn)
        grid_screen.add_widget(grid_layout)

        # options layout
        options_screen = Screen(name='options')
        self.screen_manager.add_widget(options_screen)
        options_layout = GridLayout(cols=2, padding=50)
        save_button = Button(text='Create & Save World Graph', size_hint=(.5, .1))
        save_button.bind(on_press=self.CreateWorldGraph)
        options_layout.add_widget(save_button)

        def toggle_callback(instance):
            self.EditMode = instance.text
        toggle_buttons_layout = StackLayout()
        toggle_button_list = ["Area", "Start", "Goal", "Object", "Wall"]
        for i in toggle_button_list:
            toggle_buttons_widget = ToggleButton(text=i, size_hint=(.5, .1), group='a', on_press=toggle_callback)
            toggle_buttons_layout.add_widget(toggle_buttons_widget)
        options_layout.add_widget(toggle_buttons_layout)
        options_screen.add_widget(options_layout)

        # bottom anchor (screen navigation)
        bottom_anchor = AnchorLayout(anchor_x='center', anchor_y='bottom')
        self.add_widget(bottom_anchor)
        bottom_box = BoxLayout(orientation='horizontal', size_hint=(1, .1))
        bottom_anchor.add_widget(bottom_box)
        def grid_callback(instance):
            self.screen_manager.current='grid'
        def options_callback(instance):
            self.screen_manager.current='options'
        bottom_box.add_widget(Button(text='Grid View', on_press=grid_callback))
        bottom_box.add_widget(Button(text='Options', on_press=options_callback))

    def CreateWorldGraph(self, instance):
        # reduce dictionaries to selected (True) world area
        self.WorldArea = {k: v for k, v in self.WorldArea.items() if v is True}
        self.WorldStart = {k: v for k, v in self.WorldStart.items() if v is True}
        self.WorldGoal = {k: v for k, v in self.WorldGoal.items() if v is True}
        self.WorldObject = {k: v for k, v in self.WorldObject.items() if v is True}
        self.WorldWall = {k: v for k, v in self.WorldWall.items() if v is True}

        # convert WorldArea into uniquely numbered graph nodes
        self.WorldNodes = {}
        num = 0
        for key in self.WorldArea:
            self.WorldNodes[num] = key
            num +=1

        # use graph node adjacency information (self.WorldArea) to create a list of edges between the nodes (self.WorldNodes)
        self.WorldEdgesDirected = []
        for thisKey in self.WorldNodes:
            yGrid = self.WorldNodes[thisKey][0]
            xGrid = self.WorldNodes[thisKey][1]

            otherNodes = dict(self.WorldNodes)
            otherNodes.pop(thisKey)

            for otherKey in otherNodes:
                otherY = otherNodes[otherKey][0]
                otherX = otherNodes[otherKey][1]

                if  otherY == yGrid:
                    if xGrid+1 >= otherX >=xGrid-1:
                        self.WorldEdgesDirected.append([thisKey,otherKey])

                elif otherX == xGrid:
                    if yGrid+1 >= otherY >=yGrid-1:
                        self.WorldEdgesDirected.append([thisKey,otherKey])

        # construct the directed and undirected graphs from edges
        self.DirectedG = nx.Graph()
        self.DirectedG.add_edges_from(self.WorldEdgesDirected)

        self.WorldEdgesUndirected = {tuple(item) for item in map(sorted, self.WorldEdgesDirected)} # remove symmetrical edges
        self.UndirectedG = nx.Graph()
        self.UndirectedG.add_edges_from(self.WorldEdgesUndirected)

        # identify special nodes and their labels
        start_node = []
        goal_node = []
        object_node = []
        wall_node = []
        for i in range(0,len(self.WorldStart)):
            start_node.append(list(self.WorldNodes.keys())[list(self.WorldNodes.values()).index(list(self.WorldStart.keys())[i])])
        for i in range(0,len(self.WorldGoal)):
            goal_node.append(list(self.WorldNodes.keys())[list(self.WorldNodes.values()).index(list(self.WorldGoal.keys())[i])])
        for i in range(0,len(self.WorldObject)):
            object_node.append(list(self.WorldNodes.keys())[list(self.WorldNodes.values()).index(list(self.WorldObject.keys())[i])])
        for i in range(0,len(self.WorldWall)):
            wall_node.append(list(self.WorldNodes.keys())[list(self.WorldNodes.values()).index(list(self.WorldWall.keys())[i])])

        node_order = list(self.UndirectedG.nodes())
        start_order = []
        for j in range(0,len(start_node)):
            start_order.append(node_order.index(start_node[j]))
        goal_order = []
        for j in range(0,len(goal_node)):
            goal_order.append(node_order.index(goal_node[j]))
        object_order = []
        for j in range(0,len(object_node)):
            object_order.append(node_order.index(object_node[j]))
        wall_order = []
        for j in range(0,len(wall_node)):
            wall_order.append(node_order.index(wall_node[j]))

        node_IDs = [start_node, goal_node, object_node, wall_node]
        node_orders = [start_order, goal_order, object_order, wall_order]

        # add colour information to the graph for special nodes
        regular_colour = [0.5,0.5,0.5,0.5]
        start_colour = [0,1,0,1]
        goal_colour = [1,0,0,1]
        object_colour = [0,0,1,1]
        wall_colour = [1,1,1,0.5]

        node_colours = []
        for i in range(0,len(self.WorldArea)):
            node_colours.append(regular_colour)

        for k in start_order:
            node_colours[k] = start_colour
        for k in goal_order:
            node_colours[k] = goal_colour
        for k in object_order:
            node_colours[k] = object_colour
        for k in wall_order:
            node_colours[k] = wall_colour

        # plot and save the undirected graph
        nx.draw_networkx(self.UndirectedG, pos=self.WorldNodes, node_color=node_colours)
        plt.axis('off')
        plt.savefig("result/world_graph.png", dpi=300)
        plt.show()
        nx.write_gpickle(self.UndirectedG, "result/graph.gpickle")
        print("saved files")

        # save the position and node identity information       
        outfile_WorldNodes = open('result/node_positions','wb')
        pickle.dump(self.WorldNodes,outfile_WorldNodes)
        outfile_WorldNodes.close()
        outfile_Nodes = open('result/node_IDs','wb')
        pickle.dump(node_IDs,outfile_Nodes)
        outfile_Nodes.close()
        outfile_Orders = open('result/node_orders','wb')
        pickle.dump(node_orders,outfile_Orders)
        outfile_Orders.close()

class WorldBuilder(App):
    def build(self):
        return Boxes()

if __name__ == '__main__':
    WorldBuilder().run()

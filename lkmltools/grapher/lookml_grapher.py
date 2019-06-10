'''
    grapher: creates an image showing the relationship among the models, explores and views

    Authors:
            Carl Anderson (carl.anderson@weightwatchers.com)

'''
import glob
import os
import logging
import datetime
from enum import Enum
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from lkmltools.lookml import LookML

class NodeType(Enum):
    '''types of node'''
    MODEL = 'model'
    EXPLORE = 'explore'
    VIEW = 'view'
    ORPHAN = 'orphan'

class LookMlGrapher():
    '''A LookML Grapher that parses a set of LookML files specified in some config
        and creates an image showing the relationship among the models, explores and views
    '''

    def __init__(self, config):
        '''instantiate this grapher

        Args:
            config (JSON): JSON configuration

        '''
        self.config = config
        self.lookml = LookML(config)

        # list of edge pair names
        self.models_to_explores = []
        self.explores_to_views = []

        # dict of node names with their type
        self.node_map = {}

    def plot_graph(self, g, filename, title, node_size=500, label_font_size=12, text_angle=0, image_width=16, image_height=12):
        '''plot the graph and write to file

        Args:
            g (networkx): networkx graph object
            filename (str): path to write image to
            title (str): title to add to chart
            node_size (int): node size 
            label_font_size (int): font size
            text_angle (int): angle to rotate. This is angle in degrees counter clockwise from east 
            image_width (int): width of image in inches 
            image_height (int): heightof image in inches

        Returns:
            nothing but does write image to file

        '''
        # map nodes to a color for their node type
        # https://stackoverflow.com/questions/27030473/how-to-set-colors-for-nodes-in-networkx-python
        color_map = []
        colors = ['#b3cde3', '#ccebc5', '#decbe4', '#FFA500']
        for node in g:
            if self.node_map[node] == NodeType.MODEL:
                color_map.append(colors[0])
            elif self.node_map[node] == NodeType.EXPLORE:
                color_map.append(colors[1])
            elif self.node_map[node] == NodeType.VIEW:
                color_map.append(colors[2])
            else:
                color_map.append(colors[3])

        fig = plt.figure(figsize=(image_width, image_height))
        ax = plt.subplot(111)

        try:
            import pydot
            from networkx.drawing.nx_pydot import graphviz_layout
        except ImportError: # pragma: no cover
            raise ImportError("Requires Graphviz and either PyGraphviz or pydot") # pragma: no cover

        #pos = nx.spring_layout(g)
        #pos = nx.circular_layout(g)
        #pos = nx.kamada_kawai_layout(g)
        #pos = nx.shell_layout(g)
        #pos = nx.spectral_layout(g)
        pos = graphviz_layout(g, prog='dot', seed=42)
        nx.draw(g, pos, node_size=node_size, node_color = color_map, edge_color='#939393', font_size=9, font_weight='bold')

        text = nx.draw_networkx_labels(g, pos, with_labels=False, font_size=label_font_size)
        for _, t in text.items():
            t.set_rotation(text_angle)

        plt.axis('off')
        plt.title(title, fontsize=20)
        plt.tight_layout()
        plt.savefig(filename, format="PNG")
        logging.info("Graph written to %s", filename)

    def tag_orphans(self):
        '''find any orphaned views and tag them as orphan node type

        Returns:
            nothing but side effect is that any orphans are tagged in the node map

        '''
        referenced_views = set([v[1] for v in self.explores_to_views])
        view_names = set([k for k in self.node_map if self.node_map[k] == NodeType.VIEW])
        orphans = view_names - referenced_views
        for orphan in orphans:
            self.node_map[orphan] = NodeType.ORPHAN

    def orphans(self):
        '''retrieve the set or orphaned views (if any) from the set of files

        Prerequisites:
            tag_orphans() has been called

        Returns:
            set of view names (if any)

        '''
        return set([k for k in self.node_map if self.node_map[k] == NodeType.ORPHAN])

    def create_graph(self):
        '''add nodes and edges to a graph

        Returns:
            instance of networkx graph

        '''
        g = nx.DiGraph()
        [g.add_node(node_name) for node_name in self.node_map]
        [g.add_edge(p[0], p[1]) for p in self.models_to_explores]
        [g.add_edge(p[0], p[1]) for p in self.explores_to_views]
        return g

    def process_explores(self, m, e):
        '''extract the views referenced by these explores and
        add them to node map and add explore-->view or model-->explores

        Args:
            m (str): model
            e (str): explore

        Returns:
            nothing. Side effect is to add to maps

        '''
        explore_name = e['_explore']
        self.node_map[explore_name] = NodeType.EXPLORE
        if m and '_model' in m:
            self.models_to_explores.append((m['_model'], explore_name))
        if 'from' in e:
            # this is the first view mentioned
            self.explores_to_views.append((explore_name, e['from']))
            #logging.info("Adding %s %s" % (explore_name, e['from']))

            # but there could be more mentioned in the list (if any) of joins
            if 'join' in e:
                for k in e['join']:
                    if not k.startswith('_'):
                        if 'from' in e['join'][k]:
                            # this is an edge from explore to a view contained within joined views
                            self.explores_to_views.append((explore_name, e['join'][k]['from']))

    def process_file(self, filepath, json_data=None):
        '''given a filepath to a LookML file, extract the views, models, explores as the nodes
        as well as any model-->explore and explore-->view edges

        Args:
            filepath (str): path to LookML file
            json_data (JSON): chunk of JSONified LookML code

        Returns:
            nothing but stores node names and their types as well as edges

        '''
        assert filepath or json_data
        if filepath and not json_data:
            logging.info("Processing %s", filepath)
            json_data = self.lookml.get_json_representation(filepath)

        if 'views' in json_data['files'][0]:
            for v in json_data['files'][0]['views']:
                self.node_map[v['_view']] = NodeType.VIEW
        elif 'models' in json_data['files'][0]:
            for m in json_data['files'][0]['models']:
                self.node_map[m['_model']] = NodeType.MODEL
                [self.process_explores(m, e) for e in m['explores']]
        elif 'explores' in json_data['files'][0]: 
            for e in json_data['files'][0]['explores']:
                self.process_explores(None, e)
        else:
            #logging.error("Issue with %s", filepath)
            raise Exception("No models, views, or explores? %s", filepath)

    def extract_graph_info(self, globstrings):
        '''given a list of fileglobs, process them to extract list of nodes and edges, and orphaned views

            Args:
                globstrings (list): list of globstrings

            Returns:
                nothing but side effect is that nodes are strored in self.node_map and self.models_to_explores 
                and self.explores_to_views are completed
        '''
        for globstring in globstrings:
            if list(glob.glob(globstring)) == []:
                raise Exception("Invalid glob %s" % globstring)

            for filepath in glob.glob(globstring):
                assert os.path.exists(filepath)
                self.process_file(filepath)
        self.tag_orphans()

    def run(self):
        '''process the set of files and create an image of the graph

            Returns:
                nothing. Saves an image file, specified in the config
        '''
        timestr = datetime.datetime.now().strftime("%Y-%m-%d")
        globstrings = self.config['infile_globs']
        self.extract_graph_info(globstrings)
        g = self.create_graph()

        args = {}
        args['g'] = g
        args['filename'] = self.config['output']
        args['title'] = " ".join(globstrings) + " as of " + timestr
        if 'options' in self.config:
            args.update(self.config['options'])

        logging.info("Setting the following options: %s" % args)

        self.plot_graph(**args)

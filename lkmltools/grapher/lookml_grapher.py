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
import pandas as pd

class NodeType(Enum):
    '''types of node'''
    MODEL = 'model'
    EXPLORE = 'explore'
    VIEW = 'view'
    ORPHAN = 'orphan'
    EMPTY = 'empty'

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
        pos = graphviz_layout(g, prog='dot')
        nx.draw(g, pos, node_size=node_size, node_color = color_map, edge_color='#939393', font_size=9, font_weight='bold')

        text = nx.draw_networkx_labels(g, pos, font_size=label_font_size)
        for _, t in text.items():
            logging.info(f"Text item to be included: {t}")
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

    def create_csv(self):
        '''use objects so far to create csv of file relationships

        Returns:
            csv with columns for model, explore, and view

        '''

        #turn our objects into dataframes and join them 
        m_e = pd.DataFrame(self.models_to_explores, columns = ['model', 'explore'])
        #m_e.to_csv('models_to_explores.csv', encoding='utf-8',  index=False)
        e_v = pd.DataFrame(self.explores_to_views, columns = ['explore', 'view'])
        #e_v.to_csv('explores_to_views.csv', encoding='utf-8',  index=False)
        relationships = (pd.merge(m_e, e_v, how='inner', on='explore'))

        #get orphans and join them to the file
        orphans = pd.DataFrame([k[0] for k in self.node_map.items() if k[1] in (NodeType.ORPHAN, NodeType.EMPTY)], columns = ['view'])
        all_files = pd.merge(relationships, orphans, how='outer', on='view')

        #write out a csv
        all_files = all_files.sort_values( by=['model', 'explore']).drop_duplicates()
        all_files.to_csv(self.config['csv_output'], encoding='utf-8', index=False)
        print(f"csv written to {self.config['csv_output']}")


    def create_graph_no_orphans(self):
        '''add nodes and edges to a graph without orphans

        Returns:
            instance of networkx graph

        '''

        orphanless_node_map = {k:v for k,v in self.node_map.items() if self.node_map[k] != NodeType.ORPHAN}

        g = nx.DiGraph()
        [g.add_node(node_name) for node_name in orphanless_node_map]
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
        if 'from' in e:
            if 'name' in e['from']:
                explore_name = e['from']['name']
                self.explores_to_views.append((explore_name, e['from']['name']))
            else:
                explore_name = e['from']
                self.explores_to_views.append((explore_name, e['from']))
        else:
            explore_name = e['name']
            self.explores_to_views.append((explore_name, e['name']))
        self.node_map[explore_name] = NodeType.EXPLORE
        if m:
            self.models_to_explores.append((m, explore_name))
        # if 'from' in e:
        #     # this is the first view mentioned
        #     self.explores_to_views.append((explore_name, e['from']))

        # but there could be more mentioned in the list (if any) of joins (even if there isn't a from in the explore)
        if 'joins' in e:
            for k in e['joins']:
                #add logic to use the view name where there is not a 'from' used
                if 'from' in k:
                    self.explores_to_views.append((explore_name, k['from']))
                else:
                    self.explores_to_views.append((explore_name, k['name']))

    def process_lookml(self, lookml):
        '''given a filepath to a LookML file, extract the views, models, explores as the nodes
        as well as any model-->explore and explore-->view edges

        Args:
            filepath (str): path to LookML file
            json_data (JSON): chunk of JSONified LookML code

        Returns:
            nothing but stores node names and their types as well as edges

        '''
        if lookml.has_views():
            for v in lookml.views():
                self.node_map[v['name']] = NodeType.VIEW
                viewname = self.node_map[v['name']]
                # logging.info(f"Found view {viewname}.")
        elif lookml.filetype == 'model':
            m = lookml.base_name
            logging.info(f"Found model {m}.")
            self.node_map[m] = NodeType.MODEL
            if lookml.explores():
                [self.process_explores(m, e) for e in lookml.explores()]
        elif lookml.filetype == 'explore':
            for e in lookml.explores():
                self.process_explores(None, e)
                # logging.info(f"Found model {e['name']}.")
        elif lookml.filetype == 'view':
            self.node_map[lookml.base_name] = NodeType.EMPTY
            # logging.info(f"Found empty node {lookml.base_name}.")
        else:
            raise Exception("No models, views, or explores? " + lookml.infilepath)

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
                logging.info("Processing " + filepath)
                lookml = LookML(filepath)
                self.process_lookml(lookml)
                logging.info(f"{filepath} processing complete.")
                logging.info(f"{filepath} LookLM type is {type(lookml)}")
                logging.info(f"{filepath} file type is {lookml.filetype}")
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
        '''
        Added by Neven (DAS42) for creating graph without orphan views.
        '''
        h = self.create_graph_no_orphans()

        args = {}
        args['g'] = g
        args['filename'] = self.config['output']

        args_no_orphans = {}
        args_no_orphans['g'] = h
        args_no_orphans['filename'] = "no_orphans" + self.config['output']

        if 'title' in self.config:
            args['title'] = self.config['title']
        else:
            args['title'] = " ".join(globstrings) + " as of " + timestr

        if 'title' in self.config:
            args_no_orphans['title'] = self.config['title']
        else:
            args_no_orphans['title'] = " ".join(globstrings) + " as of " + timestr

        if 'options' in self.config:
            args.update(self.config['options'])
            args_no_orphans.update(self.config['options'])

        logging.info("Setting the following options: %s" % args)
        logging.info("Setting the following options: %s" % args_no_orphans)

        self.plot_graph(**args)
        self.plot_graph(**args_no_orphans)
        self.create_csv()

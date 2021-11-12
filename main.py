from tkinter import *
from xml.dom import minidom
from pyvis.network import Network
from tkinter import filedialog


class MyUi:
    net = Network(directed=True)

    @classmethod
    def get_xml_location(cls):
        return filedialog.askopenfilename(title='select your xml', filetypes=(('xml files', '*.xml'), ('all files', '*.*')))


#node starts are in green and finishes are in red


    @classmethod
    def draw(cls, nodes, edges):
        for node in nodes:
            if node.type == 'initial_state':
                cls.net.add_node(node.name, label=node.name, color='green')
            elif node.type == 'final_state':
                cls.net.add_node(node.name, label=node.name, color='red')
            else:
                cls.net.add_node(node.name, label=node.name)

        for edge in edges:
            cls.net.add_edge(edge.origin, edge.destination, title=edge.label, arrowStrikethrough=True, color='black')

        cls.net.show('doc.html')


class Node:
    def __init__(self, name, type_of_node=NONE):
        self.name = name
        self.type = type_of_node


class Edge:
    def __init__(self, lable, origin, destination):
        self.label = lable
        self.origin = origin
        self.destination = destination


class Manager:
    nodes = []
    edges = []
    mydoc = None

    @classmethod
    def my_main(cls):
        ui = MyUi()
        cls.mydoc = minidom.parse(MyUi.get_xml_location())
        cls.read_xml_data_nodes()
        ui.draw(cls.nodes, cls.edges)


    @classmethod
    def read_xml_data_nodes(cls):
        items = cls.mydoc.getElementsByTagName('state')
        ini_state = cls.mydoc.getElementsByTagName('initialState')
        final_states = cls.mydoc.getElementsByTagName('finalState')
        
        for item in items:
            if item.attributes['name'].value == ini_state[0].attributes['name'].value:
                cls.nodes.append(Node(item.attributes['name'].value, "initial_state"))
            else:
                cls.nodes.append(Node(item.attributes['name'].value, "normal_state"))
                
        for node in cls.nodes:
            for fins in final_states:
                if fins.attributes['name'].value == node.name:
                    node.type = "final_state"
        
        cls.read_xml_data_edges()

    @classmethod
    def read_xml_data_edges(cls):
        items = cls.mydoc.getElementsByTagName('transition')
        for item in items:
            cls.edges.append(Edge(item.attributes['label'].value, item.attributes['source'].value, item.attributes['destination'].value))






def main():
    Manager.my_main()


if __name__ == '__main__':
    main()

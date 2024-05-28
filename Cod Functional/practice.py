from agent import Agent
from network import *
from content import *
from collections import defaultdict
from Product import *
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
import networkx as nx

# Function to update the plot for each frame, where i is each iteration
def update(i):
    plt.cla()
    if i == 0:  # iteration zero
        # Draw edges and nodes for the initial setup
        for node in Agent.allAgents:
            for connectedNode in node.connected:
                edge_colors[(node.id, connectedNode.id)] = 'gray'
                plt.plot([points[node.id][0], points[connectedNode.id][0]],
                         [points[node.id][1], points[connectedNode.id][1]], zorder=1, color='gray')
        for point in points:
            plt.plot(point[0], point[1], 'o', zorder=1, color='gray')
        plt.scatter([points[agentZero.id][0]], [points[agentZero.id][1]], zorder=2, color="red")
    else:
        # Retain the initial edges and update their colors
        for edge, color in edge_colors.items():
            plt.plot([points[edge[0]][0], points[edge[1]][0]], [points[edge[0]][1], points[edge[1]][1]], zorder=1, color=color)
        
        for affected in affectedInTurn[i]:
            recID = affected[1].id
            sendID = affected[0].id
            
            # Draw points for this iteration
            plt.scatter([points[recID][0]], [points[recID][1]], zorder=2, color=((numSteps-i)/numSteps, 0, 0))
            
            # Draw and update edges for this iteration
            edge_colors[(sendID, recID)] = ((numSteps-i)/numSteps, 0, 0)
            plt.plot([points[sendID][0], points[recID][0]], [points[sendID][1], points[recID][1]], zorder=2, color=edge_colors[(sendID, recID)])

# Function to assign colors to nodes
def assignNodeColors(i):
    nodeDict = defaultdict(lambda: 'gray')
    for j in range(0, i+1):
        for k in affectedInTurn[j]:
            nodeDict[k[1].id] = ((numSteps-j)/numSteps, 0, 0)  
    return nodeDict    

# Function to assign colors to edges
def assignEdgeColors(i):
    edgeDict = defaultdict(lambda: 'gray')
    for j in range(1, i+1):
        for k in affectedInTurn[j]:
            edgeDict[(k[0].id, k[1].id)] = ((numSteps-j)/numSteps, 0, 0)
    return edgeDict

def updateNx(i):
    plt.cla()
    node_color_dict = assignNodeColors(i)
    edge_color_dict = assignEdgeColors(i)
    nx.draw(G, pos, with_labels=True, node_color=[node_color_dict[node] for node in G.nodes()], edge_color=[edge_color_dict.get(edge, 'gray') for edge in G.edges()])

prodNum = int (input("How many Products do you want (1-3 products)?\nAnswer: "))
loc =0
while loc < prodNum:
    razProd = int(input("Type: \n1 to use default product \n2 to define own product \nAnswer: "))
    if razProd == 1:
        newness = 1
        price = 200
        brand_image = 1
        exclusivity = 1
        relevance = 1
        quality = 1


        print("Default Product characteristics:\n newness ==> 1 \n price ==> 200 \n brand_image ==> 1 \n exclusivity ==> 1 \n quality ==> 1")
    elif razProd ==2:
        print("Newness, Brand Image, Exckusivity, Relevance, Quality need to be set between 0.0 - 1")
        newness = float(input("Newness = "))
        price = float(input("Price = "))
        brand_image = float(input("Brand Image = "))
        exclusivity = float(input("Exclusivity = "))
        relevance = float(input("Relevance = "))
        quality = float(input("Quality = "))
    prod=Product(newness, price, brand_image, exclusivity, relevance, quality)
    Product.allProducts.append(prod)
    loc+=1


# create agents
numAgents = int(input("Number of agents: "))
coordDimensions = math.ceil(math.sqrt(numAgents)) + 1
for i in range(coordDimensions):
    for j in range(coordDimensions):
        Node.availablePoints.append([i, j])

# connect agents
for i in range(0, numAgents):
    n = Agent(i)
    Agent.allAgents.append(n)

# create network
selectedSimul = int(input('Select Network type \n 1 for Ring Lattice \n 2 for Erdos Renyi \n 3 for Watts Strogatz \n 4 for Barabasi Albert \n Answer: '))

if selectedSimul == 1:
    numConnections = int(input("Number of connections:"))
    Agent.allAgents = connectRingLattice(Agent.allAgents, numConnections)
elif selectedSimul == 2:
    probConnection = float(input("Probability of connection (0 to 1):"))
    Agent.allAgents = connectErdosRenyi(Agent.allAgents, probConnection)
elif selectedSimul == 3:
    k = int(input("Number of connections:"))
    probRewire = float(input("Probability of reconnection (0 to 1):"))
    Agent.allAgents = connectWattsStrogatz(Agent.allAgents, k, probRewire)
elif selectedSimul == 4:
    startingNum = int(input("Starting number: "))
    Agent.allAgents = connectBarabasiAlb(Agent.allAgents, startingNum)

# number of iterations of agent actions
numSteps = int(input("Number of iterations to run simulation: "))

broadcastFlag = input("Broadcasting on or off? (1 for on, 0 for off): ")
broadcastFlag = True if int(broadcastFlag) == 1 else False

nothingFlag = input("Do Nothing option on or off? (1 for on, 0 for off): ")
nothingFlag = True if int(nothingFlag) == 1 else False

# run simulation
affectedInTurn = []

# iteration 0 - first generation and share 
agentZero = random.choice(Agent.allAgents)
newContent = agentZero.generate()
affectedInTurn.append([[None, agentZero, newContent]])

# subsequent iterations
for i in range(0, numSteps+1):
    affectedInTurn.append([])
    for agentAffected in affectedInTurn[i]:
        newlyAffected = agentAffected[1].decide(newContent, broadcastFlag, nothingFlag)
        affectedInTurn[i+1].extend(newlyAffected)

# Initial edge colors dictionary
edge_colors = {}

selectedVis = int(input('Select visualization type \n 1 for Network Visualization \n 2 for Ring Visualization \n Answer: '))
if selectedVis == 1:  # nx visualization
    fig, ax = plt.subplots()
    G = nx.Graph()
    for node in Agent.allAgents:
        G.add_node(node.id)
    for node in Agent.allAgents:
        for destnode in node.connected:
            G.add_edge(node.id, destnode.id)
    pos = nx.spring_layout(G)
    ani = FuncAnimation(fig, updateNx, frames=range(0, numSteps+1), interval=1000, repeat=True)
    plt.show()
if selectedVis == 2:  # ring visualization
    fig, ax = plt.subplots()
    numNodes = len(Agent.allAgents)
    radius = len(Agent.allAgents)
    center = (0, 0)
    points = []
    for i, node in enumerate(Agent.allAgents):
        angle = (2 * i * math.pi) / numNodes
        x = center[0] + radius * 1.5 * math.cos(angle)
        y = center[1] + radius * 1.5 * math.sin(angle)
        points.append([x, y])
    ani = FuncAnimation(fig, update, frames=range(0, numSteps+1), interval=1000, repeat=True)
    plt.show()

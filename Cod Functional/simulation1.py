from agent import Agent
from Product import *
from network import *
from message import *
from collections import defaultdict
import math
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation


# Function to update the plot for each frame, where i is each iteration
def update(i):
    #print(f"Iteratie {i}: ")
    if i == 0: #iteration zero
        plt.cla()
        # Draw edges
        for node in Agent.allAgents:
            for connectedNode in node.connected:
                plt.plot([points[node.id][0], points[connectedNode.id][0]], [points[node.id][1], points[connectedNode.id][1]], zorder=1, color='gray')
        # Draw nodes
        for point in points:
            plt.plot(point[0], point[1], 'o', zorder=1, color='gray')
        # Draw agentZero     
        plt.scatter([points[agentZero.id][0]], [points[agentZero.id][1]], zorder=2, color="red")
    else:
        for affected in affectedInTurn[i]:
            #later if we want to have multiple content, we can use affected[2], different color
            recID = affected[1].id
            #print(f"recID = {recID}")    
            sendID = affected[0].id
            #print(f"sendID = {sendID}")
            
            #draw points for this iteration
            plt.scatter([points[recID][0]], [points[recID][1]], zorder=2, color=((numSteps-i)/numSteps, 0, 0)) #if we want just simple colors, do color="red"
            
            #draw edges for this iteration
            if i > 0:
                plt.plot([points[sendID][0], points[recID][0]], [points[sendID][1], points[recID][1]], zorder=2, color=((numSteps-i)/numSteps, 0, 0 )) #if we want just simple colors, do color="red"

def assignNodeColors(i):
    nodeDict = defaultdict(lambda: 'gray')
    for j in range(0, i+1):
        for k in affectedInTurn[j]:
            nodeDict[k[1].id] = ((numSteps-j)/numSteps, 0, 0) #every node k affected in turn j has this color  
    return nodeDict    
def assignEdgeColors(i):
    edgeDict = defaultdict(lambda: 'gray')
    for j in range(1, i+1):
        for k in affectedInTurn[j]:
            edgeDict[(k[0].id, k[1].id)] = ((numSteps-j)/numSteps, 0, 0) #every edge of a node k affected in turn j has this color  
            #print(f"Iteratie {i}: edge {k[0].id}, {k[1].id} added with color {(numSteps-j)/numSteps}")
    return edgeDict

def updateNx(i):
    plt.cla()
    node_color_dict=assignNodeColors(i)
    edge_color_dict=assignEdgeColors(i)
    #print(f"Iteration {i}: Edge colors: {edge_color_dict}")
    nx.draw(G, pos, with_labels=True, node_color=[node_color_dict[node] for node in G.nodes()], edge_color=[edge_color_dict[edge] for edge in G.edges()])

# create product
prodNum = int (input("How many Products do you want (1-3 products)?\nAnswer: "))
loc =0
while loc < prodNum:
     
    razProd = int(input("Type: \n1 to use default product \n2 to define own product \nAnswer: "))
    if razProd == 1:
        print("Default Product characteristics:\n newness ==> 1 \n price ==> 200 \n brand_image ==> 1 \n exclusivity ==> 1 \n quality ==> 1")
        Product(True)
    elif razProd ==2:
       Product(False)
    print(f"Product {loc+1} added.")
    loc+=1

# create agents
numAgents = int(input("Number of agents: "))

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
    Agent.allAgents = connectErdosRenyi(Agent.allAgents,probConnection)
elif selectedSimul == 3:
   k = int(input("Number of connections:"))
   probRewire = float(input("Probability of reconnection (0 to 1):"))
   Agent.allAgents = connectWattsStrogatz(Agent.allAgents,k,probRewire)
elif selectedSimul == 4:
    startingNum = int(input("Starting number: "))
    while startingNum < 2:
        print("Starting number must be greater than 1.")
        startingNum = int(input("Starting number: "))
    Agent.allAgents = connectBarabasiAlb(Agent.allAgents,startingNum)

# initialize agent properties
Agent.generateAgentData()

# initialize starting messages
i=1    
while prodNum != 0:
    mesginput = int(input("1 Default Message \n2 Custom Message \n3 Random Message \nAnswer:  "))
    if mesginput == 1:
        print("Default Message Characteristics: \nMessage Type: Advertisement \nSource: Random Any \nReading Time: 15 \nEmotional Intensity: 6 \nVisibility: 7 \nImpact on Product: 4 \nRelevance Amplifier: 3 \nRepeat Trigger: 0.3")
        Message(True)
    elif mesginput == 2:
        print(f"Add information to the message of the product {i}: ")
        Message(False)
    elif mesginput == 3:
        Message(3)     
    prodNum -= 1
    i+=1

for message in Message.allMessages:
    print(message)

# run simulation
# number of iterations of agent actions
numSteps = int(input("Number of iterations to run simulation: "))
affectedInTurn = []
affectedThisTurn = []
boughtOverTime = []
boughtThisTurn = []

# start sending messages
# iteration 0 - first generation and share 
agentsZero = [] #a list of all agents who were "starter" agents who first began sending a message at iteration 0
for message in Message.allMessages:
    affected = message.source.decideToShare(message, True)
    if affected != None:
        affectedThisTurn.append(affected)
    purchaser = message.source.decideToBuy(message)
    if purchaser != None:
        boughtThisTurn.append(purchaser)
    agentsZero.append(message.source)
affectedInTurn.append(affectedThisTurn) # everyone who received a message this iteration will be in affectedInTurn[0]

# subsequent iterations
for i in range(0, numSteps+1):
    affectedInTurn.append([]) #create a new iteration in affectedInTurn list, so that affectedInTurn[i+1] will work
    # each affectedElement from list of affectedInTurn[i] is a tuple of three things: [sender, recipient, content]
    for agentAffected in affectedInTurn[i]:
        newlyAffected = agentAffected[1].decide(newContent, broadcastFlag, nothingFlag)
        affectedInTurn[i+1].extend(newlyAffected)

selectedVis = int(input('Select visualization type \n 1 for Network Visualization \n 2 for Ring Visualization \n Answer: '))
if selectedVis == 1: #nx visualization
    fig, ax = plt.subplots()
    G = nx.Graph()
    for node in Agent.allAgents:
        G.add_node(node.id)
    for node in Agent.allAgents:
        for destnode in node.connected:
            G.add_edge(node.id, destnode.id)
    pos = nx.spring_layout(G)
    ani = FuncAnimation(fig, updateNx, frames=range(0, numSteps+1), interval=3000, repeat=True)
    plt.show()
if selectedVis == 2: #ring visualization
    # Create a new figure and axis
    fig, ax = plt.subplots()
    numNodes = len(Agent.allAgents)
    radius = len(Agent.allAgents)  # Radius of the circle
    center = (0,0)
    points = []
    # Calculate the positions of nodes in a circle
    for i, node in enumerate(Agent.allAgents):
        angle = (2 * i * math.pi) / numNodes
        x = center[0] + radius * 1.5 * math.cos(angle)
        y = center[1] + radius * 1.5 * math.sin(angle)
        points.append([x, y])
    # Create the animation
    ani = FuncAnimation(fig, update, frames=range(0, numSteps+1), interval=1000, repeat=True)
    # Show the animation
    plt.show()

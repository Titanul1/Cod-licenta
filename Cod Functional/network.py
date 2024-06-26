import random
import numpy as np
import matplotlib.pyplot as plt
import math

class Node:
    def __init__(self, id):
        self.id = id
        self.connected = []
        
def connectErdosRenyi(nodes, probConnection, bidirectional=False):
    numNodes = len(nodes)
    for i in range(numNodes):
        for j in range(numNodes):
            ran = random.uniform(0.0, 1.0)
            if ran <= probConnection and i != j:
                nodes[i].connected.append(nodes[j])
    return nodes

def connectRingLattice(nodes,numConnections):
    numNodes = len(nodes)
    if numNodes > numConnections-1:
        for i in range(numNodes):
            j = numConnections
            while j > 0:
                if j % 2 == 1:
                    toRight = math.ceil(j/2)
                    if (i+toRight) >= numNodes:
                        nodes[i].connected.append(nodes[i+toRight-numNodes])
                    else:
                        nodes[i].connected.append(nodes[i+toRight])
                else:
                    toLeft = j//2
                    toLeft = int(toLeft)
                    if (i-toLeft)<0:
                        nodes[i].connected.append(nodes[numNodes+i-toLeft])
                    else:
                        nodes[i].connected.append(nodes[i-toLeft])
                j = j -1
        return nodes
    else:
        print('Number of connections higher than number of nodes')
        quit()
    
def connectWattsStrogatz(nodes, k, probRewire):
    #start with normal ring lattice with k edges per vertex
    nodesRing = connectRingLattice(nodes, k)
    #probRewire for each edge to be rewired, the lower the number, the more insular the clusters
    for node in nodesRing:
        for connectedNode in node.connected:
            ran = random.uniform(0.0, 1.0)
            if ran < probRewire:
                nodesAvailable = [elem for elem in nodes if elem not in node.connected]
                node.connected.append(random.choice(nodesAvailable))
                node.connected.remove(connectedNode)
    return nodesRing

def connectBarabasiAlb(nodes, startingNum):
    i=0
    allConnections = 0
    nodesUsed = []
    nodesUsed.append(nodes[i])
    nodes.remove(nodes[i])
    nodesNotUsed = nodes
    i = 1
    #initialize starting cluster of nodes, everyone connected
    while i < startingNum:
        j = random.randint(0, len(nodesNotUsed)-1)
        print(f"j = {j} and length of nodesNotUsed = {len(nodesNotUsed)}")
        for node in nodesUsed:
            nodesNotUsed[j].connected.append(node)
            node.connected.append(nodes[j])    
            allConnections = allConnections + 2
        nodesUsed.append(nodes[j])
        nodesNotUsed.remove(nodes[j])
        i = i + 1
    #start adding new nodes based on preferential attachment, for now all bilateral
    while nodesNotUsed:
        oneConnection = False
        nodeToAdd = random.choice(nodesNotUsed)
        while oneConnection == False:
            for node in nodesUsed:
                prob = len(node.connected)/allConnections
                print(f'Probability of connecting {node.id} to {nodeToAdd.id} is {prob}.')
                ran = random.uniform(0.0, 1.0)
                if ran < prob:
                    node.connected.append(nodeToAdd)
                    nodeToAdd.connected.append(node)
                    allConnections = allConnections +2
                    oneConnection = True
                    break
        nodesNotUsed.remove(nodeToAdd)
        nodesUsed.append(nodeToAdd)
    return nodesUsed

#test how the connections went
def postConnections(nodes):
    for node in nodes:
        print (f"Node {node.id} is at location ({node.x}, {node.y}), connected to: ", end="")
        for j in node.connected:
            print (str(j.id) + " ", end="")
        print("\n")
        
#represent the connections graphically (x, y coordinates instead of circle graph)
def visualizeNodes(nodes):
    x_coord, y_coord = [], []
    for node in nodes:
        x_coord.append(node.x)
        y_coord.append(node.y)
        plt.text(node.x, node.y, node.id, fontsize=12, ha="right")
        for con in node.connected:
            plt.plot([node.x, con.x], [node.y, con.y], linestyle='-', marker='o', color='blue', label='line')
    plt.scatter(x_coord, y_coord, color="red", label="nodes")
    plt.title("Nodes plotted")
    plt.show()

def createCircleGraph(nodes): #visualize everything as circular
    numNodes = len(nodes)
    radius = len(nodes)  # Radius of the circle
    center = (0,0)
    points = []

    # Calculate the positions of nodes in a circle
    for i, node in enumerate(nodes):
        angle = (2 * i * math.pi) / numNodes
        x = center[0] + radius * 1.5 * math.cos(angle)
        y = center[1] + radius * 1.5 * math.sin(angle)
        points.append([x, y])

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(15, 15), dpi=90)

    # Draw edges
    for node in nodes:
        for connectedNode in node.connected:
            plt.plot([points[node.id][0], points[connectedNode.id][0]], [points[node.id][1], points[connectedNode.id][1]], 'b')
            print(f"Node {node.id} is connected to :{connectedNode.id}")

    # Draw nodes
    for point in points:
        plt.plot(point[0], point[1], 'ro')
          


    # Set axis limits
    ax.set_xlim([-radius * 2, radius * 2])
    ax.set_ylim([-radius * 2, radius * 2])

    plt.axis('equal')
    plt.show()
    return ax, points

if __name__ == "__main__":
    numNodes = int(input("Number of nodes: "))
    coordDimensions = math.ceil(math.sqrt(numNodes))+1
    for i in range(coordDimensions):
        for j in range(coordDimensions):
            Node.availablePoints.append([i, j])
    probConnection = float(input("Probability of connection (0 to 1):"))
    nodes = []
    for i in range(0, numNodes):
        n = Node(i)
        nodes.append(n)
    nodes = connectRingLattice(nodes,4)
    # connectNodes(nodes)
    #nodes = connectNodesByChance(nodes, probConnection)
    
    createCircleGraph(nodes)  # Create and display the circle graph   
    postConnections(nodes) # for debugging
    #visualizeNodes(nodes) # for visualization with distance
    

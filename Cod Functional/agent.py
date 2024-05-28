from Product import Product
from content import Content
from network import Node
import random
import numpy as np
import math
from decimal import Decimal, ROUND_DOWN

class Agent(Node):
    allAgents = []
    all_media = []
    def __init__(self, id: int):
        super().__init__(id)
        self.listContentKnown = []
        self.agentType = 'Consumer'
        self.budget = 0
        self.gender = None
        self.age = None
        self.internet_activeness = None
        self.influenceability = 0.5
        self.openness = random.randint(0, 100)
        self.suspicion = math.floor(random.uniform(0.0, 1.0)*100)/100.0
        self.public_share_ratio = math.floor(random.uniform(0, 0.8)*100)/100.0
        self.attention_span = random.randint(1, 30)
        self.relevant_to_me = []
        self.product_impression = []
        self.source_impression = []  
        self.known_messages = []
        self.bought = []
    def decide(self, content: Content, broadcastOn=True, nothingOn=True):
        # decide what to do based on content and agent rules + properties
        # for now, spread at probability virality
        whoAffected = [] #automatically updated by reaction functions, each element has format [sender, recipient, content]
        if (random.uniform(0.0, 1.0) < content.virality):
            #based on passing a threshold virality, agent decides to do "something"
            if broadcastOn == False:
                m = 2
            else:
                m = 1
            if nothingOn == False:
                n = 2
            else:
                n = 3
            reactionSeed = random.randint(m, n) #for testing purposes can do 2, 2. change back to 1, 3 later.
            if (reactionSeed == 1):
                self.broadcastContent(content, whoAffected)
                #print(f"{self.id} broadcasted to: ", end = " ")
            elif (reactionSeed == 2):
                self.shareFew(content, whoAffected)
                #print(f"{self.id} shared with close friends!", end = " ")
            else:
                pass
        '''
        for a in whoAffected:
            print(a[1].id, end=" ")
        print("")
        '''
        return whoAffected
        
    def broadcastContent(self, content, whoAffected):
        for friend in self.connected:
            updateFlag = friend.updateInfo(content)
            if updateFlag:
                whoAffected.append([self, friend, content])
    
    def shareFew(self, content, whoAffected):
        # for now, just random probability, but later, will add proximity/affinity type variables
        p = 0.3
        for friend in self.connected:
            if random.uniform(0.0, 1.0) < p:
              updateFlag = friend.updateInfo(content)
              if updateFlag:  # maybe later create repetition effects
                    whoAffected.append([self, friend, content])
    
    def updateInfo(self, content):
        #checks if info is already known before appending
        if content in self.listContentKnown:
            return False
        else:
            self.listContentKnown.append(content)
            return True
    
    def generate(self):
        # decide what or if to generate content based on agent rules + properties
        content = Content(self, random.uniform(0.0, 1.0))
        self.listContentKnown.append(content)
        return content
    def generate_age(self):
        asym =0
        meanAge = 50
        std = 10
        scale = 15
        while asym < 18 or asym > 90:
            normalPart = np.random.normal(meanAge, std)
            expPart = np.random.exponential(scale)
            asym = int(normalPart + expPart)
        return asym
    
    @staticmethod
    def generateAgentData():
        # generate media accounts
        try:
            mediaP = float(input("What percent of accounts are media accounts? (from 0 to 1, default 0.10) "))
        except ValueError:
            print("Value is not valid. Setting value at 0.10.")
            mediaP = 0.1
        # no recasting in Python... can't make child of "Agent"... instead make type a variable and have different methods depending on type
        Agent.allAgents.sort(key=lambda agent: len(agent.connected))
        for i in range(0, math.floor(len(Agent.allAgents)*mediaP)):
            Agent.allAgents[i].agentType = 'Media'
        # generate average settings
        try: 
            agedist = int(input("What kind of age distribution does this population have? (will generate ages 18 to 90) \n1. Mostly younger. \n2. Mostly older. \n3. Uniform.\n"))
        except ValueError:
            print("Value is not valid. Setting distribution to be uniform.")
            agedist = 3
        try:
            budgetmin = int(input("Define the minimum possible value in the budget range of consumers. "))
            budgetmax = int(input("Define the maximum possible value in the budget range of consumers. "))
            if budgetmin < 0:
                print("Minimum value can't be negative. Set at 0.")
                budgetmin = 0
        except ValueError:
            print("Value is not valid. Setting minimum value at 0, maximum value at 500.")
            budgetmin = 0
            budgetmax = 500
        try:
            mean_internet = float(input("How many hours does this population spend on the Internet on average? "))
        except ValueError:
            print("Invalid number. Setting average number of hours on Internet as 3.")
            mean_internet = 3
        try:
            std_internet = float(input("Standard deviation for number of hours on the Internet: "))
        except ValueError:
            print("Invalid number. Setting standard deviation for number of hours on the Internet as 2.")
            std_internet = 2
        try:
            print("Generally, in this setting, how much do others' opinions matter when compared to one's own? ")
            infmean = float(input("0.5 is 50% weight. Higher numbers mean that group opinion matters more. (select 0 to 1) "))
            if (infmean < 0 or infmean > 1):
                print("This number is out of range. Setting influenceability score mean to default (0.5).")
                infmean = 0.5  
        except ValueError:
            print("This isn't a valid number. Setting influenceability score mean to default (0.5).")
            infmean = 0.5
        # generating each agent's values based on the parameters (some that do not depend on parameters already set in __init__)
        for agent in Agent.allAgents:
            if agent.agentType == 'Consumer':
                #generate budget
                agent.budget = random.randint(budgetmin, budgetmax)
                ran = random.randint(1, 10)
                #generate gender
                if (ran > 5):
                    agent.gender = 'F'
                else:
                    agent.gender = 'M'
                #generate age
                if agedist == '1':
                    a = int(np.random.exponential(72)) # generates from 0 to roughly 72
                    while (a > 72):
                        a = int(np.random.exponential(72))
                    agent.age = a +18
                if agedist == '2':
                    agent.age = Agent.generate_age()
                else:
                    agent.age = int(random.uniform(18, 90))
                # generate internet 
                while (agent.internet_activeness == None or agent.internet_activeness < 0 or agent.internet_activeness > 24):
                    hr = math.floor(np.random.normal(mean_internet, std_internet))
                    agent.internet_activeness = hr
            #beginning of variables used by both Consumers and Media
            #influenceability
            while True:
                infl = np.random.normal(infmean, 0.2)
                if infl > 0 and infl < 1:
                    #sometimes gives floating point arithmetic problems like 56.99999... tried using Decimal
                    agent.influenceability = Decimal(infl).quantize(Decimal('1.00'), rounding=ROUND_DOWN)
                    break
            #randomized levels of interest in product, based on product relevance score
            for p in Product.allProducts:
                mean = p.relevance
                std = 0.3
                agent.relevant_to_me.append([p, math.floor(np.random.normal(mean, std)*100)/100.0])
            #randomized starting impression of each source
            for s in agent.connected:
                while True:
                    opinion = math.floor(np.random.normal(0, 1)*100)/100
                    if (opinion > -1 and opinion < 1):
                        break
                agent.source_impression.append([s, opinion])

        for i in Agent.allAgents:
            print(f"{i.id} este de tipul {i.agentType}, are {i.budget} bani, este {i.gender}, si are {i.age} ani.")
            print(f"Petrece {i.internet_activeness} ore pe Internet.")
            print(f"Este influentat de alti cu {int(i.influenceability * 100)}%.")
            print(f"Este deschis sa adopteze produse noi cu {i.openness}.")
            print(f"Este suspicios de {i.suspicion*100}% de timp.")
            print(f"Face sharing de {i.public_share_ratio*100}%.")
            print(f"Este de obicei atent pentru {i.attention_span} secunde.")
            print(f"Are urmatoarele niveluri de interes despre produse: ")
            for prod in i.relevant_to_me:
                print(f"Product {prod[0].prodID} = {prod[1]}")
            print(f"Are urmatoarele impresii despre surse cunoscute: ")
            for sursa in i.source_impression:
                print(f"Sursa {sursa[0].id} = {sursa[1]}")
                


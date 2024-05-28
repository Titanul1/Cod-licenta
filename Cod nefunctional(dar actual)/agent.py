from Product import Product
from message import Message
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
        self.agentType = 'Consumer'
        self.budget = 0
        self.gender = None
        self.age = None
        self.internet_activeness = None
        self.influenceability = 0.5
        self.openness = random.randint(0, 100) # % of newness that needs to be passed to adopt the product
        self.suspicion = math.floor(random.uniform(0.0, 1.0)*100)/100. # % reduction of trust due to suspicion
        self.public_share_ratio = math.floor(random.uniform(0, 0.8)*100)/100.
        self.attention_span = random.randint(1, 30)
        self.relevant_to_me = []
        self.product_impression = []
        self.source_impression = []  
        self.known_messages = []
        self.bought = []

    def payAttention(self, message): # will agent pay attention to the message or forget about it right away?
        prod = message.about_product
        for prodData in self.relevant_to_me:
            if prodData[0] == prod:
                relevance_product = prodData[1]
        tldr_modifier = 1
        if self.attention_span < message.reading_time:
            tldr_modifier = self.attention_span/message.reading_time
        message_interest_modifier = 1+(message.relevance_amplifier-5)/10.
        emotional_intensity_modifier = 1+(message.emotional_intensity-5)/10.
        # baseline personal relevance of product * message interest modifier * emotional intensity modifier * attention span modifier
        percentAttentive = relevance_product *message_interest_modifier*emotional_intensity_modifier*tldr_modifier
        if percentAttentive >= 1:
            percentAttentive = 1
        if (percentAttentive * 100) > random.randint(0, 100):
            return True
        else:
            return False

    def trustSource(self, message):
        src = message.source
        # check if agent knows source (even if not directly connected)
        found = False
        for s in self.source_impressions:
            if s[0] == src:
                found = True
                agent_trust = s[1]
        if found == False:
            #random first impression of new source * suspicion modifier
            agent_trust = random.randint(0, 100)/100. * (1- self.suspicion)
            self.source_impressions.append([src, agent_trust])
        sum = 0
        n = 0
        # check how friends feel * influenceability modifier
        for agent in self.connected:
            for s in agent.source_impressions:
                if s[0] == src:
                    sum += s[1]
                    n += 1
        others_trust = sum / n
        influenceability_modifier = self.influenceability-0.5
        others_impact = others_trust * influenceability_modifier
        # mai e de facut...

        # impact_on_product * others_impact, agent_trust 


    def updateProductImpression(self, message):
        for mesg in self.known_messages:
            if mesg[0].about_product == message.about_product:
                pass
        for prodData in self.product_impression:
            if prodData[0] == message.about_product:
                current_impression = prodData[1]
                self.product_impression.prodData = [message.about_product, imp]

    def decideRelevance(self, message):
        prod = message.about_product
        # is it too new to be interesting?
        if prod.newness * 100 < self.openness:
            multiplier = 1 - (self.openness/100. - prod.newness) # % lowered interest when the product is too new compared to agent's openness
        # does it give a social status bonus that makes it more interesting?
        multiplier *= 1+(prod.brand_image-0.5) # % modified depending on whether brand has a positive or negative image compared to 0.5 mean
        multiplier *= 1+(prod.visibility - 0.5) # % modified depending on whether buying the product is visible and a social bonus
        multiplier *= 1+(prod.exclusivity - 0.5) # % modified depending on whether product seems exclusive... Some brand names seems exclusive, even if everyone has them
        # what does agent remember from previous messages?
        #for self.product_impression
        
        # do friends seem to like it? (weigh this based on influenceability)

        # modify current relevant_to_me with the modifiers
        self.relevant_to_me *= multiplier
    
    def decideToShare(self, message, author):
        if author == True:
            self.known_messages.append(message, [self], 1)  # message, source, trust score
            self.updateProductImpression(message)
            if self.agentType == 'Media':
                return self.broadcastMessage(message)
            elif self.public_share_ratio*100 < random.randint(0, 100):
                return self.broadcastMessage(message)
            else: 
                return self.shareFew(message)
        else:
            if self.payAttention(message):
                trust_score = self.trustSource(message)
                self.known_messages.append([message, message.source, trust_score])
                
                #else do nothing

            # else agent doesn't pay attention
            # known messages and product impression not updated... forgets about it

        # decide what to do based on content and agent rules + properties
        # for now, spread at probability virality
    
    def decideToBuy(self, message):
        if self.agentType == 'Media':
            return None
        else:
            if self.budget > message.about_product.price:
                return None
            for elem in self.relevance_to_me:
                if elem[0] == message.about_product:
                    elem = [message.about_product, self.decideRelevance(message)]
        
    '''
    def altdecide(self, content: Content, broadcastOn=True, nothingOn=True):
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
        
        for a in whoAffected:
            print(a[1].id, end=" ")
        print("")
        return whoAffected
    '''

    def broadcastMessage(self,message):
        whoAffected = []
        for friend in self.connected:
            whoAffected.append([message, friend, self])
        return whoAffected
    
    @staticmethod
    def pickOnlyProduct(connected_agent, product_of_interest):
        for prod, relevance in connected_agent.relevant_to_me:
            if prod == product_of_interest:
                return relevance

    def shareFew(self, message):
        whoAffected = []
        baseline = 5 # how many to share (based on 5 close friends - Dunbar)
        numPeople = baseline * self.public_share_ratio*(1 + (self.internet_activeness - 5)*.1) *(1 + (self.relevant_to_me - 5)*.1)
        if self.gender == 'F':  # women share 60% more than men
            numPeople *= 1.6
        numPeople = int(numPeople)
        numShared = 0 
        uninformed = sorted(self.connected, key=lambda elem : Agent.pickOnlyProduct(elem, message.about_product)) #sorting friends based on how interested they are in message's product
        while numShared < numPeople or numShared < len(self.connected):
            if random.randint(0, 1) == 0:
                agentSelected = random.choice(uninformed)
                whoAffected.append([message, agentSelected, self])
                uninformed.remove(agentSelected)
                numShared += 1
            else:
                agentSelected = uninformed[0]
                whoAffected.append([message, agentSelected, self])
                uninformed.remove(agentSelected)
                numShared += 1
        return whoAffected
    
    '''
    def generate(self):
        # decide what or if to generate messages based on agent rules + properties
        message = Message(self, random.uniform(0.0, 1.0))
        self.known_messages.append([message, [self], 1])
        return message
    '''

    @staticmethod
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
            Agent.all_media.append(Agent.allAgents[i])
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
                agent.relevant_to_me.append([p, math.floor(np.random.normal(mean, std)*100)/100.])
            #randomized starting impression of each connected source
            for s in agent.connected:
                while True:
                    opinion = math.floor(np.random.normal(0, 1)*100)/100
                    if (opinion > -1 and opinion < 1):
                        break
                agent.source_impression.append([s, opinion])
        Agent.all_media.sort(key=lambda agent: len(agent.connected))
        Agent.allAgents.sort(key=lambda agent: len(agent.connected))
        for i in Agent.allAgents:
            print(f"{i.id} este de tipul {i.agentType}, are {i.budget} bani, este {i.gender}, si are {i.age} ani.")
            print(f"Petrece {i.internet_activeness} ore pe Internet.")
            print(f"Este influentat de alti cu {int(i.influenceability * 100)}%.")
            print(f"Este deschis sa adopteze produse noi cu {i.openness}.")
            print(f"Suspiciunea lui scade din impresie {i.suspicion*100}%.")
            print(f"Face sharing de {i.public_share_ratio*100}%.")
            print(f"Este de obicei atent pentru {i.attention_span} secunde.")
            print(f"Are urmatoarele niveluri de interes despre produse: ")
            for prod in i.relevant_to_me:
                print(f"Product {prod[0].prodID} = {prod[1]}")
            print(f"Are urmatoarele impresii despre surse cunoscute: ")
            for sursa in i.source_impression:
                print(f"Sursa {sursa[0].id} = {sursa[1]}")
                


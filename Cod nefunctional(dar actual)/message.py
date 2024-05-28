from agent import Agent 
import random
import numpy as np
from Product import Product
class Message:
    allMessages = []
    errormessage = "Value entered is not valid."

    def __init__(self, default=True):
         
        if default == True:
            self.id = Message.generateUniqueID(self)
            self.message_type = 1
            self.about_product = Product.allProducts[0]
            self.source = Message.choose_source('1')
            self.reading_time = 15
            self.emotional_intensity = 6
            self.visibility = 7
            self.impact_on_product = 4
            self.relevance_amplifier = 3
            self.repeat_trigger = 0.3
            Message.allMessages.append(self)
        
        elif default == False:    
            self.id = Message.generateUniqueID(self)
            try:
                pid = int(input("About which product is the message (enter ID)? " ))
                found = False
                for prod in Product.allProducts:
                    if prod.prodID == pid:
                        self.about_product = prod
                        found = True
                        break
                if found == False:
                   raise ValueError      
            except ValueError:
                print("This product ID does not exist. Randomly assigning a product.")
                self.about_product = random.choice(Product.allProducts)             
            print("Message Type: 1 = Advertisement, 2 = Review, 3 = Mention ")
            self.message_type = input("Message Type: ")
            self.source = Message.choose_source(0)
            self.reading_time = input("Reading Time (in seconds): ")
            print("From 1 to 10, rate the following:")
            self.emotional_intensity = input("Emotional Intensity: ")
            self.visibility = input("Visibility: ")
            self.impact_on_product = input("Impact on Product (5 is neutral about product): ")
            self.relevance_amplifier = input("Relevance Amplifier: ")
            print("From 0 to 1, rate the following:")
            self.repeat_trigger = input("Repeat Trigger: ")
            Message.allMessages.append(self)
        else:
            self.id = Message.generateUniqueID(self)
            self.about_product = random.choice(Product.allProducts)
            self.message_type = random.randint(1,3)
            source = random.randint(1,3)
            self.source = Message.choose_source(str(source))
            self.reading_time = 0
            while (self.reading_time <= 0):
                self.reading_time = np.random.normal(120, 60)
            self.emotional_intensity = random.randint(1,10)
            self.visibility = random.randint(1,10)
            self.impact_on_product = random.randint(1,10)
            self.relevance_amplifier = random.randint(1,10)
            self.repeat_trigger = random.randint(0,10)/10.
            Message.allMessages.append(self)

    @staticmethod
    def choose_source(choice):
        try:
            if choice == 0:
                choice = input("Source: \n1 = Random Any \n2 = Random Media \n3 = Most Connected Media \nAnswer: ")
        except ValueError:
            choice = -1    
        while choice != '1' and choice != '2' and choice != '3':
            print("Invalid choice. Please choose a valid source.")
            choice = input("1 = Random Any \n2 = Random Media \n3 = Most Connected Media \nAnswer: ")
        if choice == '1':
            agent = Agent.allAgents[random.randint(0, len(Agent.allAgents)-1)]
            return agent
        elif choice == '2':
            if len(Agent.all_media) == 0:
                print("No media accounts available choosing random consumer as source.")
                return Agent.allAgents[random.randint(0, len(Agent.allAgents)-1)] 
            else:
                agent = Agent.all_media[random.randint(0, len(Agent.all_media)-1)]
            return agent
        elif choice == '3':
            if len(Agent.all_media) == 0:
                print("No media accounts available choosing the most connected consumer as source.")
                return Agent.allAgents[0]
            else:
                agent = Agent.all_media[0]
            return agent
    
    @property
    def message_type(self):
        return self._message_type
    
    @message_type.setter
    def message_type(self, value):
        while (True):
            try:
                n = int(value)
                if n == 1:
                    self._message_type = "Advertisement"
                    break
                elif n == 2:
                    self._message_type = "Review"
                    break
                elif n == 3:
                    self._message_type = "Mention"
                    break
                value = input("Message Type = ")
            except ValueError:
                print(f"{Message.errormessage}")
                value = input("Message Type = ")


    @property
    def reading_time(self):
        return self._reading_time
    
    @reading_time.setter
    def reading_time(self, value):
        while (True):
            try:
                n = int(value)
                if n >=0:
                    self._reading_time = n
                    break
                value = input("Reading Time = ")
            except ValueError:
                print(f"{Message.errormessage}")
                value = input("Reading Time = ")


    @property
    def emotional_intensity(self):
        return self._emotional_intensity
    
    @emotional_intensity.setter
    def emotional_intensity(self, value):
        while (True):
            try:
                n = int(value)
                if n >=1 and n <= 10:
                    self._emotional_intensity = n
                    break
                value = input("Emotional Intensity = ")
            except ValueError:
                print(f"{Message.errormessage}")
                value = input("Emotional Intensity = ")

    @property
    def visibility(self):
        return self._visibility
    
    @visibility.setter
    def visibility(self, value):
        while (True):
            try:
                n = int(value)
                if n >=1 and n <= 10:
                    self._visibility = n
                    break
                value = input("Visibility = ")
            except ValueError:
                print(f"{Message.errormessage}")
                value = input("Visibility = ")

    @property
    def impact_on_product(self):
        return self._impact_on_product
    
    @impact_on_product.setter
    def impact_on_product(self, value):
        while (True):
            try:
                n = int(value)
                if n >=1 and n <= 10:
                    self._impact_on_product = n
                    break
                value = input("Impact on Product = ")
            except ValueError:
                print(f"{Message.errormessage}")
                value = input("Impact on Product = ")

    @property
    def relevance_amplifier(self):
        return self._relevance_amplifier

    @relevance_amplifier.setter
    def relevance_amplifier(self, value):
        while (True):
            try:
                n = int(value)
                if n >=1 and n <= 10:
                    self._relevance_amplifier = n
                    break
                value = input("Relevance Amplifier = ")
            except ValueError:
                print(f"{Message.errormessage}")
                value = input("Relevance Amplifier = ")

    @property
    def repeat_trigger(self):
        return self._repeat_trigger
    
    @repeat_trigger.setter
    def repeat_trigger(self, value):
        while (True):
            try:
                n = float(value)
                if n >=0 and n <= 1:
                    self._repeat_trigger = n
                    break
                value = input("Repeat Trigger = ")
            except ValueError:
                print(f"{Message.errormessage}")
                value = input("Repeat Trigger = ")

    def __str__(self):
        return f"\nMessage Type: {self.message_type}\nSource:{self.source.id} \nReading Time: {self.reading_time}\nEmotional Intensity: {self.emotional_intensity}\nVisibility: {self.visibility}\nImpact on Product: {self.impact_on_product}\nRelevance Amplifier: {self.relevance_amplifier}\nRepeat Trigger: {self.repeat_trigger}"

    def generateUniqueID(self):
        checkid = 0
        while True:
            found = False
            for item in Message.allMessages:
                if item.id == checkid:
                    found = True
                    checkid+=1
                    break
            if found == False:
                return checkid

if __name__ == "__main__":
    messages = []
    for i in range(10):
        messages.append(Message(i))
    print("All Messages")
    for con in messages:
        print(con.id)


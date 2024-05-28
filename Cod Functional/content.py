# Define what content is generated and/or consumed inside the network

class Content:
    allContent = []
    # maybe a factor of "correlated" content? 
    # e.g., if I believe COVID is fake, maybe I'm also the type to believe vaccines are a conspiracy
    def __init__(self, agent, virality):
        self.id = Content.generateUniqueID(self)
        self.virality = 1 # virality #for testing purposes put at 1
        Content.allContent.append(self)
        self.author = agent
        Content.allContent.append(self)
        
    '''What other variables would be interesting to include?
            tipul de informatie - stiri, reclama, recenzie
            tip de produs
            audienta tinta
            data si ora trimiterii
            price range
    '''
    def generateUniqueID(self):
        checkid = 0
        while True:
            found = False
            for item in Content.allContent:
                if item.id == checkid:
                    found = True
                    checkid+=1
                    break
            if found == False:
                return checkid
            
if __name__ == "__main__":
    contents = []
    for i in range(10):
        contents.append(Content(1))
    print("All Contents")
    for con in contents:
        print(con.id)
    
class Product:
    allProducts = []
    prodCount = -1
    errormessage = "Value entered is not valid."
    def __init__(self, default=True):
        if default == True:
            self.newness = 1
            self.visibility = 1
            self.price = 200
            self.brand_image = 1
            self.exclusivity = 1
            self.relevance = 1
            self.quality = 1
            
        else:
            print("Newness, Visibility, Brand Image, Exckusivity, Relevance, Quality need to be set between 0.0 - 1")
            self.newness = input("Newness = ")
            self.visibility = input("Visibility = ")
            self.price = input("Price = ")
            self.brand_image = input("Brand Image = ")
            self.exclusivity = input("Exclusivity = ")
            self.relevance = input("Relevance = ")
            self.quality = input("Quality = ")
        Product.prodCount += 1
        self.prodID = Product.prodCount
        Product.allProducts.append(self)
        print(self)
    
    @property
    def newness(self):
        return self._newness

    @newness.setter
    def newness(self, value):
        while (True):
            try:
                n = float(value)
                if n >=0 and n <= 1:
                    self._newness = n
                    break
                value = input("Newness = ")
            except ValueError:
                print(f"{Product.errormessage}")
                value = input("Newness = ")
    
    @property
    def visibility(self):
        return self._visibility
    
    @visibility.setter
    def visibility(self, value):
        while (True):
            try:
                n = float(value)
                if n >=0 and n <= 1:
                    self._visibility = n
                    break
                value = input("Visibility = ")
            except ValueError:
                print(f"{Product.errormessage}")
                value = input("Visibility = ")

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        while (True):
            try:
                n = float(value)
                if n >0:
                    self._price = n
                    break
                value = input("Price = ")
            except ValueError:
                print(f"{Product.errormessage}")
                value = input("Price = ")

    @property
    def brand_image(self):
        return self._brand_image
    
    @brand_image.setter
    def brand_image(self, value):
        while (True):
            try:
                n = float(value)
                if n >=0 and n <= 1:
                    self._brand_image = n
                    break
                value = input("Brand Image = ")
            except ValueError:
                print(f"{Product.errormessage}")
                value = input("Brand Image = ")
    
    @property
    def exclusivity(self):
        return self._exclusivity
    
    @exclusivity.setter
    def exclusivity(self, value):
        while (True):
            try:
                n = float(value)
                if n >=0 and n <= 1:
                    self._exclusivity = n
                    break
                value = input("Exclusivity = ")
            except ValueError:
                print(f"{Product.errormessage}")
                value = input("Exclusivity = ")
    @property
    def relevance(self):
        return self._relevance
    
    @relevance.setter
    def relevance(self, value):
        while (True):
            try:
                n = float(value)
                if n >=0 and n <= 1:
                    self._relevance = n
                    break
                value = input("Relevance = ")
            except ValueError:
                print(f"{Product.errormessage}")
                value = input("Relevance = ")
    
    @property
    def quality(self):
        return self._quality
    
    @quality.setter
    def quality(self, value):
        while (True):
            try:
                n = float(value)
                if n >=0 and n <= 1:
                    self._quality = n
                    break
                value = input("Quality = ")
            except ValueError:
                print(f"{Product.errormessage}")
                value = input("Quality = ")

                
    def alt__init__(self, newness, price, brand_image, exclusivity, relevance, quality):
        self.newness = newness
        self.price = price
        self.brand_image = brand_image
        self.exclusivity = exclusivity
        self.relevance = relevance
        self.quality = quality

    def __str__(self):
        return(f"N = {self.newness}\nV={self.visibility}\nP = {self.price}\nBi = {self.brand_image}\nEx = {self.exclusivity}\nRe = {self.relevance}\nQu = {self.quality}")
from domain.Pizza import Pizza

class PizzaBuilder:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.pizza = Pizza()
    
    def set_thin_dough(self):
        self.pizza.dough = "тонком"
        return self
    
    def set_thick_dough(self):
        self.pizza.dough = "толстом"
        return self
    
    def add_sauce(self, sauce="томатным соусом"):
        self.pizza.sauce = sauce
        return self
    
    def add_cheese(self):
        self.pizza.toppings.append("сыром")
        return self
    
    def add_bacon(self):
        self.pizza.toppings.append("беконом")
        return self
    
    def add_mushrooms(self):
        self.pizza.toppings.append("грибами")
        return self
    
    def add_pepperoni(self):
        self.pizza.toppings.append("пепперони")
        return self
    
    def add_olives(self):
        self.pizza.toppings.append("оливками")
        return self
    
    def build(self):
        pizza = self.pizza
        self.reset()
        return pizza
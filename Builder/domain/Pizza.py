class Pizza:
    def __init__(self, name="Кастомная пицца", dough="", sauce="", toppings=None):
        self.name = name
        self.dough = dough
        self.sauce = sauce
        if toppings:
            self.toppings = toppings  
        else:
            self.toppings = []

    def __str__(self):
        if not self.dough:
            dough_desc = ""
        else:
            dough_desc = f"на {self.dough} тесте"
        if self.toppings:
            toppings_desc = ", ".join(self.toppings)  
        else:
            toppings_desc = ""
        if self.sauce:
            sauce_desc = f" с {self.sauce}" 
        else:
            sauce_desc = ""
        if toppings_desc:
            return f"Пицца '{self.name}' {dough_desc}{sauce_desc} с {toppings_desc}."
        else:
            return f"Пицца '{self.name}' {dough_desc}{sauce_desc}."
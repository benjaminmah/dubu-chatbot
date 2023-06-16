class Ingredients:
    def __init__(self):
        self.ingredients = []
        self.string_ingredients = ""

    def add_ingredients(self, ingredients):
        for i in range(len(ingredients)):
            if "Professional" in ingredients[i]:
                self.ingredients.append("act professional")
            elif "Casual" in ingredients[i]:
                self.ingredients.append("act like a hippie and use tons of slang")
            elif "Bold" in ingredients[i]:
                self.ingredients.append("act aggressive")
            elif "Wholesome" in ingredients[i]:
                self.ingredients.append("act sweet and caring")
            elif "Playful" in ingredients[i]:
                self.ingredients.append("act jokey and make tons of jokes")

    def create_string(self):
        if len(self.ingredients) == 1:
            self.string_ingredients += f" {self.ingredients[0]}."
        else:
            for i in range(len(self.ingredients)):
                if i == (len(self.ingredients) - 1):
                    self.string_ingredients += f" and {self.ingredients[i]}."
                else:
                    self.string_ingredients += f" {self.ingredients[i]},"
    
    def reset_ingredients(self):
        self.ingredients = []
        self.string_ingredients = ""

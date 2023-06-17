class Ingredients:
    def __init__(self):
        self.ingredients = []
        self.string_ingredients = ""

    def add_ingredients(self, ingredients):
        for i in range(len(ingredients)):
            if "Professional" in ingredients[i]:
                self.ingredients.append("acting professional/fancy and use a very complex vocabulary")
            elif "Casual" in ingredients[i]:
                self.ingredients.append("acting like a hippie and using tons of slang like a stoner")
            elif "Hotheaded" in ingredients[i]:
                self.ingredients.append("acting impatient and rude")
            elif "Wholesome" in ingredients[i]:
                self.ingredients.append("acting wholesome and use emojis in every single sentence")
            elif "Playful" in ingredients[i]:
                self.ingredients.append("acting childish, making jokes every sentence, and use a lot of sarcasm")

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

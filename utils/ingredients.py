class Ingredients:
    def __init__(self):
        self.ingredients = []
        self.string_ingredients = ""

    def add_ingredients(self, ingredients):
        for i in range(len(ingredients)):
            if "Professional" in ingredients[i]:
                self.ingredients.append("acting professional and use a sophisticated vocabulary")
            elif "Casual" in ingredients[i]:
                self.ingredients.append("using slang like a surfer, hippie, or a stoner")
            elif "Passionate" in ingredients[i]:
                self.ingredients.append("acting super enthusiastic and using exclamation marks after every single sentence")
            elif "Wholesome" in ingredients[i]:
                self.ingredients.append("including a wide variety of emojis in every single sentence to describe what you are saying")
            elif "Playful" in ingredients[i]:
                self.ingredients.append("acting like a jokster making jokes every sentence")
            elif "Lyricist" in ingredients[i]:
                self.ingredients.append("acting like a rapper where sentences should rhyme")
            elif "Hulk" in ingredients[i]:
                self.ingredients.append("acting like Hulk with caveman vocabulary")
            elif "Robot" in ingredients[i]:
                self.ingredients.append("acting like a robot called Dubu-3000 and include onomatopoeias")

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

"""
Here we assume that 'Drink' and 'Cocktail' are different things and should
not be treated together like if they were the same thing.
"""


class Drink:
    def mix(self, fluid_one, fluid_two):
        return fluid_one + fluid_two


class Cocktail:
    def mix(self, fluid_one, fluid_two, alcoholic_fluid):
        return fluid_one + fluid_two + alcoholic_fluid


"""
Here we assume that drink and cocktail are the same thing and should actually
inherit from each over. We also assume that any Cocktail can be treated like
a Drink (if you add beer to it).
"""


class Drink:
    def mix(self, fluid_one, fluid_two):
        return fluid_one + fluid_two


class Cocktail(Drink):
    def mix(self, fluid_one, fluid_two, alcoholic_fluid="Beer"):
        return fluid_one + fluid_two + alcoholic_fluid
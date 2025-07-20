# ======= Interfaces and Base Classes =======
from abc import ABC, abstractmethod

# Base Pizza Interface
class Pizza(ABC):
    @abstractmethod
    def prepare(self):
        pass

    @abstractmethod
    def bake(self):
        pass

    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def get_cost(self):
        pass

# ======= Concrete Base Pizzas =======
class Margherita(Pizza):
    def prepare(self):
        print("Preparing Margherita pizza")

    def bake(self):
        print("Baking Margherita pizza")

    def get_description(self):
        return "Margherita"

    def get_cost(self):
        return 200

class Farmhouse(Pizza):
    def prepare(self):
        print("Preparing Farmhouse pizza")

    def bake(self):
        print("Baking Farmhouse pizza")

    def get_description(self):
        return "Farmhouse"

    def get_cost(self):
        return 250

# ======= NY and Chicago Variants =======
class NYMargherita(Margherita):
    def get_description(self):
        return "New York Margherita"

class NYFarmhouse(Farmhouse):
    def get_description(self):
        return "New York Farmhouse"

class ChicagoMargherita(Margherita):
    def get_description(self):
        return "Chicago Margherita"

class ChicagoFarmhouse(Farmhouse):
    def get_description(self):
        return "Chicago Farmhouse"

# ======= Abstract Factory Pattern =======
class AbstractPizzaFactory(ABC):
    @abstractmethod
    def get_pizza(self, pizza_type: str) -> Pizza:
        pass

class NewYorkFactory(AbstractPizzaFactory):
    def get_pizza(self, pizza_type: str):
        if pizza_type.lower() == "margherita":
            return NYMargherita()
        elif pizza_type.lower() == "farmhouse":
            return NYFarmhouse()
        return None

class ChicagoFactory(AbstractPizzaFactory):
    def get_pizza(self, pizza_type: str):
        if pizza_type.lower() == "margherita":
            return ChicagoMargherita()
        elif pizza_type.lower() == "farmhouse":
            return ChicagoFarmhouse()
        return None

# ======= Decorators for Toppings, Size =======
class PizzaDecorator(Pizza):
    def __init__(self, pizza: Pizza):
        self._pizza = pizza

class Cheese(PizzaDecorator):
    def prepare(self):
        self._pizza.prepare()
        print("Adding Cheese")

    def bake(self):
        self._pizza.bake()

    def get_description(self):
        return self._pizza.get_description() + ", Cheese"

    def get_cost(self):
        return self._pizza.get_cost() + 50

class Jalapenos(PizzaDecorator):
    def prepare(self):
        self._pizza.prepare()
        print("Adding Jalapenos")

    def bake(self):
        self._pizza.bake()

    def get_description(self):
        return self._pizza.get_description() + ", Jalapenos"

    def get_cost(self):
        return self._pizza.get_cost() + 40

class Olives(PizzaDecorator):
    def prepare(self):
        self._pizza.prepare()
        print("Adding Olives")

    def bake(self):
        self._pizza.bake()

    def get_description(self):
        return self._pizza.get_description() + ", Olives"

    def get_cost(self):
        return self._pizza.get_cost() + 30

# ======= Size Decorator =======
class Size(PizzaDecorator):
    def __init__(self, pizza: Pizza, size: str):
        super().__init__(pizza)
        self._size = size.lower()

    def prepare(self):
        self._pizza.prepare()

    def bake(self):
        self._pizza.bake()

    def get_description(self):
        return self._pizza.get_description() + f" ({self._size.title()})"

    def get_cost(self):
        size_cost = {"small": 0, "medium": 50, "large": 100}
        return self._pizza.get_cost() + size_cost.get(self._size, 0)

# ======= Sample Driver =======
if __name__ == "__main__":
    factory = NewYorkFactory()
    pizza = factory.get_pizza("Farmhouse")
    pizza = Size(pizza, "Large")
    pizza = Cheese(pizza)
    pizza = Jalapenos(pizza)

    pizza.prepare()
    pizza.bake()
    print("\nOrder Summary:")
    print("Description:", pizza.get_description())
    print("Total Cost:", pizza.get_cost())

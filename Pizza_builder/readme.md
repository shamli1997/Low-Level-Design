# 🍕 Pizza Factory System (LLD in Python)

A modular, extensible Pizza Factory system implemented in Python. Supports creation of various pizza types (Margherita, Farmhouse) across different regional styles (New York, Chicago) with clear separation of concerns using Factory Design Pattern. Includes preparation and baking steps, with optional toppings, size selection, and dynamic pricing using the Decorator Pattern.

---

## 🫠 Problem Statement
Design a pizza-making system that supports:
- Multiple pizza types: Margherita, Farmhouse
- Multiple styles: New York, Chicago
- Factory creation pattern
- Add support for crusts, toppings, sizes, sauces, and payment
- Use Decorator Pattern for dynamic topping and size addition

---

## ✅ Functional Requirements
- User can request different pizzas by name, style, and size.
- System prepares and bakes the pizza.
- Toppings, sauces, and crust can be customized at runtime.
- Payment calculated based on selection.

---

## ❌ Non-Functional Requirements
- Easy to extend new pizza types/styles.
- Code must follow SOLID principles.
- Minimize tight coupling.
- Runtime flexibility using decorators.

---

## 🧑‍💻 Actors (Use Cases)
| Actor       | Responsibilities                                  |
|-------------|---------------------------------------------------|
| Customer    | Selects pizza type, size, crust, toppings        |
| Pizza       | Prepares and bakes the pizza                     |
| Factory     | Creates pizza objects per style and type         |
| Topping     | Provides cost and name using decorators          |
| Size        | Adjusts base price via decorator pattern         |
| Payment     | Calculates total cost based on configuration     |

---

## 🧡 Class Design Notes

### 🍕 Pizza (Abstract Class)
- Methods: `prepare()`, `bake()`, `get_description()`, `get_cost()`
- Implemented by base pizzas (Margherita, Farmhouse)

### 🗒️ Concrete Pizza Classes
- `Margherita`, `Farmhouse`, etc.
- Include variations for NY/Chicago
- Define base cost and description

### 🏠 AbstractPizzaFactory (Abstract Class)
- Method: `get_pizza(pizza_type)`
- Extended by region-based factories (NY, Chicago)

### 🏢 Regional Factories
- `NewYorkFactory`, `ChicagoFactory`
- Return style-specific pizza instances

### 🧀 Toppings (Decorator Classes)
- Inherit from `Pizza`
- Wrap around base pizza to add description and cost
- Examples: `Cheese`, `Jalapenos`, `Olives`

### 🍽️ Size (Decorator Class)
- Wraps a pizza and adjusts cost based on size (Small, Medium, Large)
- Example: `LargeSize(pizza)` increases cost accordingly

### 💵 Payment
- `get_cost()` method on final decorated pizza object
- Dynamically reflects base + toppings + size cost

---

## 🔁 Relationships
| Class A               | ↔️ Relationship | Class B         | Justification                                        |
|------------------------|----------------|------------------|-----------------------------------------------------|
| AbstractPizzaFactory   | Inheritance    | RegionalFactory  | Regional factories specialize the abstract creator  |
| PizzaFactory           | Uses           | Pizza            | Central factory creates concrete pizza objects      |
| Pizza                 | Decorated By   | Toppings/Size    | Each decorator wraps the pizza and adds behavior    |
| Decorators            | Composition    | Pizza            | Decorators enhance behavior without subclassing     |

---

## 🔐 Design Patterns Used
| Pattern              | Purpose                                                              |
|----------------------|-----------------------------------------------------------------------|
| Factory              | Create pizzas based on type and region                                |
| Abstract Factory     | Create families of related pizzas (New York, Chicago variants)         |
| Decorator            | Add toppings and sizes dynamically and calculate cost at runtime      |
| Composition          | Pizza object composed of decorators (toppings and size)               |

---
| 🧩 Pattern           | 🤓 What It Means                                          | 🍕 How We Use It in Our Code                                                                                                                                                                                                                                    |
| -------------------- | --------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Factory**          | A class that creates objects based on some input.         | We use a **`PizzaFactory`** or **regional factory (like `NewYorkFactory`)** to create pizza objects like Margherita or Farmhouse without exposing the creation logic to the client. You just say "give me this pizza", and the factory gives you the right one. |
| **Abstract Factory** | A superclass to create a **family of related objects**.   | We have an **`AbstractPizzaFactory`** that all regional factories like `NewYorkFactory` or `ChicagoFactory` inherit from. This ensures each region can produce its own version of Margherita or Farmhouse.                                                      |
| **Decorator**        | Add features dynamically without changing the base class. | We use decorators like **`Cheese`**, **`Olives`**, **`Jalapenos`**, and **`Size`** to add things on top of the base pizza. These wrap the pizza object and update its **description** and **price** without modifying the pizza class itself.                   |
| **Composition**      | Building complex objects from simpler parts.              | Each pizza is built by **composing multiple decorators** (size + toppings) on top of a base pizza. This is flexible and modular. Each decorator “contains” the pizza it’s enhancing.                                                                            |


## ✅ SOLID Principles Applied
| Principle   | How it’s followed                                                    |
|-------------|----------------------------------------------------------------------|
| SRP         | Separate responsibilities: pizza creation vs topping vs payment     |
| OCP         | Easily add new pizzas, toppings, or sizes without modifying existing logic  |
| LSP         | Subclasses of Pizza and Topping decorators follow LSP               |
| ISP         | Only relevant methods exposed for each component                    |
| DIP         | High-level modules rely on Pizza abstraction not concrete classes   |

---

## 💡 Future Optimizations
- Add crust and sauce decorators
- Introduce combo offers and coupon discounts
- Store pizza orders in DB / JSON
- Use Builder Pattern for pizza construction
- Add UI or command-line interaction

---

## 🧪 Sample Run
```python
ny_factory = NewYorkFactory()
pizza = ny_factory.get_pizza("New York Farmhouse")
pizza = Cheese(pizza)
pizza = Jalapenos(pizza)
pizza = LargeSize(pizza)
print(pizza.get_description())  # New York Farmhouse, Cheese, Jalapenos, Large Size
print(pizza.get_cost())         # Base + Cheese + Jalapenos + LargeSize cost
```

---

## 📌 Summary
- Clean Factory + Abstract Factory + Decorator usage
- Runtime customization with toppings and sizes via decorators
- Followed OOP, SOLID, and extensible design
- Toppings, sizes, payments, and base pizzas are fully modular

---

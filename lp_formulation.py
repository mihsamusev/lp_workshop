"""
https://jckantor.github.io/CBE30338/06.04-Linear-Production-Model-in-Pyomo.html
x, y = rates of production in units per week

maximize: 40x + 30y
subject_to:
    x>0
    y>0
    x <= 40 demand constraint
    x + y <= 80 labor A constraints
    2x + y <= 100 labor b constraits
"""

from collections import namedtuple
import json
from pyomo.environ import (
    ConcreteModel,
    Var,
    Constraint,
    NonNegativeReals,
    Objective,
    maximize,
    SolverFactory,
)


def read_config(filepath: str):
    with open(filepath, "r") as fin:
        config = json.load(fin)
    return config


def build_model():
    model = ConcreteModel()

    # variables
    model.x = Var(domain=NonNegativeReals)
    model.y = Var(domain=NonNegativeReals)

    # constraints
    model.demand = Constraint(expr=model.x <= 40)
    model.laborA = Constraint(expr=model.x + model.y <= 80)
    model.laborB = Constraint(expr=2 * model.x + model.y <= 100)

    # objective
    model.objective = Objective(expr=40 * model.x + 30 * model.y, sense=maximize)

    return model


def describe_model(model):
    # model.display()
    # display solution
    print("\nProfit = ", model.objective())

    print("\nDecision Variables")
    print("x = ", model.x())
    print("y = ", model.y())

    print("\nConstraints")
    print("Demand  = ", model.demand())
    print("Labor A = ", model.laborA())
    print("Labor B = ", model.laborB())


def run():
    config = read_config("solver_config.json")

    model = build_model()
    model_constraints = model.component_map(ctype=[Constraint])
    for name, _ in model_constraints.items():
        print(name)

    solver = SolverFactory("scip")
    # https://www.scipopt.org/doc/html/PARAMETERS.php
    solver.options["limits/gap"] = 0.1
    solver.options["limits/softtime"] = 300

    solver.solve(model, tee=True)
    describe_model(model)


if __name__ == "__main__":
    run()

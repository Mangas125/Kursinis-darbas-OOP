from abc import ABC, abstractmethod
from itertools import combinations
import unittest
import json

class PowerPlant(ABC):
    def __init__(self, name, location, capacity_mw, cost_per_mw, is_clean_energy):
        self.name = name
        self.location = location
        self.capacity_mw = capacity_mw
        self.cost_per_mw = cost_per_mw
        self.is_clean_energy = is_clean_energy
        self.status = "inactive"

    def start(self):
        self.status = "active"

    def shutdown(self):
        self.status = "inactive"

    @abstractmethod
    def fuel_type(self):
        pass

    def generate_report(self):
        report = (
            f"[{self.__class__.__name__}] Name: {self.name}\n"
            f"Location: {self.location}\n"
            f"Capacity: {self.capacity_mw} MW\n"
            f"Status: {self.status}\n"
            f"Fuel Type: {self.fuel_type()}\n"
            f"Cost per MW: {self.cost_per_mw} EUR\n"
            f"Clean Energy: {'Yes' if self.is_clean_energy else 'No'}\n"
        )
        return report

# Subclasses
class SolarPlant(PowerPlant):
    def fuel_type(self):
        return "Solar Energy"

class CoalPlant(PowerPlant):
    def fuel_type(self):
        return "Coal"

class HydroPlant(PowerPlant):
    def fuel_type(self):
        return "Water"

class NuclearPlant(PowerPlant):
    def fuel_type(self):
        return "Uranium"

class WindPlant(PowerPlant):
    def fuel_type(self):
        return "Wind"

class WasteToEnergyPlant(PowerPlant):
    def fuel_type(self):
        return "Waste"

# Factory Method
class PowerPlantFactory:
    @staticmethod
    def create_plant(plant_type, name, location, capacity_mw, cost_per_mw, is_clean_energy):
        plant_type = plant_type.lower()
        if plant_type == "solar":
            return SolarPlant(name, location, capacity_mw, cost_per_mw, is_clean_energy)
        elif plant_type == "coal":
            return CoalPlant(name, location, capacity_mw, cost_per_mw, is_clean_energy)
        elif plant_type == "hydro":
            return HydroPlant(name, location, capacity_mw, cost_per_mw, is_clean_energy)
        elif plant_type == "nuclear":
            return NuclearPlant(name, location, capacity_mw, cost_per_mw, is_clean_energy)
        elif plant_type == "wind":
            return WindPlant(name, location, capacity_mw, cost_per_mw, is_clean_energy)
        elif plant_type == "waste":
            return WasteToEnergyPlant(name, location, capacity_mw, cost_per_mw, is_clean_energy)
        else:
            raise ValueError(f"Unknown plant type: {plant_type}")

# Manager
class PowerPlantManager:
    def __init__(self):
        self.plants = []

    def add_plant(self, plant: PowerPlant):
        self.plants.append(plant)

    def remove_plant(self, name: str):
        self.plants = [plant for plant in self.plants if plant.name != name]

    def list_plants(self):
        for plant in self.plants:
            print(plant.generate_report())
            print("------------------------")

    def fulfill_demand(self, mw_required, history_file="history.txt"):
        total_available = sum(plant.capacity_mw for plant in self.plants)
        output_lines = [f"Total available capacity: {total_available} MW"]

        if total_available < mw_required:
            shortage = mw_required - total_available
            output_lines.append(f"Cannot fulfill demand. Short by {shortage} MW.")
            self._log_to_file(output_lines, history_file)
            print("\n".join(output_lines))
            return

        best_combination = None
        best_over = float('inf')

        for r in range(1, len(self.plants) + 1):
            for combo in combinations(self.plants, r):
                total_capacity = sum(plant.capacity_mw for plant in combo)
                if total_capacity >= mw_required:
                    over = total_capacity - mw_required
                    if over < best_over or (over == best_over and (best_combination is None or len(combo) < len(best_combination))):
                        best_combination = combo
                        best_over = over

        if best_combination is None:
            output_lines.append("No combination of plants can fulfill the demand.")
            self._log_to_file(output_lines, history_file)
            print("\n".join(output_lines))
            return

        total_supplied = sum(plant.capacity_mw for plant in best_combination)
        total_cost = sum(plant.capacity_mw * plant.cost_per_mw for plant in best_combination)
        clean_energy_mw = sum(plant.capacity_mw for plant in best_combination if plant.is_clean_energy)

        for plant in best_combination:
            plant.start()

        clean_percentage = (clean_energy_mw / total_supplied) * 100 if total_supplied > 0 else 0

        output_lines.append(f"Electricity demand: {mw_required} MW")
        output_lines.append("Plants activated:")
        for plant in best_combination:
            output_lines.append(f" - {plant.__class__.__name__} \"{plant.name}\" [{plant.capacity_mw} MW @ {plant.cost_per_mw} EUR/MW]")
        output_lines.append(f"Total supplied: {total_supplied} MW")
        output_lines.append(f"Total cost: {total_cost:.2f} EUR")
        output_lines.append(f"Clean Energy: {clean_percentage:.1f}%")
        if total_supplied > mw_required:
            output_lines.append(f"Over the demand by {total_supplied - mw_required} MW.")

        self._log_to_file(output_lines, history_file)
        print("\n".join(output_lines))

    def _log_to_file(self, lines, filename):
        with open(filename, "a") as file:
            file.write("\n".join(lines) + "\n---\n")

    def show_history(self, filename="history.txt"):
        try:
            with open(filename, "r") as file:
                print(file.read())
        except FileNotFoundError:
            print("No history found.")

# Unit Tests
class TestPowerPlantManager(unittest.TestCase):
    def setUp(self):
        self.manager = PowerPlantManager()
        self.manager.add_plant(SolarPlant("SunFarm", "Spain", 500, 30, True))
        self.manager.add_plant(CoalPlant("CoalBurner", "Poland", 800, 45, False))
        self.manager.add_plant(HydroPlant("RiverPower", "Norway", 400, 20, True))

    def test_add_and_remove_plant(self):
        self.assertEqual(len(self.manager.plants), 3)
        self.manager.remove_plant("CoalBurner")
        self.assertEqual(len(self.manager.plants), 2)
        names = [p.name for p in self.manager.plants]
        self.assertNotIn("CoalBurner", names)

    def test_fulfill_demand_exact(self):
        self.manager.fulfill_demand(900)  # should pick 500 + 400
        active_plants = [p for p in self.manager.plants if p.status == "active"]
        self.assertEqual(sum(p.capacity_mw for p in active_plants), 900)

    def test_fulfill_demand_not_possible(self):
        self.manager.fulfill_demand(5000)
        active_plants = [p for p in self.manager.plants if p.status == "active"]
        self.assertEqual(len(active_plants), 0)

# Example usage 1
if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)

# Example usage 2
def main():
    manager = PowerPlantManager()

    manager.add_plant(PowerPlantFactory.create_plant("solar", "SunFarm", "Spain", 500, 30, True))
    manager.add_plant(PowerPlantFactory.create_plant("coal", "CoalBurner", "Poland", 800, 45, False))
    manager.add_plant(PowerPlantFactory.create_plant("hydro", "RiverPower", "Norway", 400, 20, True))
    manager.add_plant(PowerPlantFactory.create_plant("nuclear", "AtomicOne", "France", 1200, 40, False))
    manager.add_plant(PowerPlantFactory.create_plant("wind", "WindyHill", "Denmark", 300, 25, True))
    manager.add_plant(PowerPlantFactory.create_plant("waste", "TrashBurn", "Germany", 200, 35, False))

    print("\n=== List of all plants ===")
    manager.list_plants()

    print("\n=== Fulfilling 1500 MW demand ===")
    manager.fulfill_demand(1500)

    print("\n=== Fulfilling 4000 MW demand ===")
    manager.fulfill_demand(4000)

    print("\n=== Fulfilling 450 MW demand ===")
    manager.fulfill_demand(450)

    print("\n=== Removing CoalBurner ===")
    manager.remove_plant("CoalBurner")

    print("\n=== Adding SunRise ===")
    manager.add_plant(PowerPlantFactory.create_plant("solar", "SunRise", "Lithuania", 600, 29, True))

    print("\n=== List after removal and addition===")
    manager.list_plants()

if __name__ == "__main__":
    main()

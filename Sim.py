import random
import datetime

# Define baseline data for the simulation
baseline_data = {
    "economic_conditions": {
        "inflation_rate": 2.5,
        "gdp_growth_rate": 1.5
    },
    "energy_market_conditions": {
        "electricity_prices": 100,
        "gas_prices": 75
    },
    "weather_conditions": {
        "average_temperature": 10,
        "wind_speed": 15,
        "solar_irradiance": 800,  # Existing parameter
        "humidity": 60,          # New parameter
        "cloud_cover": 0.5       # New parameter (0 to 1 scale)
    }
}

# Utility function for validation
def validate_input(data, required_keys):
    if not all(key in data for key in required_keys):
        raise ValueError(f"Missing one or more required keys: {required_keys}")

# Enhanced electricity generation function
def calculate_electricity_generation_advanced(economic_conditions, weather_data, energy_market_conditions):
    validate_input(weather_data, ["wind_speed", "solar_irradiance", "cloud_cover"])
    validate_input(energy_market_conditions, ["electricity_prices"])

    baseline_generation = {
        "gas": 30000,
        "coal": 10000,
        "wind": 10000,
        "solar": 5000,
        "nuclear": 9000
    }
    wind_speed_factor = weather_data["wind_speed"] / 15
    solar_irradiance_factor = weather_data["solar_irradiance"] / 1000
    cloud_cover_factor = 1 - weather_data["cloud_cover"]  # Adjustment for cloud cover

    price_elasticity = 0.1  # Adjust as per realistic models

    # Adjust generation based on weather and price
    baseline_generation["wind"] *= wind_speed_factor
    baseline_generation["solar"] *= solar_irradiance_factor * cloud_cover_factor
    baseline_generation["gas"] *= 1 + price_elasticity * (100 - energy_market_conditions["electricity_prices"])
    baseline_generation["coal"] *= 1 + price_elasticity * (100 - energy_market_conditions["electricity_prices"])

    total_generation = sum(baseline_generation.values())
    return {
        "generation_by_source": baseline_generation,
        "total_generation": total_generation
    }

# Updated transmission network simulation
def simulate_transmission_network(electricity_generated, weather_conditions):
    validate_input(weather_conditions, ["average_temperature"])

    baseline_capacity = 50000
    baseline_efficiency = 95 - 0.2 * max(weather_conditions["average_temperature"] - 25, 0)  # Gradual efficiency reduction

    actual_transmission = min(electricity_generated, baseline_capacity) * (baseline_efficiency / 100)
    return {
        "capacity": baseline_capacity,
        "efficiency": baseline_efficiency,
        "actual_transmission": actual_transmission
    }

# Dynamic gas network simulation
def simulate_gas_network(economic_conditions, energy_market_conditions):
    validate_input(economic_conditions, ["inflation_rate", "gdp_growth_rate"])
    validate_input(energy_market_conditions, ["gas_prices"])

    baseline_production = 500
    price_elasticity = 0.05  # Adjust as per realistic models
    price_factor = energy_market_conditions["gas_prices"] / 75
    adjusted_production = baseline_production * (1 + price_elasticity * (75 - energy_market_conditions["gas_prices"]))

    # Dynamic gas import/export based on economic conditions
    gas_import = 200 * (1 + economic_conditions["gdp_growth_rate"] / 100)
    gas_export = 100 * (1 + economic_conditions["inflation_rate"] / 100)

    net_gas_availability = adjusted_production + gas_import - gas_export
    return {
        "production": adjusted_production,
        "import": gas_import,
        "export": gas_export,
        "net_availability": net_gas_availability
    }

# Updated GSP group simulation
def simulate_gsp_group_import_export(gsp_groups, economic_conditions, energy_market_conditions):
    gsp_results = {}
    for gsp in gsp_groups:
        validate_input(gsp, ["electricity_import", "electricity_export", "gas_import", "gas_export"])

        # Dynamic pricing impact
        electricity_import_price_factor = energy_market_conditions["electricity_prices"] / 100
        gas_price_factor = energy_market_conditions["gas_prices"] / 75

        electricity_import = gsp["electricity_import"] * electricity_import_price_factor
        electricity_export = gsp["electricity_export"] * electricity_import_price_factor
        gas_import = gsp["gas_import"] * gas_price_factor
        gas_export = gsp["gas_export"] * gas_price_factor

        net_electricity_import_export = electricity_import - electricity_export
        net_gas_import_export = gas_import - gas_export
        gsp_results[gsp["name"]] = {
            "electricity_import": electricity_import,
            "electricity_export": electricity_export,
            "gas_import": gas_import,
            "gas_export": gas_export,
            "net_electricity_import_export": net_electricity_import_export,
            "net_gas_import_export": net_gas_import_export
        }
    return gsp_results

def calculate_exported_energy_by_source(electricity_generation, gsp_import_export):
    total_exported_energy = sum(gsp["electricity_export"] for gsp in gsp_import_export.values())
    generation_by_source = electricity_generation["generation_by_source"]
    total_generation = electricity_generation["total_generation"]
    exported_energy_by_source = {}
    for source, generation in generation_by_source.items():
        source_contribution = generation / total_generation
        exported_energy_by_source[source] = total_exported_energy * source_contribution
    return exported_energy_by_source

def update_economic_conditions(economic_conditions, market_trends):
    economic_conditions["inflation_rate"] += market_trends["inflation_change"]
    economic_conditions["gdp_growth_rate"] += market_trends["gdp_growth_change"]
    economic_conditions["energy_market_conditions"]["electricity_prices"] *= (1 + random.uniform(-0.05, 0.05))
    economic_conditions["energy_market_conditions"]["gas_prices"] *= (1 + random.uniform(-0.05, 0.05))
    return economic_conditions

def simulate_demand_fluctuations(gsp_groups, date_time):
    for gsp in gsp_groups:
        if 17 <= date_time.hour <= 21:
            gsp["electricity_demand"] *= 1.2
            gsp["gas_demand"] *= 1.1
        if date_time.month in [12, 1, 2]:
            gsp["gas_demand"] *= 1.3
    return gsp_groups

# Example usage
current_date_time = datetime.datetime.now()
gsp_groups_demo = [
    {"name": "GSP1", "electricity_demand": 150, "gas_demand": 180},
    {"name": "GSP2", "electricity_demand": 130, "gas_demand": 160}
]

detailed_weather_data = {
    "average_temperature": 10,
    "wind_speed": 20,
    "solar_irradiance": 800
}

electricity_generation = calculate_electricity_generation_advanced(
    baseline_data["economic_conditions"],
    detailed_weather_data,
    baseline_data["energy_market_conditions"]
)

transmission_network = simulate_transmission_network(
    electricity_generation["total_generation"],
    detailed_weather_data
)

gas_network = simulate_gas_network(
    baseline_data["economic_conditions"],
    baseline_data["energy_market_conditions"]
)

gsp_import_export = simulate_gsp_group_import_export(
    gsp_groups_demo,
    baseline_data["economic_conditions"],
    baseline_data["energy_market_conditions"]
)

exported_energy_by_source = calculate_exported_energy_by_source(
    electricity_generation,
    gsp_import_export
)

market_trends_example = {
    "inflation_change": 0.1,
    "gdp_growth_change": -0.1
}

updated_economic_conditions = update_economic_conditions(
    baseline_data["economic_conditions"],
    market_trends_example
)

gsp_groups_with_fluctuations = simulate_demand_fluctuations(
    gsp_groups_demo,
    current_date_time
)

# Define baseline data for the simulation
baseline_data = {
    "economic_conditions": {
        "inflation_rate": 2.5,  # Example average inflation rate
        "gdp_growth_rate": 1.5  # Example average GDP growth rate
    },
    "energy_market_conditions": {
        "electricity_prices": 100,  # Example average price per MWh
        "gas_prices": 75  # Example average price per MWh
    },
    "weather_conditions": {
        "average_temperature": 10,  # Example average temperature in Celsius
        "wind_speed": 15  # Example average wind speed in km/h
    }
}

# Function to calculate electricity generation based on different power sources
def calculate_electricity_generation(economic_conditions, weather_conditions, energy_market_conditions):
    """
    Calculate electricity generation based on different power sources.
    Adjusts the generation capacities based on economic and weather conditions.
    """
    baseline_generation = {
        "gas": 30000,
        "coal": 10000,
        "wind": 15000,
        "solar": 8000,
        "nuclear": 9000
    }
    baseline_generation["wind"] *= (weather_conditions["wind_speed"] / 15)
    price_factor = energy_market_conditions["electricity_prices"] / 100
    baseline_generation["gas"] *= (1 / price_factor)
    baseline_generation["coal"] *= (1 / price_factor)
    total_generation = sum(baseline_generation.values())
    return {
        "generation_by_source": baseline_generation,
        "total_generation": total_generation
    }

# Function to simulate the transmission network efficiency and capacity
def simulate_transmission_network(electricity_generated, weather_conditions):
    """
    Simulate the transmission network efficiency and capacity.
    """
    baseline_capacity = 50000
    baseline_efficiency = 95
    if weather_conditions["average_temperature"] > 25:
        baseline_efficiency -= 3
    actual_transmission = min(electricity_generated, baseline_capacity) * (baseline_efficiency / 100)
    return {
        "capacity": baseline_capacity,
        "efficiency": baseline_efficiency,
        "actual_transmission": actual_transmission
    }

# Function to simulate the gas network
def simulate_gas_network(economic_conditions, energy_market_conditions):
    """
    Simulate the gas network, including production, import, export, and distribution.
    """
    baseline_production = 500
    price_factor = energy_market_conditions["gas_prices"] / 75
    adjusted_production = baseline_production * (1 / price_factor)
    gas_import = 200
    gas_export = 100
    net_gas_availability = adjusted_production + gas_import - gas_export
    return {
        "production": adjusted_production,
        "import": gas_import,
        "export": gas_export,
        "net_availability": net_gas_availability
    }

# Function to simulate the total electricity and gas import/export for each GSP Group in the UK
def simulate_gsp_group_import_export(gsp_groups, economic_conditions, energy_market_conditions):
    """
    Simulate the total electricity and gas import/export for each GSP Group in the UK.
    """
    gsp_results = {}
    for gsp in gsp_groups:
        electricity_import = gsp["electricity_import"] * (energy_market_conditions["electricity_prices"] / 100)
        electricity_export = gsp["electricity_export"] * (energy_market_conditions["electricity_prices"] / 100)
        gas_import = gsp["gas_import"] * (energy_market_conditions["gas_prices"] / 75)
        gas_export = gsp["gas_export"] * (energy_market_conditions["gas_prices"] / 75)
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

# Function to calculate the total amount of each power type used to generate the total exported energy
def calculate_exported_energy_by_source(electricity_generation, gsp_import_export):
    """
    Calculate the total amount of each power type used to generate the total exported energy.
    """
    total_exported_energy = sum(gsp["electricity_export"] for gsp in gsp_import_export.values())
    generation_by_source = electricity_generation["generation_by_source"]
    total_generation = electricity_generation["total_generation"]
    exported_energy_by_source = {}
    for source, generation in generation_by_source.items():
        source_contribution = generation / total_generation
        exported_energy_by_source[source] = total_exported_energy * source_contribution
    return exported_energy_by_source

# Function to calculate the net demand level for each GSP group and the whole of the UK
def calculate_net_demand(gsp_groups, electricity_generation, gas_network):
    """
    Calculate the net demand level for each GSP group and the whole of the UK.
    """
    total_uk_electricity_demand = 0
    total_uk_gas_demand = 0
    gsp_net_demands = {}

    for gsp in gsp_groups:
        net_electricity_demand = gsp["electricity_demand"] - electricity_generation["total_generation"]
        net_gas_demand = gsp["gas_demand"] - gas_network["net_availability"]
        total_uk_electricity_demand += net_electricity_demand
        total_uk_gas_demand += net_gas_demand
        gsp_net_demands[gsp["name"]] = {
            "net_electricity_demand": net_electricity_demand,
            "net_gas_demand": net_gas_demand
        }

    total_uk_net_demand = {
        "total_electricity_demand": total_uk_electricity_demand,
        "total_gas_demand": total_uk_gas_demand
    }

    return {"gsp_net_demands": gsp_net_demands, "total_uk_net_demand": total_uk_net_demand}

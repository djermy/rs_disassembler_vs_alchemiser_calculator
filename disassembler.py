from api_fetcher import get_item_cost
from database_handler import id_grabber
from calculator_utils import cost_of_charge
from user_input import validate_choice, is_choice_valid
import constants

def disassembler_calculator():

    # get users item index to disassemble
    choice = validate_choice()
    
    # define chosen items name via index
    item_name = constants.ITEMS[choice]

    # get item id
    item_id = id_grabber(item_name)

    # get current item cost
    item_cost = get_item_cost(item_id)

    # get value of empty divine charge
    empty_divine_charge_value = get_item_cost(constants.EMPTY_DIVINE_CHARGE_ID)

    # calculate cost of machine fuel to process 1 item
    cost_of_charges = constants.DISASSEMBLER_CHARGES_PER_ITEM * cost_of_charge()
    
    # total cost to process 1 of the chosen item
    cost_per_item = round((item_cost + cost_of_charges), 2)

    # hourly and daily costs to process chosen item
    hourly = round((cost_per_item * constants.ITEMS_DISASSEMBLED_PER_HOUR), 2)
    daily = round((hourly * 24), 2)
    
    if item_name == 'soapstone':

        soapstone_calculator(daily, empty_divine_charge_value)


    else:
        daily_empty_charges = calculate_empty_charges_per_day(constants.LOGS_COMPS)
    
        # value of empty divine charges per day
        daily_empty_charge_value = round(empty_divine_charge_value * daily_empty_charges, 2)
        
        # profit/loss per day/hour
        daily_profit = daily_empty_charge_value - daily
        hourly_profit = daily_profit / 24
        per_item_profit = hourly_profit / constants.ITEMS_DISASSEMBLED_PER_HOUR

        print(f'The profit/loss to disassemble {item_name} is: {round(per_item_profit, 2)}')
        print(f'The hourly profit/loss to disassemble {item_name} is: {round(hourly_profit, 2)}')
        print(f'The daily profit/loss to disassemble {item_name} is: {round(daily_profit, 2)}')

def calculate_daily_soapstone_comps():
    '''
    Calculates and returns 2 values: daily_historic, daily_classic.
    The amount of daily historic and classic components found.
    '''

    comps = constants.SOAPSTONE_COMPS
    
    # divine charges made
    daily_empty_charges = calculate_empty_charges_per_day(comps)
    
    # historic components
    p_historic = comps['special']['historic']
    hourly_historic = constants.ITEMS_DISASSEMBLED_PER_HOUR * p_historic
    daily_historic = hourly_historic * 24
   
    # classic components
    p_not_historic = 1 - p_historic
    p_classic = p_not_historic * comps['special']['classic']
    hourly_classic = constants.ITEMS_DISASSEMBLED_PER_HOUR * p_classic
    daily_classic = hourly_classic * 24
    
    return daily_historic, daily_classic

def calculate_empty_charges_per_day(comps):
    p_junk = comps['junk']
    p_not_junk = 1 - p_junk
    p_simple = comps['simple parts']
    p_overall = p_not_junk * p_simple
    simple_parts_per_hour = constants.ITEMS_DISASSEMBLED_PER_HOUR * p_overall
    simple_parts_per_day = simple_parts_per_hour * 24
    empty_divine_charges_per_day = simple_parts_per_day / constants.SIMPLE_PARTS_PER_EMPTY_DIVINE_CHARGE

    return round(empty_divine_charges_per_day, 2)

def calculate_daily_crates(daily_historic, daily_classic):
    '''
    Take daily historic and classic components from soapstone.
    Calculate the daily small and large historic and classic crates-
    made per day and return them as a dictionary object.
    '''

    # calculate daily small crates
    daily_small_historic = round(daily_historic / constants.SMALL_CRATE_COMPS, 2)
    daily_small_classic = round(daily_classic / constants.SMALL_CRATE_COMPS, 2)

    # calculate daily large crates
    daily_large_historic = round(daily_historic / constants.LARGE_CRATE_COMPS, 2)
    daily_large_classic = round(daily_classic / constants.LARGE_CRATE_COMPS, 2)

    return {
        'daily_small_historic': daily_small_historic,
        'daily_large_historic': daily_large_historic,
        'daily_small_classic': daily_small_classic,
        'daily_large_classic': daily_large_classic
    }

def crate_values():
    '''
    Gets values of and returns dictionary of crate values.
    '''

    # get the value of all 4 crates
    small_historic = get_item_cost(constants.SMALL_HISTORIC_CRATE_ID)
    large_historic = get_item_cost(constants.LARGE_HISTORIC_CRATE_ID)
    small_classic = get_item_cost(constants.SMALL_CLASSIC_CRATE_ID)
    large_classic = get_item_cost(constants.LARGE_CLASSIC_CRATE_ID)

    crates = {
        'historic': {
            'small': small_historic,
            'large': large_historic
        },
        'classic': {
            'small': small_classic,
            'large': large_classic
        }
    }
    
    return crates

def calculate_comp_value(crates):
    '''
    Calculates and returns the values of historic and classic comps and returns-
    them as a dictionary object.
    '''

    # calculate historic comp values
    small_historic_comp_value = round(crates['historic']['small'] / constants.SMALL_CRATE_COMPS, 2)
    large_historic_comp_value = round(crates['historic']['large'] / constants.LARGE_CRATE_COMPS, 2)

    # calculate classic comp values
    small_classic_comp_value = round(crates['classic']['small'] / constants.SMALL_CRATE_COMPS, 2)
    large_classic_comp_value = round(crates['classic']['large'] / constants.LARGE_CRATE_COMPS, 2)

    component_values = {
        'historic': {
            'small_value': small_historic_comp_value,
            'large_value': large_historic_comp_value
        },
        'classic': {
            'small_value': small_classic_comp_value,
            'large_value': large_classic_comp_value
        }
    }

    return component_values

def calculate_best_crate(comp_values):
    '''
    Takes dictionary object of component values for small and large crates-
    and returns a dictionary object of the most valuable component and which crate.
    '''

    best_crate = {
        'historic': {
            'value': None,
            'crate': None
        },
        'classic': {
            'value': None,
            'crate': None
        }
    }

    if comp_values['historic']['small_value'] > comp_values['historic']['large_value']:
        best_crate['historic']['value'] = comp_values['historic']['small_value']
        best_crate['historic']['crate'] = 'small'
    else:
        best_crate['historic']['value'] = comp_values['historic']['large_value']
        best_crate['historic']['crate'] = 'large'

    if comp_values['classic']['small_value'] > comp_values['classic']['large_value']:
        best_crate['classic']['value'] = comp_values['classic']['small_value']
        best_crate['classic']['crate'] = 'small'
    else:
        best_crate['classic']['value'] = comp_values['classic']['large_value']
        best_crate['classic']['crate'] = 'large'

    return best_crate

def soapstone_calculator(daily, empty_divine_charge_value):
    '''
    Perform calculations and return best crate and values for both components.
    '''
    # get number of daily empty divine charges
    daily_empty_charges = calculate_empty_charges_per_day(constants.SOAPSTONE_COMPS)

    # get number of daily comps
    daily_historic_comps, daily_classic_comps = calculate_daily_soapstone_comps()
    
    # get number of crates made per day
    daily_crates = calculate_daily_crates(daily_historic_comps, daily_classic_comps)

    # crate values
    crates = crate_values()

    # get value of comps for all 4 crates
    comp_values = calculate_comp_value(crates)

    # get best crate type and value for both comps
    best_crates = calculate_best_crate(comp_values)

    # daily values of all historic and classic comps
    daily_historic_value = round(best_crates['historic']['value'] * daily_historic_comps, 2)
    daily_classic_value = round(best_crates['classic']['value'] * daily_classic_comps, 2)
    total_daily_comp_value = round(daily_historic_value + daily_classic_value, 2)

    # value of empty divine charges per day
    daily_empty_charge_value = round(empty_divine_charge_value * daily_empty_charges, 2)

    # total value
    total_daily_value = round(total_daily_comp_value + daily_empty_charge_value, 2)

    # profit/loss
    daily_profit_or_loss = round(total_daily_value - daily, 2)
    hourly = round(daily_profit_or_loss / 24, 2)
    single = round(hourly / constants.ITEMS_DISASSEMBLED_PER_HOUR)

    # test print historic
    print(f'The best crate to make for historic components are', end='')
    print(f' {best_crates["historic"]["crate"]}, with a component', end='')
    print(f' value of {best_crates["historic"]["value"]}')
    
    # test print classic
    print(f'The best crate to make for classic components are', end='')
    print(f' {best_crates["classic"]["crate"]}, with a component', end='')
    print(f' value of {best_crates["classic"]["value"]}')


    print('The below values assume you make the stated best crate for both components!')
    print(f'The profit or loss to disassemble soapstone is {single}')
    print(f'The hourly profit or loss to disassemble soapstone is {hourly}')
    print(f'The daily profit or loss to disassemble soapstone is {daily_profit_or_loss}')

disassembler_calculator()
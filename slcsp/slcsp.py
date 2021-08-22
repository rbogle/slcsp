import csv


def load_datafile(filename: str) -> list:
    """Takes a filename for a csv file and converts the file to a list

    Args:
        filename (str): csv filename

    Returns:
        list: data from csv file
    """
    with open(filename) as csv_file:
        data = list()
        reader = csv.reader(csv_file)
        for row in reader:
            data.append(row)
        return data


def filter_plans(plans: list, plan: str = "Silver") -> dict:
    """Filters the raw list from plans file for the 'plan' needed
       and builds a dictonary of state, area, and rates list.

    Args:
        plans (list): original list of plans [ id, state, level, price, region]
        plan (str, optional): Plan type to filter on. Defaults to 'Silver'.

    Returns:
        dict: { 'state' :
                    'rate_area': [
                        rate1, rate2,...
                    ]
               }
    """
    # remove header
    plans.pop(0)
    filtered_data = dict()
    for row in plans:
        # only process the plan we want default: 'Silver'
        if row[2] == plan:
            state = row[1]
            area = row[4]
            rate = row[3]
            # seed a dict for the state if dne
            if state not in filtered_data:
                filtered_data[state] = dict()
            # seed a list for the area if dne
            if area not in filtered_data[state]:
                filtered_data[state][area] = list()
            # now append the rate to the list for the area
            filtered_data[state][area].append(float(rate))
    return filtered_data


def filter_zip_map(zip_map: list) -> dict:
    """Takes a raw list of zipcode,state,county_code,name,rate_area
        builds a dictionary mapping a zip to its state(s) along with
        list of rate_areas within each state

    Args:
        zip_map (list): List of arrays: zipcode,state,county_code,name,rate_area

    Returns:
        dict: {
            'zipcode':
            {
                'State':[area1, area2, ...]
            }
        }
    """
    # remove header
    zip_map.pop(0)
    filtered_map = dict()
    for row in zip_map:
        zipcode = row[0]
        state = row[1]
        area = row[4]
        # seed a dict for the zipcode if dne
        if zipcode not in filtered_map:
            filtered_map[zipcode] = dict()
        # seed a list for the state if dne
        if state not in filtered_map[zipcode]:
            filtered_map[zipcode][state] = list()
        # put the area in to the list if dne
        if area not in filtered_map[zipcode][state]:
            filtered_map[zipcode][state].append(area)
    return filtered_map


def lookup_state_area(zip_code: str, zip_map: dict) -> tuple:
    """Takes a zipcode and filtered zip_map and returns a tuple
        of the state and area for that zip

    Args:
        zip_code (str): [description]
        zip_map (dict): generated from filtered_zip_map

    Returns:
        tuple (str, str): state,area
    """
    states = zip_map.get(zip_code, None)
    # unknown zip code
    if states is None:
        return None

    # more than one state in zip_code = ambiguous answer
    if len(states.keys()) > 1:
        return None

    # gets the first key, should be only one
    state = next(iter(states))
    areas = states[state]

    # more than one rate area for zipcode = ambiguous answer
    if len(areas) != 1:
        return None
    else:
        return (state, areas[0])


def lookup_plan_rates(state: str, area: str, plan_rates: dict) -> list:
    """Returns a sorted list of rates for the state and area

    Args:
        state (str): [description]
        area (str): [description]
        plan_rates (dict): [description]

    Returns:
        list: [sorted rates]
    """
    areas = plan_rates.get(state, None)
    if areas is not None:
        rates = areas.get(area, None)
        if rates is not None:
            rates.sort()
            return rates
    return None


def find_slcsp(zip_map: dict, plans: dict, zip_list: list) -> list:
    """Dives into the the plan rates to find the slcsp for each zip
       and adds the slcsp to the row in ziplist

    Args:
        zip_map (dict): mapping of zips to state,area
        plans (dict): mapping of rates for a plan to state, area
        zip_list (list): list of zips to discover slcsp for

    Returns:
        list: original list of zips augmented with the slcsp data
    """
    for row in zip_list:
        zip_code = row[0]
        geo = lookup_state_area(zip_code, zip_map)
        if geo is not None:
            state, area = geo
            rates = lookup_plan_rates(state, area, plans)
            if rates is not None and len(rates) > 1:
                # set empty field to second lowest rate
                row[1] = str(rates[1])
    return zip_list


def process_data(plans_filename: str, zip_map_filename: str, slcsp_filename: str):
    """Main processes the 3 required files, creates the filtered data
       and then iterates over the provided zip list to find the slcsp for each
       then prints out the pair of zip and slcsp in order requested.

    Args:
        plans_filename (str): [description]
        zip_map_filename (str): [description]
        slcsp_filename (str): [description]
    """

    # load and filter plan data to silver
    all_plans = load_datafile(plans_filename)
    silverplans = filter_plans(all_plans)

    # load and filter zip_map data
    zip_area_data = load_datafile(zip_map_filename)
    zip_mapping = filter_zip_map(zip_area_data)

    # list of zips for search and output
    zip_list = load_datafile(slcsp_filename)
    headers = zip_list.pop(0)

    slcsp_list = find_slcsp(zip_mapping, silverplans, zip_list)

    print(",".join(headers))
    for slcsp in slcsp_list:
        print(",".join(slcsp))

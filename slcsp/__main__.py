import slcsp
import argparse
import os
import sys

if __name__ == "__main__":

    plans_filename = "data/plans.csv"
    zip_map_filename = "data/zips.csv"
    slcsp_filename = "data/slcsp.csv"

    description = "Find the second lowest cost sliver plan for a provide list of zipcode"
    prog = "slcsp"

    parser = argparse.ArgumentParser(description=description, prog=prog)
    parser.add_argument("--plans", "-p", help="path to file containing rate plans")
    parser.add_argument("--areas", "-a", help="path to file mapping zipcodes to rate areas")
    parser.add_argument("--zips", "-z", help="path to file with zipcode to search for slcsp")

    args = parser.parse_args()
    
    if args.plans:
        plans_filename = args.plans
    if args.areas: 
        zip_map_filename = args.areas
    if args.zips:
        slcsp_filename = args.zips

    if not os.path.isfile(plans_filename):
        print (f"The plans file specified: {plans_filename} could not be found")
        sys.exit()
    if not os.path.isfile(zip_map_filename):
        print (f"The areas file specified: {zip_map_filename} could not be found")
        sys.exit()
    if not os.path.isfile(slcsp_filename):
        print (f"The zipcode search file specified: {slcsp_filename} could not be found")
        sys.exit()

    slcsp.process_data(plans_filename, zip_map_filename, slcsp_filename)

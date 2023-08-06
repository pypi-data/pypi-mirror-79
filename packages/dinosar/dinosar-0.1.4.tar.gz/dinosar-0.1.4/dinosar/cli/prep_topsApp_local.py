#!/usr/bin/env python3
"""Prepare directory for running topsApp.py on local machine.

Generate interferogram folder containing:
topsApp.xml
SLCs
Orbit files
Aux file


Example
-------

$ prep_topsApp_aws.py -i query.geojson -m 20141130 -s 20141106 -n 1 -r 46.45 46.55 -120.53 -120.43

$ prep_topsApp_aws.py -i query.geojson -t topsApp-template.yml -m 20141130 -s 20141106

Author: Scott Henderson (scottyh@uw.edu)
Updated: 08/2018
"""
import argparse
import os
from dinosar.archive import asf
import dinosar.isce as dice


def cmdLineParse():
    """Command line parser."""
    parser = argparse.ArgumentParser(description="prepare ISCE 2.2 topsApp.py")
    parser.add_argument(
        "-i",
        type=str,
        dest="inventory",
        required=True,
        help="Inventory vector file (query.geojson)",
    )
    parser.add_argument(
        "-m", type=str, dest="master", required=True, help="Master date"
    )
    parser.add_argument("-s", type=str, dest="slave", required=True, help="Slave date")
    parser.add_argument(
        "-p",
        type=str,
        dest="path",
        required=True,
        help="Path/Track/RelativeOrbit Number",
    )
    parser.add_argument(
        "-n",
        type=int,
        nargs="+",
        dest="swaths",
        required=False,
        choices=(1, 2, 3),
        help="Subswath numbers to process",
    )
    parser.add_argument(
        "-o",
        dest="poeorb",
        action="store_true",
        required=False,
        default=True,
        help="Use precise orbits (True/False)",
    )
    parser.add_argument(
        "-t",
        type=str,
        dest="template",
        required=False,
        help="Path to YAML input template file",
    )
    parser.add_argument(
        "-d", type=str, dest="dem", required=False, help="Path to DEM file"
    )
    parser.add_argument(
        "-b",
        type=float,
        nargs=4,
        dest="roi",
        required=False,
        metavar=("S", "N", "W", "E"),
        help="Region of interest bbox [S,N,W,E]",
    )
    parser.add_argument(
        "-g",
        type=float,
        nargs=4,
        dest="gbox",
        required=False,
        metavar=("S", "N", "W", "E"),
        help="Geocode bbox [S,N,W,E]",
    )
    parser.add_argument(
        "-a", type=int, dest="alooks", required=False, help="Azimuthlooks"
    )
    parser.add_argument(
        "-r", type=int, dest="rlooks", required=False, help="Rangelooks"
    )
    parser.add_argument(
        "-f", type=float, dest="filtstrength", required=False, help="Filter strength"
    )

    return parser


def main():
    """Run as a script with args coming from argparse."""
    parser = cmdLineParse()
    inps = parser.parse_args()
    gf = asf.load_inventory(inps.inventory)

    if inps.template:
        print(f"Reading from template file: {inps.template}...")
        inputDict = dice.read_yaml_template(inps.template)
    else:
        inputDict = {
            "topsinsar": {
                "sensorname": "SENTINEL1",
                "master": {"safe": ""},
                "slave": {"safe": ""},
            }
        }

    intdir = "int-{0}-{1}".format(inps.master, inps.slave)
    if not os.path.isdir(intdir):
        os.mkdir(intdir)
    os.chdir(intdir)

    master_urls = asf.get_slc_urls(gf, inps.master, inps.path)
    slave_urls = asf.get_slc_urls(gf, inps.slave, inps.path)
    downloadList = master_urls + slave_urls
    inps.master_scenes = [os.path.basename(x) for x in master_urls]
    inps.slave_scenes = [os.path.basename(x) for x in slave_urls]

    if inps.poeorb:
        try:
            frame = os.path.basename(inps.master_scenes[0])
            downloadList.append(asf.get_orbit_url(frame))
            frame = os.path.basename(inps.slave_scenes[0])
            downloadList.append(asf.get_orbit_url(frame))
        except Exception as e:
            print("Trouble downloading POEORB... maybe scene is too recent?")
            print("Falling back to using header orbits")
            print(e)
            inps.poeorb = False
            pass

    # Update input dictionary with argparse inputs
    inputDict["topsinsar"]["master"]["safe"] = inps.master_scenes
    inputDict["topsinsar"]["master"]["output directory"] = "masterdir"
    inputDict["topsinsar"]["slave"]["safe"] = inps.slave_scenes
    inputDict["topsinsar"]["slave"]["output directory"] = "slavedir"
    # Optional inputs
    # swaths, poeorb, dem, roi, gbox, alooks, rlooks, filtstrength
    if inps.swaths:
        inputDict["topsinsar"]["swaths"] = inps.swaths
    if inps.dem:
        inputDict["topsinsar"]["demfilename"] = inps.dem
    if inps.roi:
        inputDict["topsinsar"]["regionofinterest"] = inps.roi
    if inps.gbox:
        inputDict["topsinsar"]["geocodeboundingbox"] = inps.gbox
    if inps.filtstrength:
        inputDict["topsinsar"]["filterstrength"] = inps.filtstrength
    if inps.alooks:
        inputDict["topsinsar"]["azimuthlooks"] = inps.alooks
    if inps.rlooks:
        inputDict["topsinsar"]["rangelooks"] = inps.rlooks
    print(inputDict)
    xml = dice.dict2xml(inputDict)
    dice.write_xml(xml)
    # Create a download file
    asf.write_download_urls(downloadList)
    print(f"Generated download-links.txt and topsApp.xml in {intdir}")


if __name__ == "__main__":
    main()

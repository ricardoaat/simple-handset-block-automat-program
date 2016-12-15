#!/usr/bin/env python
""" Query and blocks Imei using handset db detection_list """
import logging
import os
from modules.Colors import Colors
from modules.Util import logconsole

from modules.Querydb import Querydb
from modules.HandsetStatus import HandsetStatus
from modules.ForceImei import ForceImei
from modules.BlockHandset import BlockHadset

from config import LOG_ROUTE, IMEI_ROUTE, REGIS_ONLY_FILE


def imeifileload():
    """ Opens the imei file generated
        from the database """
    if os.path.isfile(IMEI_ROUTE):
        print "File FOUND " + IMEI_ROUTE
    else:
        print "File " + IMEI_ROUTE + " not found, make sure it does exist dude"
        quit()


    return open(IMEI_ROUTE, "rb")


def compiledfileload():
    """ Opens the compiled imei file regonly """
    if os.path.isfile(REGIS_ONLY_FILE):
        print "File FOUND " + REGIS_ONLY_FILE
    else:
        print "File " + REGIS_ONLY_FILE + " not found, make sure it does exist dude"
        quit()


    return open(REGIS_ONLY_FILE, "rb")



def main():
    """ Main function """
    issuccess = True
    logging.basicConfig(filename=LOG_ROUTE, level=logging.DEBUG)

    if os.path.isfile(LOG_ROUTE):
        with open(LOG_ROUTE, 'w'):
            pass

    logconsole("************** Init Program **************", "i")


    if querydb():
        print Colors.OKGREEN + "Querydb status true" + Colors.ENDC
    else:
        issuccess = False

    imeifile = imeifileload()


    if issuccess:
        if handsetstatus(imeifile):
            print Colors.OKGREEN + "Handset status true" + Colors.ENDC
        else:
            issuccess = False
            print  Colors.FAIL + "Handset status FALSE" + Colors.ENDC
        imeifile.close()


    compiledfile = compiledfileload()
    if issuccess:
        if forceimei(compiledfile):
            print Colors.OKGREEN + "Force IMEI status true" + Colors.ENDC
        else:
            issuccess = False
            print  Colors.FAIL + "Force IMEI status FALSE" + Colors.ENDC
    compiledfile.close()


    compiledfile = compiledfileload()
    if issuccess:
        if blockhandset(compiledfile):
            print Colors.OKGREEN + "BLOCKHANDSET status true" + Colors.ENDC
        else:
            issuccess = False
            print  Colors.FAIL + "BLOCKHANDSET status FALSE" + Colors.ENDC

    compiledfile.close()



def querydb():
    """
    Query the Detection list table from Handset DB
    in order to list the imei to block
     """
    logconsole(Colors.OKGREEN + " -----------DATABASE QUERY FILE GEN----------- " +
               Colors.ENDC, "i")
    querydatab = Querydb()


    return querydatab.run()


def handsetstatus(imeifile):
    """ Handset validation call """
    logconsole(Colors.OKGREEN + " -----------HANDSET VALIDATION FILE GEN----------- " +
               Colors.ENDC, "i")
    hadstatus = HandsetStatus()


    return hadstatus.run(imeifile)


def forceimei(compiledfile):
    """ Force Imei """
    logconsole(Colors.OKGREEN + " -----------FORCE IMEI SERVICE----------- " +
               Colors.ENDC, "i")
    forceimeiob = ForceImei()


    return forceimeiob.run(compiledfile)


def blockhandset(compiledfile):
    """ Force Imei """
    logconsole(Colors.OKGREEN + " -----------Block Handset Service----------- " +
               Colors.ENDC, "i")
    blckhandset = BlockHadset()


    return blckhandset.run(compiledfile)


if __name__ == '__main__':
    main()

""" Query giving an imei msisdni file """
import csv
import re
import os.path
from modules.SoapService import shootsoap
from modules.Util import logconsole
from modules.Constants import Constants
from config import SERVICE_ACTION_MANAGEMENT, REGIS_ONLY_FILE

class HandsetStatus(object):
    """ Query giving an imei msisdni file """

    def buildmessage(self, imei):
        """ Builds the soap request """

        body = Constants.HANDSETSTATUSSOAP.format(imei=imei)


        return body


    def logresponse(self, response, imei):
        """ Prints the response on the log """
        issuccess = True
        imeidata = "Imei " + imei
        status = "not know"
        logconsole(response, "i")

        result_search = re.search('<imei>(.+?)</imei>', response)
        if result_search:
            response_code = result_search.group(1)
            res_code = "Imei " + response_code + " " + imeidata
            logconsole("Resp code" + res_code, "i")
        else:
            notfound = "<imei> not found"
            logconsole(notfound, "e")
            issuccess = False

        result_search = re.search('<status>(.+?)</status>', response)
        if result_search:
            status = result_search.group(1)
            logconsole("Status: " + status, "i")
        else:
            notfound = "<status> not found"
            logconsole(notfound, "e")
            issuccess = False


        return issuccess, status


    def run(self, imeifile):
        """ Loads imei file """
        if os.path.isfile(REGIS_ONLY_FILE):
            with open(REGIS_ONLY_FILE, 'w'):
                pass
        comp_file_reg = open(REGIS_ONLY_FILE, "w")

        imei_file = imeifile
        reader = csv.reader(imei_file)

        total = 0
        row = 0
        errorcount = 0
        status = ""
        registeredtoothercounter = 0
        blacklistedcounter = 0
        othercounter = 0
        registeredcounter = 0

        for row in reader:

            imei = row[0]
            logconsole("HANDSETSTATUS: Calling service with: ", "i")
            logconsole("Imei " + imei, "i")

            body = self.buildmessage(imei)
            response = shootsoap(body, SERVICE_ACTION_MANAGEMENT)

            issuccess, status = self.logresponse(response, imei)

            if not issuccess:
                errorcount += 1

            if status == "REGISTERED_TO_OTHER":
                registeredtoothercounter += 1
                if row[4] == "INVALID_IMEI":
                    comp_file_reg.write(",".join(row) + "\n")
            elif status == "BLACKLISTED":
                blacklistedcounter += 1
            elif status == "UNREGISTERED":
                print row
                comp_file_reg.write(",".join(row) + "\n")
                registeredcounter += 1
            else:
                logconsole("UNKNOWN STATUS. CHECK IT DUDE", "e")
                othercounter += 1

            total += 1
            logconsole("********************************************************************", "i")

        finishmsg = ("Finished with " + str(errorcount) + " errors \n" +
                     "REGISTERED_TO_OTHER: " + str(registeredtoothercounter) +
                     " | BLACKLISTED: " + str(blacklistedcounter) +
                     " | UNREGISTERED: " + str(registeredcounter) +
                     " | OTHER: " + str(othercounter))
        logconsole(finishmsg, "i")
        comp_file_reg.close()

        if errorcount == 0:
            return True
        else:
            return False

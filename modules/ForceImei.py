
""" Forces Imei giving an imei file """
import csv
import re
from modules.SoapService import shootsoap
from modules.Util import logconsole
from modules.Constants import Constants
from config import SERVICE_ACTION_MANAGEMENT

class ForceImei(object):
    """ Forces Imei giving an imei file """

    def buildmessage(self, imei, msisdn):
        """ Builds the soap request """

        body = Constants.FORCEIMEISOAP.format(msisdn=msisdn,
                                              imei=imei)


        return body

    def logresponse(self, response, imei, msisdn):
        """ Prints the response on the log """
        isforced = True
        imeidata = "Imei " + imei + " Msisdn " + msisdn
        logconsole(response, "i")

        result_search = re.search('<responseCode>(.+?)</responseCode>', response)
        if result_search:
            response_code = result_search.group(1)
            res_code = "Code " + response_code + " " + imeidata
            logconsole("Resp code" + res_code, "i")
            if response_code != '0':
                logconsole(res_code, "e")
                isforced = False
        else:
            notfound = "<responseCode> not found"
            logconsole(notfound, "e")


        return isforced


    def run(self, imeifile):
        """ Loads imei file """
        imei_file = imeifile
        reader = csv.reader(imei_file)

        row = 0
        errorcount = 0
        total = 0

        for row in reader:

            imei = row[0]
            msisdn = row[2]

            logconsole("ForceImei: Calling service with: ", "i")
            logconsole("Imei " + imei +
                       " Msisdn " + msisdn, "i")

            body = self.buildmessage(imei, msisdn)

            response = shootsoap(body, SERVICE_ACTION_MANAGEMENT)
            if not self.logresponse(response, imei, msisdn):
                errorcount += 1

            total += 1

            logconsole("********************************************************************", "i")

        finishmsg = "Finished with " + str(errorcount) + " errors / " + str(total)

        logconsole(finishmsg, "i")

        if errorcount == 0:
            return True
        else:
            return False

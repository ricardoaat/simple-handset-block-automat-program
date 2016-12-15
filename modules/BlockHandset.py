""" Blocks Imei giving an imei msisdni file """
import csv
import re
import datetime
from modules.SoapService import shootsoap
from modules.Util import logconsole
from modules.Constants import Constants
from config import SERVICE_ACTION_HANDSET

class BlockHadset(object):
    """ Blocks Imei giving an imei msisdni file """

    def buildmessage(self, imei, msisdn, reporttype):
        """ Builds the soap request """
        now = datetime.datetime.today()
        now = now.strftime("%Y-%m-%dT%H:%M:%S")

        body = Constants.BLOCKHANDSETSOAP.format(msisdn=msisdn,
                                                 imei=imei,
                                                 reporttype=reporttype,
                                                 now=now)


        return body


    def logresponse(self, response, imei, msisdn):
        """ Prints the response on the log """
        imeidata = "Imei " + imei + " Msisdn " + msisdn
        isblocked = True
        logconsole(response, "i")

        result_search = re.search('<responseCode>(.+?)</responseCode>', response)
        if result_search:
            response_code = result_search.group(1)
            res_code = "Code " + response_code + " " + imeidata
            logconsole("Resp code" + res_code, "i")
            if response_code != '0':
                logconsole(res_code, "e")
                isblocked = False
        else:
            notfound = "<responseCode> not found"
            logconsole(notfound, "e")

        result_search = re.search('<responseDetail>(.+?)</responseDetail>', response)
        if result_search:
            response_detail = result_search.group(1)
            logconsole("Response Detail: " + response_detail, "i")
        else:
            notfound = "<responseDetail> not found"
            logconsole(notfound, "e")

        return isblocked


    def run(self, compiledfile):
        """ Loads imei file """
        compiled_file = compiledfile
        reader = csv.reader(compiled_file)

        row = 0
        errorcount = 0
        total = 0

        for row in reader:
            reporttype = ""
            imei = row[0]
            msisdn = row[2]
            date = row[5]

            if row[4] == "UNREGISTERED_IMEI":
                reporttype = "AUTOMATIC_BLOCKING_HANDSET_NOT_REGISTERED"
            elif row[4] == "INVALID_IMEI":
                reporttype = "AUTOMATIC_BLOCKING_IMEI_INVALID"

            date = re.sub(" ", "T", date)

            logconsole("BlockHadset: Calling service with: ", "i")
            logconsole("Imei " + imei +
                       " Msisdn " + msisdn +
                       " treatement " + reporttype +
                       " planbldate " + date, "i")

            body = self.buildmessage(row[0], row[2], reporttype)
            logconsole(body, "i")

            response = shootsoap(body, SERVICE_ACTION_HANDSET)
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

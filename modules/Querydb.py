""" Query giving an imei msisdni file """
import os
import datetime
import psycopg2


from modules.Util import logconsole
from modules.Constants import Constants

from config import IMEI_ROUTE
from config import HOST, PORT, DBNAME, USER, PASSWORD


class Querydb(object):
    """
    Query the Detection list table from Handset DB
    in order to list the imei to block
     """

    def buildqueries(self):
        """ Builds the queries to use on handset """
        now = datetime.datetime.today()
        yesterday = datetime.datetime.today() - datetime.timedelta(days=1)

        now = now.strftime("%Y-%m-%d")
        yesterday = yesterday.strftime("%Y-%m-%d")

        invalidimeiquery = Constants.INVALIDIMEIQUERY.format(now=now, yesterday=yesterday)

        unregimeiquery = Constants.UNREGISIMEIQUERY.format(now=now, yesterday=yesterday)


        return invalidimeiquery, unregimeiquery


    def run(self):
        """ Write line """
        if os.path.isfile(IMEI_ROUTE):
            with open(IMEI_ROUTE, 'w'):
                pass
        db_query_fout = open(IMEI_ROUTE, "w")

        invalidimeiquery, unregimeiquery = self.buildqueries()

        total = 0
        isnotempty = False
        print invalidimeiquery
        try:
            conn = psycopg2.connect(host=HOST,
                                    port=PORT,
                                    dbname=DBNAME,
                                    user=USER,
                                    password=PASSWORD)
            cur = conn.cursor()

            cur.execute(invalidimeiquery)

            if cur.rowcount:
                rows = cur.fetchall()
                for row in rows:
                    total += 1
                    db_query_fout.write(",".join([str(col) for col in row]) + "\n")
                isnotempty = True
            else:
                logconsole("Invalid imei query 0 data", "i")

            cur.execute(unregimeiquery)
            if cur.rowcount:
                rows = cur.fetchall()
                for row in rows:
                    total += 1
                    db_query_fout.write(",".join([str(col) for col in row]) + "\n")
                isnotempty = True
            else:
                logconsole("unregistered imei query 0 data", "i")

            logconsole("Finished creating file with " +
                       str(total) + " entries", "i")


            return isnotempty



        except psycopg2.DatabaseError, error:
            print "Can't connect to handset bruh %s" % error
            logconsole("Can't connect to handset bruh %s" % error, "e")


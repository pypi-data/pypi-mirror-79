
import requests
import time
import argparse
import sys
from requests.exceptions import RequestException, Timeout, TooManyRedirects
import re


class BitcoinNotification:
    def __init__(self, Bitcoin_Api_URL, Webhooks_URL):
        self.Bitcoin_Api_URL = Bitcoin_Api_URL
        self.Webhooks_URL = Webhooks_URL

    def getBitcoinPrice(self):

        try:
            api_url = self.Bitcoin_Api_URL
            # Api calling for bitcoin prices in INR
            response = requests.get(api_url)
            json_response = response.json()
            currentBitcoinPrice = json_response['bpi']['INR']['rate_float']
        # print cutomized msg if there is no internet access
        except RequestException:
            print(' NO Internet!')
            print('Please check your Internet'
                  ' connection and run program again.')
            sys.exit()
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
        # returning bitcoin price
        return round(currentBitcoinPrice, 2)

    def postWebhooks(self, event, value):

        ifttt_event_url = self.Webhooks_URL.format(event)
        requests.post(ifttt_event_url, json=value)

    def sendIFTTTEmergencyNotificaton(self, time_interval):

        try:
            while True:
                price = self.getBitcoinPrice()
                value = {'value1': price}
                self.postWebhooks('bitcoin_price_emergency', value)
                print("Emergency notification sent")
                time.sleep(float(time_interval[0]) * 60)

        except KeyboardInterrupt:
            print('Exiting from this application, Please wait.....')
            time.sleep(5)
            print('ThankYou for using this Application')

    def sendTelegramNotificaton(self, time_interval):

        try:
            while True:
                price = self.getBitcoinPrice()
                value = {'value1': price}
                self.postWebhooks('bitcoin_price_update', value)
                print("Telegram Notification sent")
                time.sleep(float(time_interval[0]) * 60)

        except KeyboardInterrupt:
            print('Exiting from this application, Please wait.....')
            time.sleep(5)
            print('ThankYou for using this Application')

    def sendGmailNotification(self, time_interval):

        try:
            while True:
                regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
                name = input('Please enter your name: ')
                email = input('Please enter your Email: ')
                # chceking email is valid
                if(re.search(regex, email)):
                    price = self.getBitcoinPrice()
                    value = {'value1': email, 'value2': name, 'value3': price}
                    self.postWebhooks('email_bitcoin_notification', value)
                    print('Email notification sent')
                    time.sleep(float(time_interval[0]) * 60)
                else:
                    print('Invalid Email ,'+name)
                    print('Please re-run the program and provide valid email')
                    sys.exit()

        except KeyboardInterrupt:
            print('Exiting from this application, Please wait.....')
            time.sleep(5)
            print('ThankYou for using this Application')


def main():

    Bitcoin_Api_URL = 'https://api.coindesk.com/v1/bpi/currentprice/INR.json'
    # for bitcoin.notificaion123@gmail.com
    Webhooks_URL = 'https://maker.ifttt.com/trigger/{}/with/key/jrvNIRNL-vboEF2g3mcaDoUitHgy-Z180veQ4JkbYNf'

    b1 = BitcoinNotification(Bitcoin_Api_URL, Webhooks_URL)
    current_bitcoinprice = b1.getBitcoinPrice()
    parser = argparse.ArgumentParser(
        usage='''\
            Usage: This app gives the price of 1 Bitcoin in INR.
            Destination(-d) must be provided else destination will be
            telegram by default.
            To recive notification from IFTTT install IFTTT mobile app.
            To recive notifications on Telegram install Telegram app
            and join this channel @IFTTT.

            Prerequisite : INSTALL IFTTT APP AND TELEGRAM APP
            and TO RECIVE NOTIFICATON.
            PRESS Ctrl+C to terminate the app
        ''',
        description="BITCOIN PRICE NOTIFIER ",
        epilog="Copyright @Rajat Bhatt")
    # command line variable for time gap
    parser.add_argument(
        "-i",
        "--interval",
        type=int,
        nargs=1,
        metavar="interval",
        default=[1],
        help="Time interval in minutes")
    # command line variable for threshold
    parser.add_argument(
        "-t",
        "--threshold",
        type=int,
        nargs=1,
        metavar="threshold",
        default=[400000],
        help="Threshold in INR(₹)")

    # command line variable for destination
    parser.add_argument(
        "-d",
        "--destination",
        metavar='destnation',
        default='telegram',
        help='There are various options to recive notifications'
        'from us (1)IFTTT app (2) Telegram app (3) Email')

    new_args = parser.parse_args()
    print('Running Application with time interval of ', new_args.interval[0],
          'mins and threshold = ₹', new_args.threshold[0], 'and Destination= ',
          new_args.destination)

    # calls the function to send notifications
    if (new_args.destination == 'telegram' and
            new_args.threshold[0] < current_bitcoinprice):
        print('''\
            To recive the notification
        from Telegram, install the telegram app and join the
        channel using this link - https://t.me/bitcoin_notificationrajat or
        follow @Bitcoinprice_notificationrajat
        ''')
        b1.sendTelegramNotificaton(new_args.interval)

    if (new_args.destination == 'ifttt' or
            new_args.threshold[0] > current_bitcoinprice):

        b1.sendIFTTTEmergencyNotificaton(new_args.interval)

    if (new_args.destination == 'email'):
        b1.sendGmailNotification(new_args.interval)


# driver code
if __name__ == "__main__":
    main()

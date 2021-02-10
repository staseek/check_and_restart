#!/usr/bin/python3
"""
Module with simple checking something, sleep and do something if check fails.
"""
import logging
from subprocess import call
import time
import requests

FORMAT = '%(asctime)s %(levelname)s %(threadName)s %(name)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

# 1 minute
SLEEP_MIN_TIME = 60
# 10 minute 
SLEEP_MAX_TIME = 10 * 60

def check_my_ip_is(ip=YOUR_IP_HERE):
    """
    Function checking external ip address for ip.
    Default use - check vpn is on and connection works fine.
    """
    try:
        logging.info('starting check')
        return ip == requests.get('https://api.myip.com', timeout=(5.0, 5.0)).json()['ip']
    except Exception as exc:
        logging.exception(exc)
        return False

def nothing():
    """ Function with doing nothing :) """
    logging.debug('i\'m doing nothing')

def restart_vpnclient():
    """ Restarting systemd service vpnclient """
    logging.debug('restarting pihole')
    #call(["docker-compose", "-f", "/home/pi/pihole/docker-compose.yml", "stop"])
    #time.sleep(3)
    #call(["bash -c \"yes | docker system prune \""])
    #logging.debug('docker stopped and pruned')
    call(["/usr/bin/systemctl restart vpnclient.service"], shell=True)
    logging.debug('vpnclient restarted')
    #time.sleep(30)
    #call(["docker-compose", "-f", "/home/pi/pihole/docker-compose.yml", "start"])
    #logging.debug('started pihole back')

def main(check_action=check_my_ip_is, action_on_success=nothing, action_on_failure=restart_vpnclient):
    """
    Main function
    """
    previous_result = None
    current_sleep_value = SLEEP_MIN_TIME
    while True:
        current_result = check_action()
        logging.info('current check returns {}'.format(current_result))
        _ = action_on_success() if current_result else action_on_failure()
        current_sleep_value = min(SLEEP_MAX_TIME, current_result + 60.0) if previous_result == current_result else SLEEP_MIN_TIME
        time.sleep(current_sleep_value)
        
if __name__ == "__main__":
    main()


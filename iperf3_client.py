#
# Periodic iperf3 client, and REST API for access to results
#
# Written by Glen Darling, December 2018.
# Copyright 2018, Glen Darling; all rights reserved.
#

from flask import Flask
import json
import re
import subprocess
import threading
import time

# iperf3 server details
IPERF3_ADDRESS = '192.168.123.6'
IPERF3_PORT = 5862
IPERF3_BINARY = '/usr/local/bin/iperf3'
IPERF3_COMMAND = IPERF3_BINARY + ' -c ' + IPERF3_ADDRESS + ' -p ' + str(IPERF3_PORT) + ' -O 5 -J'
iperf3_results = None

# How long to pause between iperf3 network stress tests
SECONDS_BETWEEN_TESTS = (0.10 * 60)

# REST API details
REST_API_BIND_ADDRESS = '0.0.0.0'
REST_API_PORT = 5659
REST_API_VERSION = "1.0"
webapp = Flask('iperf3_client')

# Network stress test thread
class Iperf3ClientThread(threading.Thread):
  def run(self):
    global iperf3_results
    #print("\nIperf3 client thread started!")
    t = 1
    while True:
      #print("\n\nStarting iperf3 test #" + str(t) + "...\n")
      t += 1
      #print("Command: " + IPERF3_COMMAND)
      results = subprocess.run(['/bin/sh', '-c', IPERF3_COMMAND], check=True, stdout=subprocess.PIPE).stdout
      iperf3_results = results.decode('UTF-8')
      #print(iperf3_results)
      time.sleep(SECONDS_BETWEEN_TESTS)

# A web server to make the network stress test results available locally
@webapp.route("/v1/performance")
def get_performance():
  if None == iperf3_results:
    return '{"error": "no data yet"}\n'
  else:
    return iperf3_results + '\n'

# Main program (to instantiate and start the 3 threads)
if __name__ == '__main__':
  tester = Iperf3ClientThread()
  tester.start()
  webapp.run(host=REST_API_BIND_ADDRESS, port=REST_API_PORT)


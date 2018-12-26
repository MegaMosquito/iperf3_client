FROM ubuntu
WORKDIR /usr/src/app

# Install build tools, etc.
RUN apt-get update && apt-get install -y build-essential python3 wget curl jq vim python3-pip

# Build and install iperf3 (and fixup library paths)
RUN wget https://downloads.es.net/pub/iperf/iperf-3.6.tar.gz
RUN tar -xvf iperf-3.6.tar.gz
RUN cd iperf-3.6; ./configure; make; make install
RUN ldconfig

# Install Flsk for the REST API server
RUN pip3 install flask

# Copy the code
COPY ./iperf3_client.py .

# Run the daemon
CMD python3 iperf3_client.py


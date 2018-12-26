# iperf3 Client and REST API
  
This container periodically runs an `iperf3` client.  See https://github.com/esnet/iperf for details. The client needs to connect to an `iperf3` somewhere else on the local area network. The `iperf3` client data is cachedand made available from a REST API, bound to all interfaces on port 5659.  You can reach the API with a command like this:

```
curl -s localhost:5659/v1/performance | jq .end
```

The data returned by the API is exactly that provided by `iperf3` with the `-J` argument (for JSON output).


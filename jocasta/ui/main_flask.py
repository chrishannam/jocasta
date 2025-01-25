from influxdb_client import InfluxDBClient
from flask import Flask, render_template, request, redirect, url_for
from pathlib import Path
from tapo import ApiClient
import asyncio


COST_PER_KWH = 0.24
app = Flask(__name__)


def get_latest():
    # Configuration variables
    url = "http://localhost:8086"  # Replace with your InfluxDB URL
    token = "C5S8MYBsMqMPJzwprQVbCigBxsut-cVBYuSXyemw_XbP5NWjH4HM03l8I15j1sBx24vLuUXJGsfDBjOe6zQGpQ=="       # Replace with your InfluxDB token
    org = "Home"       # Replace with your InfluxDB organization
    bucket = "sensors"          # Replace with your InfluxDB bucket
    measurement = "your_measurement"  # Replace with your measurement name

    # Initialize the InfluxDB client
    client = InfluxDBClient(url=url, token=token, org=org)

    # Query the latest value
    query = f"""
    from(bucket: "{bucket}")
        |> range(start: -1h)
        |> filter(fn: (r) => r["reading"] == "temperature" or r["reading"] == "light" or r["reading"] == "humidity")
        |> sort(columns: ["_time"], desc: true)
        |> last()
    """

    tables = client.query_api().query(query)

    # Print the latest value
    readings = {}
    for table in tables:
        for record in table.records:
            readings[record['reading']] = record.get_value()

    # Close the client
    client.close()
    return readings


@app.route('/')
async def index():
    
    # Query the latest value
    readings = get_latest()
    client = ApiClient(TAPO_USERNAME, TAPO_PASSWORD)
    plug = await client.p110(TAPO_IP)

    current_state = await plug.get_device_info()
    device_on = current_state.device_on

    energy = await plug.get_energy_usage()
    cost = round(energy.month_energy * COST_PER_KWH/1000, 2)
    return render_template('index_latest.html', data=readings, device_on=device_on, monthly_cost=cost)


TAPO_IP = '192.168.0.60'
TAPO_USERNAME = 'bassdread@gmail.com'
TAPO_PASSWORD = '2uPJ+E8gd#3xgC7'

# Handle the toggle plug request
@app.route('/toggle_plug', methods=['POST'])
async def toggle_plug():
    
    client = ApiClient(TAPO_USERNAME, TAPO_PASSWORD)
    plug = await client.p110(TAPO_IP)
    current_state = await plug.get_device_info()
    # Toggle the state
    if current_state.device_on:
        await plug.off()
    else:
        await plug.on()

    # Redirect back to the main page
    return redirect(url_for('index'))

if __name__ == '__main__':
    asyncio.run(app.run(debug=True, host='0.0.0.0',  port=8081))

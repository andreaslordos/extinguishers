To add a new country, create a new folder with a similar structure to the "cyprus" folder. 

For fires specifically, find NASA satellite data on your specified country [via this website](https://firms.modaps.eosdis.nasa.gov/download/create.php). Download it in JSON format and include it in the emergencies folder. Then in `src/main.py`, specify country by changing the COUNTRY variable (e.g. COUNTRY='wakanda'). Include a list of lat/longs of current ERC's in the hubs folder in .txt format.

For other types of emergencies (e.g. medical), follow the same format with the hubs folder, and create your own type of node in the src/nodes folder (e.g. MedicalNode)

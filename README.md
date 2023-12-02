# Experimental GPU miner for Ocvcoin

## IT CAN ONLY RUN EFFICIENTLY ON NVIDIA GPUs YET!!!

### Usage on Windows

- Download & Install Python 3.6.0: <https://raw.githubusercontent.com/ocvcoin/gpuminer/main/python_download_links.txt>

- Download & Extract zip file: <https://github.com/ocvcoin/gpuminer/archive/refs/heads/main.zip>

- Right Click & Open `start_mining.cmd`


### Usage on Ubuntu, MacOS

- Just run following command:

```
curl -o ~/run.sh https://raw.githubusercontent.com/ocvcoin/gpuminer/main/run.sh || wget -O ~/run.sh https://raw.githubusercontent.com/ocvcoin/gpuminer/main/run.sh && sudo bash ~/run.sh ___ADD_YOUR_OCVCOIN_ADDRESS_HERE___
```

dont forget to change: `___ADD_YOUR_OCVCOIN_ADDRESS_HERE___`

### Usage on HiveOS

- Download json: <https://github.com/ocvcoin/hiveos_gpuminer/releases/download/v1.0.0.0/ocvcoin-gpuminer.flight-sheet.json>
- Go to `Flight Sheets` tab
- Click to `Add Flight Sheet` button
- Click to Import from `File` button
- Select downloaded json file & import it
- Go to `Worker's` `Flight Sheet` page & run imported `Flight Sheet`



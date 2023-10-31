# Experimental GPU miner for Ocvcoin


### Usage on Windows

- Download & Unzip: <https://github.com/ocvcoin/gpuminer/archive/refs/heads/main.zip>

- Read the instructions in `python_download_links.txt` & install python 3.6.0

- Run `start_mining.cmd`


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



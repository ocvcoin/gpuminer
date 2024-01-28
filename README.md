# Experimental GPU miner for Ocvcoin

## IT CAN ONLY RUN EFFICIENTLY ON NVIDIA GPUs YET!!!

### Mining on Windows

- Download and Install Python 3.6.0: <https://raw.githubusercontent.com/ocvcoin/gpuminer/main/python_download_links.txt>

- Download and Extract zip file: <https://github.com/ocvcoin/gpuminer/archive/refs/heads/main.zip>

- Double Click `start_mining.cmd`


### Mining on Ubuntu, Debian, MacOS

- Run following command:

```
curl -o ~/run.sh https://raw.githubusercontent.com/ocvcoin/gpuminer/main/run.sh || wget -O ~/run.sh https://raw.githubusercontent.com/ocvcoin/gpuminer/main/run.sh && sudo bash ~/run.sh ___ADD_YOUR_OCVCOIN_ADDRESS_HERE___
```

### Mining on HiveOS

- Download Flight Sheet: <https://github.com/ocvcoin/hiveos_gpuminer/releases/download/v1.0.0.0/ocvcoin-gpuminer.flight-sheet.json>
- Go to `Flight Sheets` tab
- Click to `Add Flight Sheet` button
- Click to Import from `File` button and import `ocvcoin-gpuminer.flight-sheet.json` 
- Select or Add a wallet
- Click `Create Flight Sheet` button
- Go to Worker's `Flight Sheet` tab and run created Flight Sheet



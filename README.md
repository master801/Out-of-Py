# Out-of-Py


## Info

This tool is for decoding and encoding the text `.lua` and `.bin` files in Mahouka Koukou no Rettousei Out of Order for PS Vita.

Please give credit if using this tool.


## Before using:

Install [Python](https://www.python.org/downloads/) ([3.12.0](https://www.python.org/downloads/release/python-3120/))</br>

Install dependencies:
- [kaitaistruct](https://pypi.org/project/kaitaistruct/)</br>
- [py-lua-parser](https://github.com/boolangery/py-lua-parser)</br>

OR

Install dependencies using `pip`
```shell
py -3.12 -m pip install -r requirements.txt
```



## Usage

#### Arguments:
- `--mode` [`DECODE`, `ENCODE`] - Mode to use
- `--input` [`INPUT_DIRECTORY`] - Input directory
- `--output` [`OUTPUT_DIRECTORY`] - Output directory
- `--threads` [`THREADS`] - Amount of threads to use for processing files. Default is 1
- `--overwrite` - If files in output directory should be overwritten if it already exists.

#### Example usage:
```
py -3.12 main.py --mode=DECODE --input=INPUT_DIR --output=OUTPUT_DIR
py -3.12 main.py --mode=DECODE --input=INPUT_DIR --output=OUTPUT_DIR --threads=4 --overwrite
```

### Currently Supports:

- [x] Graph2D/TuneData/IMH_Tuning_List_X_XX.bin
- [x] Graph2D/Tutorial/TutorialList.bin
- [x] Param/Atk/CadParam.bin
- [x] Param/Atk/CadTextParam.bin
- [x] Param/Atk/CharMenuParam.bin
- [x] Param/Atk/MagicParam.bin
- [x] Param/Atk/MagicText.bin

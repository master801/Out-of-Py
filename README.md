# Out-of-Py


## Info

Please give credit where it's due if using my tool.


## Before using:

Install [Python](https://www.python.org/downloads/) (project is built with [3.7.3](https://www.python.org/downloads/release/python-373/))</br>
Install [kaitaistruct](https://pypi.org/project/kaitaistruct/) running the command: `pip install kaitaistruct`</br>
Install [py-lua-parser](https://github.com/boolangery/py-lua-parser) by running the command: `pip install luaparser`</br>


## Usage

#### Arguments:
- `--mode` [`DECODE`, `ENCODE`] - Mode to use
- `--input` [`INPUT_DIRECTORY`] - Input directory
- `--output` [`OUTPUT_DIRECTORY`] - Output directory
- `--threads` [`THREADS`] - Amount of threads to use for processing files. Default is 1 - Error log will be more helpful than using more threads
- `--overwrite` [`True`, `False`] - If files in output directory should be overwritten if it already exists. Default is False.

#### Example usage:
```
python main.py --mode=DECODE --input=INPUT_DIR --output=OUTPUT_DIR
python main.py --mode=DECODE --input=INPUT_DIR --output=OUTPUT_DIR --threads=4 --overwrite=True
```

#### Tested on:
- Windows (Windows 10)
- Linux (Fedora 29)

### Currently Supports:

- [x] Graph2D/TuneData/IMH_Tuning_List_X_XX.bin
- [x] Graph2D/Tutorial/TutorialList.bin
- [x] Param/Atk/CadParam.bin
- [x] Param/Atk/CadTextParam.bin
- [x] Param/Atk/CharMenuParam.bin
- [x] Param/Atk/MagicParam.bin
- [x] Param/Atk/MagicText.bin

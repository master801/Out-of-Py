# Out-of-Py


## Before using:

Install [Python](https://www.python.org/downloads/) (project is built with [3.6.4](https://www.python.org/downloads/release/python-364/))</br>
Install [kaitaistruct](https://pypi.org/project/kaitaistruct/) running the command: `pip install kaitaistruct`</br>
Install [py-lua-parser](https://github.com/boolangery/py-lua-parser) by running the command: `pip install luaparser`</br>


## Usage

#### Arguments:
- `--mode` [`DECODE`, `ENCODE`]
- `--input` [`INPUT_DIRECTORY`]
- `--output` [`OUTPUT_DIRECTORY`]

##### Example usage:
```
python main.py --mode=DECODE --input=INPUT_DIR --output=OUTPUT_DIR
```

### Currently Supports:

- [x] IMH_Tuning_List_X_XX.bin
- [x] MagicText.bin
- [x] CadParam.bin
- [x] CadTextParam.bin
- [ ] CharMenuParam.bin
- [x] TutorialList.bin

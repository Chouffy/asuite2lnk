# asuite2lnk
Parse an ASuite database into LNK files (Windows Shortcuts), which means parsing SQLite entries into `pylnk3`.

## How to use 

1. Install [pylnk3](https://github.com/strayge/pylnk): `pip install pylnk3==0.4.2`
2. Configure the following variables:
  * `_ASUITE_SQLITE_DB`: Direct path to the ASuite database
  * `_TARGET_LNK_FOLDER `: Existing folder which will contain all LNK files
  * `_VAR_DRIVE`: Drive letter + `:` of the drive where ASuite is launched
  * `_VAR_ASUITE `: Folder from where ASuite is launched
3. Execute the script `python .\asuite2lnk.py`
4. Observe the result!
  * `"Error for title: " + lnk_title` if the LNK failed to be created
  * `"ASuite2lnk done!"` when the script is finished

Tested with ASuite 2.0.0.1422 Beta, Python 3.8.5

## Known limitations

* Cannot parse URL or folders
* Doesn't parse the "directory" tree defined in ASuite, only applications

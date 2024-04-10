# Copyright (c) 2015 Miro Mannino

import xml.etree.ElementTree as ET
import os
import sys
import biplist

# Config
iTerm_CONFIG_PATH = os.path.join(
    os.environ["HOME"], "Library", "Preferences", "com.googlecode.iterm2.plist"
)


def readITermConfig(query):
    query = query.strip()
    rE = ET.Element("items")
    if os.path.isfile(iTerm_CONFIG_PATH):
        try:
            config = biplist.readPlist(iTerm_CONFIG_PATH)

            for item in config[b"Window Arrangements"]:
                profileName = item.decode("ascii")
                if len(query) > 0 and profileName.lower().find(query.lower()) == -1:
                    continue
                iE = ET.SubElement(
                    rE,
                    "item",
                    valid="yes",
                    arg=f"arr_{profileName}",
                    autocomplete=profileName,
                )
                tE = ET.SubElement(iE, "title")
                tE.text = "New iTerm Arrangement"
                stE = ET.SubElement(iE, "subtitle")
                stE.text = profileName

            defaultBookmarkGUID = config.get(b"Default Bookmark Guid")
            for item in config[b"New Bookmarks"]:
                profileName = item.get(b"Name").decode("ascii")
                if item.get("Guid") == defaultBookmarkGUID:
                    continue
                if len(query) > 0 and profileName.lower().find(query.lower()) == -1:
                    continue
                iE = ET.SubElement(
                    rE, "item", valid="yes", arg=profileName, autocomplete=profileName
                )
                tE = ET.SubElement(iE, "title")
                tE.text = "New iTerm window"
                stE = ET.SubElement(iE, "subtitle")
                stE.text = profileName

        except Exception as e:
            # print(e)
            return None
        return rE
    else:
        return None


res = readITermConfig(sys.argv[1] if len(sys.argv) > 1 else "")
if res is not None:
    print('<?xml version="1.0"?>')
    print(ET.tostring(res).decode("ascii"))

# coding=<utf8>
# -*- coding: utf-8 -*-

import logging
adls_logger = logging.getLogger('azure.datalake.store')
adls_logger.addHandler(logging.FileHandler(filename="adls.log"))
adls_logger.setLevel(logging.DEBUG)  # DEBUG produces a lot of output.

from azure.datalake.store.exceptions import FileNotFoundError
from azure.datalake.store import core, lib


def custom_walk(adls_client, path):
    """
    Walk a path recursively and returns list of files and dirs(if parameter set)

    Parameters
    ----------
    adls_client: AzureDLFileSystem
        The ADLS client that will be used to make ls calls
    path: str or AzureDLPath
        Path to query

    Returns
    -------
    List of files and dirs
    """
    ret = list(adls_client.ls(path, detail=True))
    for item in ret:
        yield item

    current_subdirs = [f for f in ret if f['type'] != 'FILE']
    while current_subdirs:
        dirs_below_current_level = []
        for apath in current_subdirs:
            try:
                sub_elements = adls_client.ls(apath['name'], detail=True)
            except FileNotFoundError:
                # Folder may have been deleted while walk is going on. Infrequent so we can take the linear hit
                ret.remove(apath)
                continue
            if not sub_elements:
                pass
            else:
                for item in sub_elements:
                    yield item
                dirs_below_current_level.extend([f for f in sub_elements if f['type'] != 'FILE'])
        current_subdirs = dirs_below_current_level


if __name__ == '__main__':
    #token = lib.auth(username='admin@aad179.ccsctp.net', password="D@t@!@k351", tenant_id='4ca0b6b0-e97c-43bc-aa52-48f274d2cf1a', client_id='1950a258-227b-4e31-a9cf-717495945fc2')
    token = lib.auth() ## Fill this with how they acqure the token
    # ADD details on how they are using the token
    adl = core.AzureDLFileSystem(token, store_name="akharitadls", per_call_timeout_seconds=120)
    for x in adl.ls("/"):
        if "azure_python_sdk_test_" in x:
            adl.rm(x)



    exit(1)
    for x in custom_walk(adl, u'/'):
        print(x)
        ## ADD jhson code here




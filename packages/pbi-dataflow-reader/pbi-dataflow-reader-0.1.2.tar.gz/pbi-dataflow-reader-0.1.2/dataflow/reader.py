from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
import urllib.request, urllib.parse
import json
import pandas as pd

class dataflow_reader(object):

    _BLOB_URL_FORMAT = "https://{}.blob.core.windows.net/{}/{}?{}"
    _CONTAINER_URL_FORMAT = "https://{}.dfs.core.windows.net/{}/"
    _storage_account_name = ""
    _storage_account_key = ""
    _storage_account_sas = ""
    _container_name = "powerbi"
    _folder_name = ""
    _sas_permissions = None
    _expiry_in_minutes = 60

    def __init__(self, storage_account_name, storage_account_key, pbi_workspace_name, dataflow_name, expiry_in_minutes = 60):
        self._storage_account_name = storage_account_name
        self._storage_account_key = storage_account_key
        self._folder_name = "{}/{}".format(pbi_workspace_name, dataflow_name)
        # read only
        self._sas_permissions = BlobSasPermissions(read=True)
        self._expiry_in_minutes = expiry_in_minutes

    def get_blob_sas(self, blob_name):
        start_time = datetime.utcnow() - timedelta(minutes=5)
        expiration_time = datetime.utcnow() + timedelta(minutes=self._expiry_in_minutes)
        return generate_blob_sas(self._storage_account_name, 
            self._container_name, 
            blob_name, 
            account_key = self._storage_account_key, 
            expiry = expiration_time, 
            start = start_time,
            permission=self._sas_permissions)

    def get_blob_name_from_url(self, url):
        container_url = self._CONTAINER_URL_FORMAT.format(self._storage_account_name, self._container_name)
        return urllib.parse.unquote(url.replace(container_url, ""))

    def get_metadata(self, entity_name):
        blob_name = "{}/model.json".format(self._folder_name)
        blob_sas = self.get_blob_sas(blob_name)
        blob_url = self._BLOB_URL_FORMAT.format(urllib.parse.quote(self._storage_account_name), urllib.parse.quote(self._container_name), urllib.parse.quote(blob_name), blob_sas)
        data = urllib.request.urlopen(blob_url)
        return json.load(data)

    def get_entity_files(self, entity_name):
        metadata = self.get_metadata(entity_name)
        partitions = []
        for entity in metadata["entities"]:
            if entity["name"] == entity_name:
                for partition in entity["partitions"]:
                    blob_name = self.get_blob_name_from_url(partition["location"])
                    blob_sas = self.get_blob_sas(blob_name)
                    blob_url = self._BLOB_URL_FORMAT.format(urllib.parse.quote(self._storage_account_name), urllib.parse.quote(self._container_name), urllib.parse.quote(blob_name), blob_sas)
                    partitions.append(blob_url)

        return partitions


    def read_entity(self, entity_name):
        li = []
        attributes = self.get_entity_attributes(entity_name)
        names = [attr["name"] for attr in attributes]
        for file in self.get_entity_files(entity_name):
            df = pd.read_csv(file, index_col=None, header=None, names=names)
            li.append(df)

        return pd.concat(li, axis=0, ignore_index=True)


    def get_entity_attributes(self, entity_name):
        metadata = self.get_metadata(entity_name)
        for entity in metadata["entities"]:
            if entity["name"] == entity_name:
                return entity["attributes"]
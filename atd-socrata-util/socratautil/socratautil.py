"""
Helper methods for interacting with the Socrata Open Data API (SODS).

We've chosen to build our own methods rather than use [Sodapy](https://github.com/xmunoz/sodapy)
in order to handle some common ETL routines, particularly with Knack integration.
"""
import json
import os

import requests

from datautil import mills_to_unix, iso_to_unix, lower_case_keys


class Soda(object):
    """
    Class to query and publish open data via the Socrata Open Data API (SODA)
    """

    def __init__(
        self,
        auth=None,
        date_fields=None,
        host="data.austintexas.gov",
        lat_field="locaiton_latitude",
        lon_field="location_longitude",
        location_field="location",
        records=None,
        replace=False,
        resource=None,
        soql=None,
        source="knack",
    ):

        self.auth = auth
        self.date_fields = date_fields
        self.host = host
        self.lat_field = lat_field
        self.lon_field = lon_field
        self.location_field = location_field
        self.records = records
        self.replace = replace
        self.soql = soql
        self.source = source

        if not resource:
            raise Exception("Socrata resouce ID is required.")

        self.resource = resource

        self.data = None
        self.fieldnames = None
        self.metadata = None

        self.url = f"https://{self.host}/resource/{self.resource}.json"
        self.url_metadata = f"https://{self.host}/api/views/{self.resource}.json"

        self._get_metadata()
        self._get_fieldnames()
        self._get_date_fields()

        if self.records:
            self._handle_records()

        else:
            self._query()

    def _handle_records(self):

        if self.date_fields:
            if self.source == "knack":
                self.records = mills_to_unix(self.records, self.date_fields)
            elif self.source == "postgrest" or self.source == "kits":
                self.records = iso_to_unix(self.records, self.date_fields)

        self.records = lower_case_keys(self.records)

        # need to handle nulls after lowercase keys or the keys won't match the metdata
        self._handle_nulls()

        if self.location_field:
            self.records = self._location_fields()

        self.res = self._upload()
        self._handle_response()
        return self.res

    def _location_fields(self):
        """
        Create special socrata "location" field from x/y values.
        """
        for record in self.records:

            try:
                #  create location field if lat and lon are avaialble
                if record[self.lat_field] and record[self.lon_field]:
                    record[self.location_field] = "({},{})".format(
                        record[self.lat_field], record[self.lon_field]
                    )

                else:
                    record[self.location_field] = ""

            except KeyError:
                #  do not add location field if lat/lon keys are missing
                pass

        return self.records

    def _upload(self):
        if self.replace:
            res = requests.put(self.url, json=self.records, auth=self.auth)

        else:
            res = requests.post(self.url, json=self.records, auth=self.auth)

        res.raise_for_status()
        return res.json()

    def _handle_response(self):
        """
        Parse socrata API response
        """
        if "error" in self.res:
            raise Exception(self.res)

        elif self.res.get("Errors"):
            raise Exception(self.res)

        return True

    def _query(self):
        """
        Query a socrata resource. soql must be a dict formated as { $key : value }
        as defined in the SoQl spec, here: https://dev.socrata.com/docs/queries/
        """
        res = requests.get(self.url, params=self.soql)

        res.raise_for_status()
        self.data = res.json()
        return res.json()

    def _handle_nulls(self):
        # Set empty strings to None. Socrata does not allow empty strings.
        # Convert other string field objects to strings for good measure

        columns = self.metadata["columns"]
        # use this to check out field types
        # list(set([t['dataTypeName'] for t in self.metadata['columns']]))
        #  ['location', 'text', 'number']
        fields_strings = [
            column["fieldName"]
            for column in columns
            if column["dataTypeName"] == "text"
        ]

        fields_numbers = [
            column["fieldName"]
            for column in columns
            if column["dataTypeName"] == "number"
        ]

        for record in self.records:
            for key in record.keys():
                if key in fields_strings:
                    if record[key] == "":
                        # empty strings are not allowed. Set value to null.
                        record[key] = None
                        continue

                    elif record[key] is None:
                        # None will be handled by Socrata correctly as a null value
                        continue

                    else:
                        # Coerce to string.
                        record[key] = str(record[key])
                        continue

                elif key in fields_numbers:
                    # socrata will not accept an empty string for null number values
                    if record[key] == "":
                        record[key] = None

        return

    def _get_metadata(self):
        print("get socrata metadata")
        res = requests.get(self.url_metadata, auth=self.auth)
        self.metadata = res.json()

        return self.metadata

    def _get_fieldnames(self):
        self.fieldnames = [
            col["fieldName"]
            for col in self.metadata["columns"]
            if "@computed_region" not in col["fieldName"]
        ]
        return self.fieldnames

    def _get_date_fields(self):
        self.date_fields = [
            field["fieldName"]
            for field in self.metadata["columns"]
            if "date" in field["dataTypeName"]
        ]
        return self.date_fields


def prepare_deletes(records, primary_key):
    #  Format socrata payload for record deletes
    #  See: https://dev.socrata.com/docs/
    deletes = []

    for record in records:
        deletes.append({primary_key: record[primary_key], ":deleted": True})

    return deletes


def strip_geocoding(dicts):
    """
    Remove unwanted metadata from socrata location field
    """
    for record in dicts:

        try:
            location = record.get("location")
            record["location"] = {
                "latitude": location["latitude"],
                "longitutde": location["longitutde"],
            }

        except KeyError:
            continue

    return dicts

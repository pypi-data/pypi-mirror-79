#!/usr/bin/env python

import requests
import logging


class Instance:

    DATACENTERS = {
        'us-east-1': 'ash3',
        'us-west-2': 'pdx2',
        'eu-west-1': 'dub1',
        'us-east4': 'ash4',
        'us-west1': 'pdx1',
        'us-central1': 'ord1',
        'us-west1': 'pdx4',
    }

    REGIONS = {
        'ash3': 'us-east-1',
        'pdx2': 'us-west-2',
        'dub1': 'eu-west-1',
        'ash4': 'us-east4',
        'pdx1': 'us-west1',
        'ord1': 'us-central1',
        'pdx4': 'us-west1',
    }

    @staticmethod
    def get_cloud_provider(**kwargs):
        provider = ""
        if requests.get("http://169.254.169.254/").content.split("\n")[1] == "computeMetadata/":
            provider = "gcp"
        else:
            provider = "aws"
        return provider

    @staticmethod
    def get_region_by_datacenter(datacenter, *kwargs):

        return Instance.REGIONS[datacenter]

    @staticmethod
    def get_datacenter_by_region(region, *kwargs):
        return Instance.DATACENTERS[region]

# coding: utf-8

# Copyright (c) 2015, thumbor-community
# Use of this source code is governed by the MIT license that can be
# found in the LICENSE file.

import thumbor.loaders.http_loader as http_loader

from . import *
from ..aws.bucket import Bucket

from datetime import datetime


def validate(context, url, normalize_url_func=http_loader._normalize_url):
    return _validate(context, url, normalize_url_func)


def _generate_presigned_url(context, bucket, key, callback):
    """
    Generates presigned URL
    :param Context context: Thumbor's context
    :param string bucket: Bucket name
    :param string key: Path to get URL for
    :param callable callback: Callback method once done
    """
    Bucket(bucket, context.config.get('TC_AWS_REGION'),
           context.config.get('TC_AWS_ENDPOINT')).get_url(key, callback=callback)


def load(context, url, callback):
    """
    Loads image
    :param Context context: Thumbor's context
    :param string url: Path to load
    :param callable callback: Callback method once done
    """
    if _use_http_loader(context, url):
        http_loader.load_sync(context, url, callback,
                              normalize_url_func=http_loader._normalize_url)
    else:
        bucket, key, expiration = _get_bucket_and_key_and_expiration(
            context, url)

        # Check expiration date
        expirationdate = datetime.fromtimestamp(expiration)

        if expirationdate > datetime.now():
            if _validate_bucket(context, bucket):
                def on_url_generated(generated_url):
                    def noop(url):
                        return url
                    http_loader.load_sync(
                        context, generated_url, callback, normalize_url_func=noop)

                _generate_presigned_url(context, bucket, key, on_url_generated)
            else:
                callback(None)
        else:
            callback(None)

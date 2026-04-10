# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function


__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r"""
    options:
      engine_mount_point:
        type: str
        required: true
        description:
          - The path where the secret backend is mounted.
    """

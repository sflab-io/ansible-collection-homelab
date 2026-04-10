#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = r"""
module: vault_secrets_tune
version_added: 0.1.0
author:
  - Sebastian Freund(@abes140377)
short_description: Tunes configuration parameters for a HashiCorp Vault secrets engine
description:
  - >-
    L(Tunes,https://developer.hashicorp.com/vault/api-docs/system/mounts#tune-mount-configuration)
    configuration parameters for a given secrets engine mount point in HashiCorp Vault.
extends_documentation_fragment:
  - sflab.homelab.connection
  - sflab.homelab.auth
  - sflab.homelab.action_group
  - sflab.homelab.check_mode
  - sflab.homelab.engine_mount
  - sflab.homelab.requirements
options:
  description:
    type: str
    required: false
    description:
      - The description of the mount.
      - This overrides the current stored value, if any.
  default_lease_ttl:
    type: str
    required: false
    description:
      - The default time-to-live for leases.
      - This overrides the global default.
      - This value can be provided as a duration string, such as V(72h), or as a number of seconds.
      - A value of V(0) is equivalent to the system default TTL.
  max_lease_ttl:
    type: str
    required: false
    description:
      - The maximum time-to-live for leases.
      - This overrides the global default.
      - This value can be provided as a duration string, such as V(72h), or as a number of seconds.
      - A value of V(0) is equivalent to the system max TTL.
  audit_non_hmac_request_keys:
    type: list
    elements: str
    required: false
    description:
      - The list of keys that will not be HMAC'd by audit devices in the request data object.
  audit_non_hmac_response_keys:
    type: list
    elements: str
    required: false
    description:
      - The list of keys that will not be HMAC'd by audit devices in the response data object.
  listing_visibility:
    type: str
    required: false
    choices:
      - unauth
      - hidden
    description:
      - Whether to show this mount in the UI-specific listing endpoint.
      - If not set, behaves like V(hidden).
  passthrough_request_headers:
    type: list
    elements: str
    required: false
    description:
      - List of headers to allow and pass from the request to the plugin.
  allowed_response_headers:
    type: list
    elements: str
    required: false
    description:
      - List of headers to allow, allowing a plugin to include them in the response.
  allowed_managed_keys:
    type: list
    elements: str
    required: false
    description:
      - List of managed key registry entry names that the mount is allowed to access.
  plugin_version:
    type: str
    required: false
    description:
      - The semantic version of the plugin to use, e.g. V(v0.1.0).
      - Changes will not take effect until the mount is reloaded.
  delegated_auth_accessors:
    type: list
    elements: str
    required: false
    description:
      - List of allowed authentication mount accessors the backend can request delegated authentication for.
"""

EXAMPLES = r"""
- name: Tune PKI intermediate CA for ACME support
  sflab.homelab.vault_secrets_tune:
    url: https://vault:8201
    auth_method: userpass
    username: '{{ user }}'
    password: '{{ passwd }}'
    engine_mount_point: pki_int
    passthrough_request_headers:
      - If-Modified-Since
    allowed_response_headers:
      - Last-Modified
      - Location
      - Replay-Nonce
      - Link

- name: Set lease TTLs for a secrets engine
  sflab.homelab.vault_secrets_tune:
    url: https://vault:8201
    auth_method: token
    token: '{{ vault_token }}'
    engine_mount_point: secret
    default_lease_ttl: 1h
    max_lease_ttl: 24h

- name: Update description and listing visibility
  sflab.homelab.vault_secrets_tune:
    url: https://vault:8201
    auth_method: token
    token: '{{ vault_token }}'
    engine_mount_point: pki
    description: 'PKI secret engine for internal certificates'
    listing_visibility: unauth
"""

RETURN = r"""
config:
  type: dict
  returned: success
  description:
    - The current configuration of the secrets engine after tuning.
  sample:
    description: 'PKI secret engine for internal certificates'
    default_lease_ttl: 2678400
    max_lease_ttl: 2678400
    audit_non_hmac_request_keys: []
    audit_non_hmac_response_keys: []
    listing_visibility: unauth
    passthrough_request_headers:
      - If-Modified-Since
    allowed_response_headers:
      - Last-Modified
      - Location
      - Replay-Nonce
      - Link
  contains:
    description:
      type: str
      description:
        - The description of the secret engine.
    default_lease_ttl:
      type: int
      description:
        - The default lease TTL of the secret engine in seconds.
    max_lease_ttl:
      type: int
      description:
        - The maximum lease TTL of the secret engine in seconds.
    audit_non_hmac_request_keys:
      type: list
      elements: str
      description:
        - The list of non-HMAC request keys to audit.
    audit_non_hmac_response_keys:
      type: list
      elements: str
      description:
        - The list of non-HMAC response keys to audit.
    listing_visibility:
      type: str
      description:
        - The listing visibility of the secret engine.
    passthrough_request_headers:
      type: list
      elements: str
      description:
        - The list of request headers to pass through.
    allowed_response_headers:
      type: list
      elements: str
      description:
        - The list of response headers to allow.
    allowed_managed_keys:
      type: list
      elements: str
      description:
        - The list of allowed managed key registry entry names.
    plugin_version:
      type: str
      description:
        - The semantic version of the plugin.
    delegated_auth_accessors:
      type: list
      elements: str
      description:
        - The list of allowed authentication mount accessors.
prev_config:
  description:
    - The previous configuration of the secrets engine before tuning.
  type: dict
  returned: changed
  sample:
    description: 'PKI secret engine'
    default_lease_ttl: 2678400
    max_lease_ttl: 2678400
    audit_non_hmac_request_keys: []
    audit_non_hmac_response_keys: []
    listing_visibility: unauth
    passthrough_request_headers: []
    allowed_response_headers: []
  contains:
    description:
      type: str
      description:
        - The description of the secret engine.
    default_lease_ttl:
      type: int
      description:
        - The default lease TTL of the secret engine in seconds.
    max_lease_ttl:
      type: int
      description:
        - The maximum lease TTL of the secret engine in seconds.
    audit_non_hmac_request_keys:
      type: list
      elements: str
      description:
        - The list of non-HMAC request keys to audit.
    audit_non_hmac_response_keys:
      type: list
      elements: str
      description:
        - The list of non-HMAC response keys to audit.
    listing_visibility:
      type: str
      description:
        - The listing visibility of the secret engine.
    passthrough_request_headers:
      type: list
      elements: str
      description:
        - The list of request headers to pass through.
    allowed_response_headers:
      type: list
      elements: str
      description:
        - The list of response headers to allow.
    allowed_managed_keys:
      type: list
      elements: str
      description:
        - The list of allowed managed key registry entry names.
    plugin_version:
      type: str
      description:
        - The semantic version of the plugin.
    delegated_auth_accessors:
      type: list
      elements: str
      description:
        - The list of allowed authentication mount accessors.
"""

import traceback


try:
    import hvac

    from hvac.exceptions import Forbidden, InvalidRequest
except ImportError:
    HAS_HVAC = False
    HVAC_IMPORT_ERROR = traceback.format_exc()
else:
    HAS_HVAC = True
    HVAC_IMPORT_ERROR = None

from typing import List, Optional

from ansible.module_utils.basic import missing_required_lib

from ..module_utils._timeparse import duration_str_to_seconds
from ..module_utils._vault_module import VaultModule
from ..module_utils._vault_module_error import VaultModuleError


class VaultSecretsTuneModule(VaultModule):
    """
    Vault Secrets Tune module.
    """

    ARGSPEC: dict = dict(
        engine_mount_point=dict(type="str", required=True),
        description=dict(type="str", required=False),
        default_lease_ttl=dict(type="str", required=False),
        max_lease_ttl=dict(type="str", required=False),
        audit_non_hmac_request_keys=dict(type="list", elements="str", required=False),
        audit_non_hmac_response_keys=dict(type="list", elements="str", required=False),
        listing_visibility=dict(type="str", required=False, choices=["unauth", "hidden"]),
        passthrough_request_headers=dict(type="list", elements="str", required=False),
        allowed_response_headers=dict(type="list", elements="str", required=False),
        allowed_managed_keys=dict(type="list", elements="str", required=False),
        plugin_version=dict(type="str", required=False),
        delegated_auth_accessors=dict(type="list", elements="str", required=False),
    )

    DURATION_PARAMS: List[str] = ["default_lease_ttl", "max_lease_ttl"]

    LIST_PARAMS: List[str] = [
        "audit_non_hmac_request_keys",
        "audit_non_hmac_response_keys",
        "passthrough_request_headers",
        "allowed_response_headers",
        "allowed_managed_keys",
        "delegated_auth_accessors",
    ]

    def __init__(self, *args, **kwargs) -> None:
        argspec: dict = self.ARGSPEC.copy()

        super(VaultSecretsTuneModule, self).__init__(
            *args,
            argument_spec=argspec,
            supports_check_mode=True,
            **kwargs,
        )

    def get_defined_tune_params(self) -> dict:
        """
        Get the defined tune parameters.

        Returns:
            dict: The defined tune parameters.
        """

        filtered_params: dict = {}

        for key in self.ARGSPEC.keys():
            if key == "engine_mount_point":
                continue

            if self.params[key] is not None:
                if key in self.DURATION_PARAMS:
                    filtered_params[key] = duration_str_to_seconds(self.params[key])
                else:
                    filtered_params[key] = self.params[key]

        return filtered_params

    def format_config_data(self, config_data: dict) -> dict:
        """
        Format the configuration data for a secrets engine.

        Args:
            config_data (dict): The configuration data to format.

        Returns:
            dict: The formatted configuration data.
        """

        formatted_data: dict = {}

        for key, value in config_data.items():
            if key != "options":
                formatted_data[key] = value

        return formatted_data

    def get_current_config(self) -> dict:
        """
        Get the current configuration of the secrets engine.

        Returns:
            dict: The current configuration of the secrets engine.
        """

        path: str = self.params["engine_mount_point"]

        try:
            config: dict = self.client.sys.read_mount_configuration(path=path)
        except InvalidRequest:
            self.handle_error(
                VaultModuleError(
                    message=f"Invalid request: Secrets engine not found at path '{path}'",
                    exception=traceback.format_exc(),
                ),
            )
        except Forbidden:
            self.handle_error(
                VaultModuleError(
                    message=f"Forbidden: Permission denied to read mount configuration at path '{path}'",
                    exception=traceback.format_exc(),
                ),
            )
        except Exception:
            self.handle_error(
                VaultModuleError(
                    message=f"Error reading mount configuration at path '{path}'",
                    exception=traceback.format_exc(),
                ),
            )

        config_data: dict = config.get("data", {})
        formatted_config: dict = self.format_config_data(config_data)

        return formatted_config

    def compare_config(self, previous_config: dict, desired_config: dict) -> dict:
        """
        Compare the previous and desired configurations.

        Args:
            previous_config (dict): The previous configuration.
            desired_config (dict): The desired configuration.

        Returns:
            dict: The differences between the configurations.
        """

        differences: dict = {}

        for key, value in desired_config.items():
            if key not in previous_config:
                differences[key] = value
            else:
                if key in self.LIST_PARAMS:
                    if set(value) != set(previous_config[key]):
                        differences[key] = value
                else:
                    if value != previous_config[key]:
                        differences[key] = value

        return differences

    def tune_mount(self, config: dict) -> None:
        """
        Tune the secrets engine configuration.

        Args:
            config (dict): The configuration to apply.
        """

        if self.check_mode:
            return None

        path: str = self.params["engine_mount_point"]

        try:
            self.client.sys.tune_mount_configuration(
                path=path,
                **config,
            )
        except Forbidden:
            self.handle_error(
                VaultModuleError(
                    message=f"Forbidden: Permission denied to tune mount at path '{path}'",
                    exception=traceback.format_exc(),
                ),
            )
        except Exception:
            self.handle_error(
                VaultModuleError(
                    message=f"Error tuning mount configuration at path '{path}'",
                    exception=traceback.format_exc(),
                ),
            )


def ensure_tuned(
    module: VaultSecretsTuneModule,
    previous_config: dict,
    desired_config: dict,
) -> dict:
    """
    Ensure that the secrets engine is tuned with the desired configuration.

    Args:
        module (VaultSecretsTuneModule): The module object.
        previous_config (dict): The previous configuration.
        desired_config (dict): The desired configuration.

    Returns:
        dict: The result of the operation.
    """

    config_diff: dict = module.compare_config(
        previous_config,
        desired_config,
    )

    if not config_diff:
        return dict(changed=False, config=previous_config)

    module.tune_mount(config_diff)

    # Get the updated configuration
    if not module.check_mode:
        updated_config: dict = module.get_current_config()
    else:
        # In check mode, merge the changes into the previous config
        updated_config: dict = previous_config.copy()
        updated_config.update(config_diff)

    return dict(
        changed=True,
        prev_config=previous_config,
        config=updated_config,
    )


def run_module() -> None:
    module: VaultSecretsTuneModule = VaultSecretsTuneModule()

    if not HAS_HVAC:
        module.fail_json(
            msg=missing_required_lib("hvac"),
            exception=HVAC_IMPORT_ERROR,
        )

    desired_config: dict = module.get_defined_tune_params()

    if not desired_config:
        module.fail_json(
            msg="No tune parameters provided. At least one tune parameter must be specified.",
        )

    module.initialize_client()

    previous_config: dict = module.get_current_config()

    result: dict = ensure_tuned(
        module,
        previous_config,
        desired_config,
    )

    module.exit_json(**result)


def main() -> None:
    run_module()


if __name__ == "__main__":
    main()

#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = r"""
module: vault_kv_secret_engine
version_added: 0.1.0
author:
  - sflab
short_description: Configures a KV secret engine in HashiCorp Vault
description:
  - >-
    Ensures a L(KV secret engine,https://developer.hashicorp.com/vault/docs/secrets/kv)
    is configured as expected in HashiCorp Vault.
  - Supports both KV version 1 and KV version 2.
extends_documentation_fragment:
  - sflab.homelab.connection
  - sflab.homelab.auth
  - sflab.homelab.action_group
  - sflab.homelab.check_mode
  - sflab.homelab.engine_mount
  - sflab.homelab.requirements
  - sflab.homelab.secret_engine
options:
  kv_version:
    type: int
    required: false
    default: 2
    choices:
      - 1
      - 2
    description:
      - The version of the KV secret engine to use.
      - Version 1 does not support versioning of secrets.
      - Version 2 supports versioning of secrets.
      - 'Reference: https://developer.hashicorp.com/vault/docs/secrets/kv'
"""

EXAMPLES = r"""
- name: Create a KV v2 secret engine
  sflab.homelab.vault_kv_secret_engine:
    url: https://vault:8200
    auth_method: token
    token: '{{ vault_token }}'
    engine_mount_point: secrets_homelab
    kv_version: 2
    state: present

- name: Create a KV v1 secret engine
  sflab.homelab.vault_kv_secret_engine:
    url: https://vault:8200
    auth_method: token
    token: '{{ vault_token }}'
    engine_mount_point: secrets_homelab_v1
    kv_version: 1
    state: present

- name: Remove a KV secret engine
  sflab.homelab.vault_kv_secret_engine:
    url: https://vault:8200
    auth_method: token
    token: '{{ vault_token }}'
    engine_mount_point: secrets_homelab
    state: absent
"""

RETURN = r"""
config:
  type: dict
  returned: O(state=present)
  description:
    - The configuration of the secret engine.
  sample:
    description: 'The KV secret engine.'
    default_lease_ttl: 2678400
    max_lease_ttl: 2678400
    audit_non_hmac_request_keys: []
    audit_non_hmac_response_keys: []
    listing_visibility: unauth
    passthrough_request_headers: []
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
prev_config:
  description:
    - The previous configuration of the secret engine.
  type: dict
  returned: changed
  sample:
    description: 'The KV secret engine.'
    default_lease_ttl: 2678400
    max_lease_ttl: 2678400
    audit_non_hmac_request_keys: []
    audit_non_hmac_response_keys: []
    listing_visibility: unauth
    passthrough_request_headers: []
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
"""

import traceback


try:
    from hvac.exceptions import Forbidden
except ImportError:
    HAS_HVAC = False
    HVAC_IMPORT_ERROR = traceback.format_exc()
else:
    HAS_HVAC = True
    HVAC_IMPORT_ERROR = None

from typing import Optional

from ansible.module_utils.basic import missing_required_lib

from ..module_utils._vault_module_error import VaultModuleError
from ..module_utils._vault_secret_engine_module import VaultSecretEngineModule


KV_BACKEND_TYPES = ("kv-v1", "kv-v2", "kv")


class VaultKvSecretEngineModule(VaultSecretEngineModule):
    """
    Extends VaultSecretEngineModule to support KV secret engines (v1 and v2).
    Overrides enable_mount to pass the KV version via options.
    """

    def __init__(self, *args, **kwargs):
        super(VaultKvSecretEngineModule, self).__init__(
            *args,
            backend_type="kv",
            argument_spec=dict(
                kv_version=dict(type="int", required=False, default=2, choices=[1, 2]),
            ),
            **kwargs,
        )

    def enable_mount(self, config: dict) -> None:
        """
        Enable the KV secret engine with the specified version.

        Args:
            config (dict): The mount configuration of the secret engine.
        """

        if self.check_mode:
            return None

        path: str = self.params["engine_mount_point"]
        description: Optional[str] = self.params["description"]
        kv_version: int = self.params["kv_version"]

        try:
            self.client.sys.enable_secrets_engine(
                path=path,
                backend_type="kv",
                description=description,
                config=config,
                options={"version": str(kv_version)},
            )
        except Forbidden:
            self.handle_error(
                VaultModuleError(
                    message=f"Forbidden: Permission Denied to path '{path}'",
                    exception=traceback.format_exc(),
                ),
            )
        except Exception:
            self.handle_error(
                VaultModuleError(
                    message=f"Error enabling KV mount '{path}'",
                    exception=traceback.format_exc(),
                ),
            )


def ensure_engine_absent(
    module: VaultKvSecretEngineModule,
    previous_mount_config: Optional[dict],
    previous_backend_type: Optional[str],
) -> dict:
    """
    Ensure that a KV secret engine is absent.

    Args:
        module (VaultKvSecretEngineModule): The module object.
        previous_mount_config (dict): The configuration of the secret engine.
        previous_backend_type (str): The backend type of the secret engine.

    Returns:
        dict: The result of the operation.
    """

    engine_mount_point: str = module.params["engine_mount_point"]

    if previous_mount_config is None:
        return dict(changed=False)

    if previous_backend_type is None or previous_backend_type not in KV_BACKEND_TYPES:
        module.handle_error(
            VaultModuleError(
                message=f"The secret engine at '{engine_mount_point}' has backend '{previous_backend_type}' that is not a KV secret engine",
            ),
        )

    module.disable_mount()

    return dict(changed=True, prev_config=previous_mount_config)


def ensure_engine_present(
    module: VaultKvSecretEngineModule,
    previous_mount_config: Optional[dict],
    previous_backend_type: Optional[str],
    desired_mount_config: dict,
) -> dict:
    """
    Ensure that a KV secret engine is present.

    Args:
        module (VaultKvSecretEngineModule): The module object.
        previous_mount_config (dict): The previous configuration of the secret engine.
        previous_backend_type (str): The backend type of the secret engine.
        desired_mount_config (dict): The desired configuration of the secret engine.

    Returns:
        dict: The result of the operation to be sent to Ansible.
    """

    engine_mount_point: str = module.params["engine_mount_point"]
    replace_non_kv_secret_engine: bool = module.params["replace_different_backend_type"]

    if previous_mount_config is None:
        description: Optional[str] = desired_mount_config.pop("description", None)

        module.enable_mount(desired_mount_config)

        return dict(changed=True, config=dict(description=description, **desired_mount_config))

    if previous_backend_type is None or previous_backend_type not in KV_BACKEND_TYPES:
        if not replace_non_kv_secret_engine:
            module.handle_error(
                VaultModuleError(
                    message=f"The secret engine at '{engine_mount_point}' has backend '{previous_backend_type}' that is not a KV secret engine",
                ),
            )

        module.disable_mount()

        description: Optional[str] = desired_mount_config.pop("description", None)

        module.enable_mount(desired_mount_config)

        return dict(changed=True, config=dict(description=description, **desired_mount_config))

    mount_config_diff: dict = module.compare_mount_config(
        previous_mount_config,
        desired_mount_config,
    )

    if mount_config_diff:
        module.configure_mount(mount_config_diff)

        return dict(
            changed=True,
            prev_config=previous_mount_config,
            config=desired_mount_config,
        )

    return dict(changed=False, config=previous_mount_config)


def run_module() -> None:
    module = VaultKvSecretEngineModule()

    if not HAS_HVAC:
        module.fail_json(
            msg=missing_required_lib("hvac"),
            exception=HVAC_IMPORT_ERROR,
        )

    state: str = module.params.get("state")

    desired_mount_config: dict = module.get_defined_mount_config_params()

    module.initialize_client()

    previous_mount_config: Optional[dict] = module.get_formatted_mount_config()
    previous_backend_type: Optional[str] = module.get_mount_backend_type()

    if state == "absent":
        result: dict = ensure_engine_absent(
            module,
            previous_mount_config,
            previous_backend_type,
        )

    if state == "present":
        result: dict = ensure_engine_present(
            module,
            previous_mount_config,
            previous_backend_type,
            desired_mount_config,
        )

    module.exit_json(**result)


def main() -> None:
    run_module()


if __name__ == "__main__":
    main()

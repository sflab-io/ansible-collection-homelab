#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = r"""
module: vault_write
version_added: 0.1.0
author:
  - Sebastian Freund (@sflab)
short_description: Execute a write operation in HashiCorp Vault
description:
  - >-
    L(Writes,https://hvac.readthedocs.io/en/stable/usage/index.html#writing-data)
    data to a specified path in HashiCorp Vault.
  - This module provides a generic interface for executing Vault write operations.
  - The module is not idempotent and will always report changed=true when executed.
extends_documentation_fragment:
  - sflab.homelab.connection
  - sflab.homelab.auth
  - sflab.homelab.action_group
  - sflab.homelab.check_mode
  - sflab.homelab.requirements
options:
  path:
    type: str
    required: true
    description:
      - The Vault path to write data to.
  data:
    type: dict
    required: true
    description:
      - The data to write to the specified path.
      - Key-value pairs are passed through to the Vault write operation without validation.
"""

EXAMPLES = r"""
- name: Configure PKI cluster path
  sflab.homelab.vault_write:
    url: https://vault:8201
    auth_method: token
    token: '{{ vault_token }}'
    path: pki/config/cluster
    data:
      path: https://vault.example.com/v1/pki
      aia_path: https://vault.example.com/v1/pki

- name: Configure PKI URLs
  sflab.homelab.vault_write:
    url: https://vault:8201
    auth_method: token
    token: '{{ vault_token }}'
    path: pki/config/urls
    data:
      issuing_certificates: "{{ cluster_aia_path }}/issuer/{{ issuer_id }}/der"
      crl_distribution_points: "{{ cluster_aia_path }}/issuer/{{ issuer_id }}/crl/der"
      ocsp_servers: "{{ cluster_path }}/ocsp"
      enable_templating: true

- name: Configure intermediate PKI cluster path
  sflab.homelab.vault_write:
    url: https://vault:8201
    auth_method: token
    token: '{{ vault_token }}'
    path: pki_int/config/cluster
    data:
      path: https://vault.example.com/v1/pki_int
      aia_path: https://vault.example.com/v1/pki_int
"""

RETURN = r"""
response:
  type: dict
  returned: |
    changed
    not check_mode
  description:
    - The response from the Vault write operation.
  sample:
    request_id: abc123-def456-ghi789
    lease_id: ""
    renewable: false
    lease_duration: 0
    data: {}
    wrap_info: null
    warnings: null
    auth: null
"""

import traceback

from typing import Optional

from ansible.module_utils.basic import missing_required_lib


ARGSPEC: dict = dict(
    path=dict(type="str", required=True),
    data=dict(type="dict", required=True),
)

try:
    import hvac
except ImportError:
    HAS_HVAC: bool = False
    HVAC_IMPORT_ERROR: Optional[str] = traceback.format_exc()

    from ansible_collections.community.hashi_vault.plugins.module_utils._hashi_vault_module import (
        HashiVaultModule,
    )

    class VaultWriteModule(HashiVaultModule):
        """
        Extends HashiVaultModule to simplify the creation of Vault modules.
        """

        def __init__(
            self,
            *args,
            argument_spec: Optional[dict] = None,
            **kwargs,
        ) -> None:
            argspec: dict = ARGSPEC.copy()

            if argument_spec is not None:
                argspec.update(argument_spec)

            super_argspec: dict = HashiVaultModule.generate_argspec(**argspec)

            super(VaultWriteModule, self).__init__(
                *args,
                argument_spec=super_argspec,
                supports_check_mode=True,
                **kwargs,
            )

else:
    HAS_HVAC: bool = True
    HVAC_IMPORT_ERROR: Optional[str] = None

    from ..module_utils._vault_module import VaultModule
    from ..module_utils._vault_module_error import VaultModuleError

    class VaultWriteModule(VaultModule):
        """
        Extends VaultModule to simplify the creation of Vault modules.
        """

        client: hvac.Client

        def __init__(
            self,
            *args,
            argument_spec: Optional[dict] = None,
            **kwargs,
        ) -> None:
            argspec: dict = ARGSPEC.copy()

            if argument_spec is not None:
                argspec.update(argument_spec)

            super(VaultWriteModule, self).__init__(
                *args,
                argument_spec=argspec,
                supports_check_mode=True,
                **kwargs,
            )


def run_module() -> None:
    module: VaultWriteModule = VaultWriteModule()

    if not HAS_HVAC:
        module.fail_json(
            msg=missing_required_lib("hvac"),
            exception=HVAC_IMPORT_ERROR,
        )

    module.initialize_client()

    path: str = module.params["path"]
    data: dict = module.params["data"]

    result: dict = dict(changed=True)

    if not module.check_mode:
        try:
            # Use the adapter directly to avoid conflicts when data contains 'path' key
            # write() uses **kwargs which causes "multiple values for argument 'path'" error
            # The adapter.post() method allows us to send data as JSON without parameter conflicts
            response = module.client._adapter.post(f"/v1/{path}", json=data)
            if isinstance(response, dict):
                result["response"] = response
            elif response.status_code == 204 or not response.content:
                result["response"] = {}
            else:
                result["response"] = response.json()
        except Exception as e:
            # Capture the actual exception type and message for better diagnostics
            exception_type = type(e).__name__
            exception_msg = str(e)
            module.handle_error(
                VaultModuleError(
                    message=f"Error writing to Vault path '{path}': {exception_type}: {exception_msg}",
                    exception=traceback.format_exc(),
                ),
            )

    module.exit_json(**result)


def main() -> None:
    run_module()


if __name__ == "__main__":
    main()

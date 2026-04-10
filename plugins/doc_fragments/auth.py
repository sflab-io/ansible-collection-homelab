# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Sebastian Freund (@sflab)
# SPDX-License-Identifier: MIT

from __future__ import absolute_import, division, print_function


__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r"""
    options:
      auth_method:
        description:
          - Authentication method to be used.
          - C(none) auth method was added in collection version C(0.1.0).
          - C(cert) auth method was added in collection version C(0.1.0).
        choices:
          - token
          - userpass
          - ldap
          - approle
          - jwt
          - cert
          - none
        default: token
        type: str
      mount_point:
        description:
          - Vault mount point.
          - If not specified, the default mount point for a given auth method is used.
          - Does not apply to token authentication.
        type: str
      token:
        description:
          - Vault token. Token may be specified explicitly, through the listed [env] vars, and also through the C(VAULT_TOKEN) env var.
          - If no token is supplied, explicitly or through env, then the plugin will check for a token file, as determined by I(token_path) and I(token_file).
          - The order of token loading (first found wins) is C(token param -> ansible var -> ANSIBLE_HASHI_VAULT_TOKEN -> VAULT_TOKEN -> token file).
        type: str
      token_path:
        description: If no token is specified, will try to read the I(token_file) from this path.
        type: str
      token_file:
        description: If no token is specified, will try to read the token from this file in I(token_path).
        default: '.vault-token'
        type: str
      token_validate:
        description:
          - For token auth, will perform a C(lookup-self) operation to determine the token's validity before using it.
          - Disable if your token does not have the C(lookup-self) capability.
        type: bool
        default: false
        version_added: 0.1.0
      username:
        description: Authentication user name.
        type: str
      password:
        description: Authentication password.
        type: str
      role_id:
        description:
          - Vault Role ID or name. Used in C(approle) and C(cert) auth methods.
          - For C(cert) auth, if no I(role_id) is supplied, the default behavior is to try all certificate roles and return any one that matches.
        type: str
      secret_id:
        description: Secret ID to be used for Vault AppRole authentication.
        type: str
      jwt:
        description: The JSON Web Token (JWT) to use for JWT authentication to Vault.
        type: str
      cert_auth_public_key:
        description: For C(cert) auth, path to the certificate file to authenticate with, in PEM format.
        type: path
        version_added: 0.1.0
      cert_auth_private_key:
        description: For C(cert) auth, path to the private key file to authenticate with, in PEM format.
        type: path
        version_added: 0.1.0
    """

    PLUGINS = r"""
    options:
      auth_method:
        env:
          - name: ANSIBLE_HASHI_VAULT_AUTH_METHOD
            version_added: 0.1.0
        ini:
          - section: hashi_vault_collection
            key: auth_method
            version_added: 0.1.0
        vars:
          - name: ansible_hashi_vault_auth_method
            version_added: 0.1.0
      mount_point:
        env:
          - name: ANSIBLE_HASHI_VAULT_MOUNT_POINT
            version_added: 0.1.0
        ini:
          - section: hashi_vault_collection
            key: mount_point
            version_added: 0.1.0
        vars:
          - name: ansible_hashi_vault_mount_point
            version_added: 0.1.0
      token:
        env:
          - name: ANSIBLE_HASHI_VAULT_TOKEN
            version_added: 0.1.0
        vars:
          - name: ansible_hashi_vault_token
            version_added: 0.1.0
      token_path:
        env:
          - name: ANSIBLE_HASHI_VAULT_TOKEN_PATH
            version_added: 0.1.0
        ini:
          - section: hashi_vault_collection
            key: token_path
            version_added: 0.1.0
        vars:
          - name: ansible_hashi_vault_token_path
            version_added: 0.1.0
      token_file:
        env:
          - name: ANSIBLE_HASHI_VAULT_TOKEN_FILE
            version_added: 0.1.0
        ini:
          - section: hashi_vault_collection
            key: token_file
            version_added: 0.1.0
        vars:
          - name: ansible_hashi_vault_token_file
            version_added: 0.1.0
      token_validate:
        env:
          - name: ANSIBLE_HASHI_VAULT_TOKEN_VALIDATE
        ini:
          - section: hashi_vault_collection
            key: token_validate
            version_added: 0.1.0
        vars:
          - name: ansible_hashi_vault_token_validate
            version_added: 0.1.0
      username:
        env:
          - name: ANSIBLE_HASHI_VAULT_USERNAME
            version_added: '0.1.0'
        vars:
          - name: ansible_hashi_vault_username
            version_added: '0.1.0'
      password:
        env:
          - name: ANSIBLE_HASHI_VAULT_PASSWORD
            version_added: '0.1.0'
        vars:
          - name: ansible_hashi_vault_password
            version_added: '0.1.0'
      role_id:
        env:
          - name: ANSIBLE_HASHI_VAULT_ROLE_ID
            version_added: 0.1.0
        ini:
          - section: hashi_vault_collection
            key: role_id
            version_added: 0.1.0
        vars:
          - name: ansible_hashi_vault_role_id
            version_added: 0.1.0
      secret_id:
        env:
          - name: ANSIBLE_HASHI_VAULT_SECRET_ID
            version_added: 0.1.0
        vars:
          - name: ansible_hashi_vault_secret_id
            version_added: 0.1.0
      jwt:
        env:
          - name: ANSIBLE_HASHI_VAULT_JWT
      cert_auth_public_key:
        env:
          - name: ANSIBLE_HASHI_VAULT_CERT_AUTH_PUBLIC_KEY
        vars:
          - name: ansible_hashi_vault_cert_auth_public_key
            version_added: 0.1.0
        ini:
          - section: hashi_vault_collection
            key: cert_auth_public_key
      cert_auth_private_key:
        env:
          - name: ANSIBLE_HASHI_VAULT_CERT_AUTH_PRIVATE_KEY
        vars:
          - name: ansible_hashi_vault_cert_auth_private_key
            version_added: 0.1.0
        ini:
          - section: hashi_vault_collection
            key: cert_auth_private_key
    """

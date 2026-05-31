#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = r"""
module: authentik_provider
version_added: 0.1.0
author:
  - Sebastian Freund (@sflab)
short_description: Manage OAuth2/OpenID Connect providers in Authentik
description:
  - Creates or deletes an OAuth2/OpenID Connect provider in Authentik.
  - Supports idempotent operation — repeated runs produce no changes when state is already correct.
  - Resolves the authorization flow UUID, invalidation flow UUID, signing key UUID, and scope
    property mapping UUIDs from their human-readable names automatically.
options:
  authentik_url:
    type: str
    required: true
    description:
      - The base URL of the Authentik instance, without a trailing slash.
      - "Example: https://authentik.home.sflab.io"
      - The module automatically appends C(/api/v3) when the URL does not already end with it.
  authentik_token:
    type: str
    required: true
    no_log: true
    description:
      - The Authentik API token used to authenticate against the Authentik API.
  name:
    type: str
    required: true
    description:
      - The name of the OAuth2/OpenID Connect provider.
  authorization_flow:
    type: str
    required: true
    description:
      - The slug of the authorization flow to use for this provider.
      - "Example: default-provider-authorization-explicit-consent"
  invalidation_flow:
    type: str
    required: false
    default: default-provider-invalidation-flow
    description:
      - The slug of the invalidation flow used when ending the session from this provider.
      - "Example: default-provider-invalidation-flow"
  client_type:
    type: str
    required: false
    default: confidential
    choices:
      - confidential
      - public
    description:
      - The OAuth2 client type.
      - Confidential clients are capable of maintaining the confidentiality of their credentials.
      - Public clients are incapable.
  redirect_uris:
    type: list
    elements: str
    required: true
    description:
      - List of allowed redirect URIs for this provider.
      - Each URI will use strict matching mode.
  scopes:
    type: list
    elements: str
    required: false
    default:
      - openid
      - profile
      - email
    description:
      - List of OAuth2 scope names to assign to this provider.
      - Scope property mappings are resolved by scope name via the API.
  signing_key:
    type: str
    required: false
    description:
      - The name of the certificate key pair to use for signing tokens.
      - "Example: authentik Self-signed Certificate"
      - When omitted, no signing key is configured.
  state:
    type: str
    required: false
    default: present
    choices:
      - present
      - absent
    description:
      - The desired state of the provider.
      - When C(present), creates the provider if it does not exist.
      - When C(absent), removes the provider if it exists.
  validate_certs:
    type: bool
    required: false
    default: true
    description:
      - Whether to validate SSL certificates when connecting to the Authentik API.
      - Set to C(false) when using a self-signed or custom CA certificate that is not trusted
        by the system's default CA store.
      - "Note: Disabling certificate validation is not recommended for production use unless
        combined with O(ca_cert_path)."
  ca_cert_path:
    type: path
    required: false
    description:
      - Path to a PEM-encoded CA certificate file used to verify the Authentik server certificate.
      - Use this when the Authentik server uses a certificate issued by a custom or internal CA
        (for example a HashiCorp Vault PKI CA).
      - When set, O(validate_certs) should remain C(true).
"""

EXAMPLES = r"""
- name: Create OAuth2 provider for Portainer
  sflab.homelab.authentik_provider:
    authentik_url: "https://authentik.home.sflab.io"
    authentik_token: "{{ authentik_api_token }}"
    name: "portainer"
    authorization_flow: "default-provider-authorization-explicit-consent"
    client_type: "confidential"
    redirect_uris:
      - "https://portainer.authentik.home.sflab.io/"
    scopes:
      - openid
      - profile
      - email
    signing_key: "authentik Self-signed Certificate"
    state: present
  register: provider_result

- name: Remove OAuth2 provider for Portainer
  sflab.homelab.authentik_provider:
    authentik_url: "https://authentik.home.sflab.io"
    authentik_token: "{{ authentik_api_token }}"
    name: "portainer"
    authorization_flow: "default-provider-authorization-explicit-consent"
    redirect_uris:
      - "https://portainer.authentik.home.sflab.io/"
    state: absent
"""

RETURN = r"""
provider_pk:
  type: int
  returned: when state is present
  description:
    - The primary key (integer ID) of the created or existing provider.
  sample: 42
client_id:
  type: str
  returned: when state is present
  description:
    - The OAuth2 client ID of the provider.
  sample: "abc123def456"
client_secret:
  type: str
  returned: when state is present
  no_log: true
  description:
    - The OAuth2 client secret of the provider.
  sample: "supersecret"
changed:
  type: bool
  returned: always
  description:
    - Whether the module made any changes.
"""

import traceback

from typing import Optional
from uuid import UUID

from ansible.module_utils.basic import AnsibleModule, missing_required_lib


try:
    import authentik_client
    from authentik_client.rest import ApiException
except ImportError:
    HAS_AUTHENTIK_CLIENT: bool = False
    AUTHENTIK_CLIENT_IMPORT_ERROR: Optional[str] = traceback.format_exc()
else:
    HAS_AUTHENTIK_CLIENT: bool = True
    AUTHENTIK_CLIENT_IMPORT_ERROR: Optional[str] = None


ARGSPEC: dict = dict(
    authentik_url=dict(type="str", required=True),
    authentik_token=dict(type="str", required=True, no_log=True),
    name=dict(type="str", required=True),
    authorization_flow=dict(type="str", required=True),
    invalidation_flow=dict(type="str", required=False, default="default-provider-invalidation-flow"),
    client_type=dict(type="str", required=False, default="confidential", choices=["confidential", "public"]),
    redirect_uris=dict(type="list", elements="str", required=True),
    scopes=dict(type="list", elements="str", required=False, default=["openid", "profile", "email"]),
    signing_key=dict(type="str", required=False, default=None),
    state=dict(type="str", required=False, default="present", choices=["present", "absent"]),
    validate_certs=dict(type="bool", required=False, default=True),
    ca_cert_path=dict(type="path", required=False, default=None),
)


def get_flow_uuid(flows_api, slug: str, module: AnsibleModule) -> UUID:
    """
    Resolve a flow UUID from its slug.

    Args:
        flows_api: An authenticated Authentik FlowsApi instance.
        slug: The slug of the flow.
        module: The AnsibleModule instance for error reporting.

    Returns:
        The UUID of the flow.
    """
    try:
        response = flows_api.flows_instances_list(slug=slug)
        if not response.results:
            module.fail_json(msg=f"Flow with slug '{slug}' not found in Authentik")
        return response.results[0].pk
    except ApiException:
        module.fail_json(
            msg=f"Failed to retrieve flow with slug '{slug}' from Authentik",
            exception=traceback.format_exc(),
        )


def get_signing_key_uuid(crypto_api, name: str, module: AnsibleModule) -> UUID:
    """
    Resolve a certificate key pair UUID from its name.

    Args:
        crypto_api: An authenticated Authentik CryptoApi instance.
        name: The name of the certificate key pair.
        module: The AnsibleModule instance for error reporting.

    Returns:
        The UUID of the certificate key pair.
    """
    try:
        response = crypto_api.crypto_certificatekeypairs_list(name=name)
        if not response.results:
            module.fail_json(msg=f"Certificate key pair with name '{name}' not found in Authentik")
        return response.results[0].pk
    except ApiException:
        module.fail_json(
            msg=f"Failed to retrieve certificate key pair '{name}' from Authentik",
            exception=traceback.format_exc(),
        )


def get_scope_mapping_uuids(propertymappings_api, scope_names: list, module: AnsibleModule) -> list:
    """
    Resolve a list of scope names to their property mapping UUIDs.

    Args:
        propertymappings_api: An authenticated Authentik PropertymappingsApi instance.
        scope_names: List of OAuth2 scope name strings.
        module: The AnsibleModule instance for error reporting.

    Returns:
        A list of UUIDs for the scope property mappings.
    """
    uuids: list = []
    for scope_name in scope_names:
        try:
            response = propertymappings_api.propertymappings_provider_scope_list(scope_name=scope_name)
            if not response.results:
                module.fail_json(
                    msg=f"Scope property mapping for scope '{scope_name}' not found in Authentik",
                )
            uuids.append(response.results[0].pk)
        except ApiException:
            module.fail_json(
                msg=f"Failed to retrieve scope property mapping for scope '{scope_name}' from Authentik",
                exception=traceback.format_exc(),
            )
    return uuids


def find_existing_provider(providers_api, name: str, module: AnsibleModule):
    """
    Find an existing OAuth2 provider by name.

    Args:
        providers_api: An authenticated Authentik ProvidersApi instance.
        name: The name of the provider to find.
        module: The AnsibleModule instance for error reporting.

    Returns:
        The provider object if found, None otherwise.
    """
    try:
        response = providers_api.providers_oauth2_list(name=name)
        for provider in response.results:
            if provider.name == name:
                return provider
        return None
    except ApiException:
        module.fail_json(
            msg=f"Failed to retrieve OAuth2 providers from Authentik",
            exception=traceback.format_exc(),
        )


def ensure_present(
    module: AnsibleModule,
    providers_api,
    flows_api,
    crypto_api,
    propertymappings_api,
) -> dict:
    """
    Ensure the OAuth2 provider exists in Authentik.

    Args:
        module: The AnsibleModule instance.
        providers_api: An authenticated Authentik ProvidersApi instance.
        flows_api: An authenticated Authentik FlowsApi instance.
        crypto_api: An authenticated Authentik CryptoApi instance.
        propertymappings_api: An authenticated Authentik PropertymappingsApi instance.

    Returns:
        A result dict with provider details and changed flag.
    """
    name: str = module.params["name"]
    authorization_flow_slug: str = module.params["authorization_flow"]
    invalidation_flow_slug: str = module.params["invalidation_flow"]
    client_type_str: str = module.params["client_type"]
    redirect_uris: list = module.params["redirect_uris"]
    scope_names: list = module.params["scopes"]
    signing_key_name: Optional[str] = module.params["signing_key"]

    existing = find_existing_provider(providers_api, name, module)

    if existing is not None:
        return dict(
            changed=False,
            provider_pk=existing.pk,
            client_id=existing.client_id,
            client_secret=existing.client_secret,
        )

    if module.check_mode:
        return dict(
            changed=True,
            provider_pk=None,
            client_id=None,
            client_secret=None,
        )

    authorization_flow_uuid = get_flow_uuid(flows_api, authorization_flow_slug, module)
    invalidation_flow_uuid = get_flow_uuid(flows_api, invalidation_flow_slug, module)
    scope_uuids = get_scope_mapping_uuids(propertymappings_api, scope_names, module)

    signing_key_uuid: Optional[UUID] = None
    if signing_key_name:
        signing_key_uuid = get_signing_key_uuid(crypto_api, signing_key_name, module)

    client_type_enum = (
        authentik_client.ClientTypeEnum.CONFIDENTIAL
        if client_type_str == "confidential"
        else authentik_client.ClientTypeEnum.PUBLIC
    )

    redirect_uri_requests = [
        authentik_client.RedirectURIRequest(
            matching_mode=authentik_client.MatchingModeEnum.STRICT,
            url=uri,
        )
        for uri in redirect_uris
    ]

    provider_request = authentik_client.OAuth2ProviderRequest(
        name=name,
        authorization_flow=authorization_flow_uuid,
        invalidation_flow=invalidation_flow_uuid,
        client_type=client_type_enum,
        redirect_uris=redirect_uri_requests,
        property_mappings=scope_uuids,
        signing_key=signing_key_uuid,
    )

    try:
        new_provider = providers_api.providers_oauth2_create(provider_request)
    except ApiException:
        module.fail_json(
            msg=f"Failed to create OAuth2 provider '{name}' in Authentik",
            exception=traceback.format_exc(),
        )

    return dict(
        changed=True,
        provider_pk=new_provider.pk,
        client_id=new_provider.client_id,
        client_secret=new_provider.client_secret,
    )


def ensure_absent(
    module: AnsibleModule,
    providers_api,
) -> dict:
    """
    Ensure the OAuth2 provider does not exist in Authentik.

    Args:
        module: The AnsibleModule instance.
        providers_api: An authenticated Authentik ProvidersApi instance.

    Returns:
        A result dict with changed flag.
    """
    name: str = module.params["name"]

    existing = find_existing_provider(providers_api, name, module)

    if existing is None:
        return dict(changed=False)

    if module.check_mode:
        return dict(changed=True)

    try:
        providers_api.providers_oauth2_destroy(existing.pk)
    except ApiException:
        module.fail_json(
            msg=f"Failed to delete OAuth2 provider '{name}' from Authentik",
            exception=traceback.format_exc(),
        )

    return dict(changed=True)


def run_module() -> None:
    module: AnsibleModule = AnsibleModule(
        argument_spec=ARGSPEC,
        supports_check_mode=True,
    )

    if not HAS_AUTHENTIK_CLIENT:
        module.fail_json(
            msg=missing_required_lib("authentik-client"),
            exception=AUTHENTIK_CLIENT_IMPORT_ERROR,
        )

    authentik_url: str = module.params["authentik_url"].rstrip("/")
    authentik_token: str = module.params["authentik_token"]
    state: str = module.params["state"]
    validate_certs: bool = module.params["validate_certs"]
    ca_cert_path: Optional[str] = module.params["ca_cert_path"]

    if not authentik_url.endswith("/api/v3"):
        authentik_url = authentik_url + "/api/v3"

    configuration = authentik_client.Configuration(
        host=authentik_url,
        access_token=authentik_token,
        verify_ssl=validate_certs,
        ssl_ca_cert=ca_cert_path,
    )

    with authentik_client.ApiClient(configuration) as api_client:
        providers_api = authentik_client.ProvidersApi(api_client)
        flows_api = authentik_client.FlowsApi(api_client)
        crypto_api = authentik_client.CryptoApi(api_client)
        propertymappings_api = authentik_client.PropertymappingsApi(api_client)

        if state == "present":
            result: dict = ensure_present(module, providers_api, flows_api, crypto_api, propertymappings_api)
        else:
            result: dict = ensure_absent(module, providers_api)

    module.exit_json(**result)


def main() -> None:
    run_module()


if __name__ == "__main__":
    main()

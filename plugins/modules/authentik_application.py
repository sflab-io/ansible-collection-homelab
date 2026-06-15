#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = r"""
module: authentik_application
version_added: 0.1.0
author:
  - Sebastian Freund (@sflab)
short_description: Manage applications in Authentik
description:
  - Creates or deletes an application in Authentik.
  - Supports idempotent operation — repeated runs produce no changes when state is already correct.
  - Resolves the provider primary key from the provider name automatically.
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
      - The display name of the application.
  slug:
    type: str
    required: true
    description:
      - The URL slug of the application. Must be unique within the Authentik instance.
      - "Example: portainer"
  provider:
    type: str
    required: false
    description:
      - The name of the OAuth2 provider to associate with this application.
      - The provider primary key is resolved by name via the API.
      - When omitted, the application is created without a provider.
  state:
    type: str
    required: false
    default: present
    choices:
      - present
      - absent
    description:
      - The desired state of the application.
      - When C(present), creates the application if it does not exist.
      - When C(absent), removes the application if it exists.
  authentik_validate_certs:
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
      - When set, O(authentik_validate_certs) should remain C(true).
"""

EXAMPLES = r"""
- name: Create Portainer application in Authentik
  sflab.homelab.authentik_application:
    authentik_url: "https://authentik.home.sflab.io"
    authentik_token: "{{ authentik_api_token }}"
    name: "Portainer"
    slug: "portainer"
    provider: "portainer"
    state: present

- name: Remove Portainer application from Authentik
  sflab.homelab.authentik_application:
    authentik_url: "https://authentik.home.sflab.io"
    authentik_token: "{{ authentik_api_token }}"
    name: "Portainer"
    slug: "portainer"
    state: absent
"""

RETURN = r"""
application_slug:
  type: str
  returned: when state is present
  description:
    - The slug of the created or existing application.
  sample: "portainer"
changed:
  type: bool
  returned: always
  description:
    - Whether the module made any changes.
"""

import traceback

from typing import Optional

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
    slug=dict(type="str", required=True),
    provider=dict(type="str", required=False, default=None),
    state=dict(type="str", required=False, default="present", choices=["present", "absent"]),
    authentik_validate_certs=dict(type="bool", required=False, default=True),
    ca_cert_path=dict(type="path", required=False, default=None),
)


def find_existing_application(core_api, slug: str, module: AnsibleModule):
    """
    Find an existing application by slug.

    Args:
        core_api: An authenticated Authentik CoreApi instance.
        slug: The slug of the application to find.
        module: The AnsibleModule instance for error reporting.

    Returns:
        The application object if found, None otherwise.
    """
    try:
        return core_api.core_applications_retrieve(slug)
    except ApiException as exc:
        if exc.status == 404:
            return None
        module.fail_json(
            msg=f"Failed to retrieve application '{slug}' from Authentik",
            exception=traceback.format_exc(),
        )


def find_provider_pk(providers_api, provider_name: str, module: AnsibleModule) -> int:
    """
    Resolve an OAuth2 provider primary key from its name.

    Args:
        providers_api: An authenticated Authentik ProvidersApi instance.
        provider_name: The name of the provider.
        module: The AnsibleModule instance for error reporting.

    Returns:
        The integer primary key of the provider.
    """
    try:
        response = providers_api.providers_oauth2_list(name=provider_name)
        for provider in response.results:
            if provider.name == provider_name:
                return provider.pk
        module.fail_json(msg=f"OAuth2 provider with name '{provider_name}' not found in Authentik")
    except ApiException:
        module.fail_json(
            msg=f"Failed to retrieve OAuth2 provider '{provider_name}' from Authentik",
            exception=traceback.format_exc(),
        )


def ensure_present(
    module: AnsibleModule,
    core_api,
    providers_api,
) -> dict:
    """
    Ensure the application exists in Authentik.

    Args:
        module: The AnsibleModule instance.
        core_api: An authenticated Authentik CoreApi instance.
        providers_api: An authenticated Authentik ProvidersApi instance.

    Returns:
        A result dict with application slug and changed flag.
    """
    name: str = module.params["name"]
    slug: str = module.params["slug"]
    provider_name: Optional[str] = module.params["provider"]

    existing = find_existing_application(core_api, slug, module)

    if existing is not None:
        return dict(
            changed=False,
            application_slug=existing.slug,
        )

    if module.check_mode:
        return dict(
            changed=True,
            application_slug=slug,
        )

    provider_pk: Optional[int] = None
    if provider_name:
        provider_pk = find_provider_pk(providers_api, provider_name, module)

    app_request = authentik_client.ApplicationRequest(
        name=name,
        slug=slug,
        provider=provider_pk,
    )

    try:
        new_app = core_api.core_applications_create(app_request)
    except ApiException:
        module.fail_json(
            msg=f"Failed to create application '{name}' in Authentik",
            exception=traceback.format_exc(),
        )

    return dict(
        changed=True,
        application_slug=new_app.slug,
    )


def ensure_absent(
    module: AnsibleModule,
    core_api,
) -> dict:
    """
    Ensure the application does not exist in Authentik.

    Args:
        module: The AnsibleModule instance.
        core_api: An authenticated Authentik CoreApi instance.

    Returns:
        A result dict with changed flag.
    """
    slug: str = module.params["slug"]

    existing = find_existing_application(core_api, slug, module)

    if existing is None:
        return dict(changed=False)

    if module.check_mode:
        return dict(changed=True)

    try:
        core_api.core_applications_destroy(existing.slug)
    except ApiException:
        module.fail_json(
            msg=f"Failed to delete application '{slug}' from Authentik",
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
    authentik_validate_certs: bool = module.params["authentik_validate_certs"]
    ca_cert_path: Optional[str] = module.params["ca_cert_path"]

    if not authentik_url.endswith("/api/v3"):
        authentik_url = authentik_url + "/api/v3"

    configuration = authentik_client.Configuration(
        host=authentik_url,
        access_token=authentik_token,
        verify_ssl=authentik_validate_certs,
        ssl_ca_cert=ca_cert_path,
    )

    with authentik_client.ApiClient(configuration) as api_client:
        core_api = authentik_client.CoreApi(api_client)
        providers_api = authentik_client.ProvidersApi(api_client)

        if state == "present":
            result: dict = ensure_present(module, core_api, providers_api)
        else:
            result: dict = ensure_absent(module, core_api)

    module.exit_json(**result)


def main() -> None:
    run_module()


if __name__ == "__main__":
    main()

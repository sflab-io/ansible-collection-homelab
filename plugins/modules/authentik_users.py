#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = r"""
module: authentik_users
version_added: 0.1.0
author:
  - Sebastian Freund (@sflab)
short_description: Synchronizes NetBox contact groups and contacts to Authentik groups and users
description:
  - Reads all contact groups from NetBox and creates corresponding groups in Authentik.
  - Reads all contacts for each NetBox contact group and creates corresponding users in Authentik.
  - Assigns each Authentik user to the corresponding Authentik group.
  - Supports idempotent operation — repeated runs produce no changes when state is already correct.
  - When state=absent, removes all users and groups that were created from NetBox data.
options:
  netbox_url:
    type: str
    required: true
    description:
      - The URL of the NetBox instance.
      - "Example: https://netbox.home.sflab.io"
  netbox_token:
    type: str
    required: true
    no_log: true
    description:
      - The NetBox API token used to authenticate against the NetBox API.
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
  state:
    type: str
    required: false
    default: present
    choices:
      - present
      - absent
    description:
      - The desired state of the synchronization.
      - When C(present), creates groups and users in Authentik as needed.
      - When C(absent), removes users and groups from Authentik that originate from NetBox data.
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
- name: Synchronize NetBox contacts to Authentik
  sflab.homelab.authentik_users:
    netbox_url: "https://netbox.home.sflab.io"
    netbox_token: "{{ netbox_api_token }}"
    authentik_url: "https://authentik.home.sflab.io"
    authentik_token: "{{ authentik_api_token }}"
    state: present

- name: Remove all NetBox-synchronized users and groups from Authentik
  sflab.homelab.authentik_users:
    netbox_url: "https://netbox.home.sflab.io"
    netbox_token: "{{ netbox_api_token }}"
    authentik_url: "https://authentik.home.sflab.io"
    authentik_token: "{{ authentik_api_token }}"
    state: absent
"""

RETURN = r"""
groups_created:
  type: int
  returned: always
  description:
    - The number of Authentik groups that were newly created during this run.
  sample: 3
groups_deleted:
  type: int
  returned: always
  description:
    - The number of Authentik groups that were deleted during this run.
  sample: 0
users_created:
  type: int
  returned: always
  description:
    - The number of Authentik users that were newly created during this run.
  sample: 5
users_deleted:
  type: int
  returned: always
  description:
    - The number of Authentik users that were deleted during this run.
  sample: 0
memberships_created:
  type: int
  returned: always
  description:
    - The number of group membership assignments that were newly created during this run.
  sample: 5
"""

import traceback

from typing import Optional

from ansible.module_utils.basic import AnsibleModule, missing_required_lib


try:
    import pynetbox
except ImportError:
    HAS_PYNETBOX: bool = False
    PYNETBOX_IMPORT_ERROR: Optional[str] = traceback.format_exc()
else:
    HAS_PYNETBOX: bool = True
    PYNETBOX_IMPORT_ERROR: Optional[str] = None

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
    netbox_url=dict(type="str", required=True),
    netbox_token=dict(type="str", required=True, no_log=True),
    authentik_url=dict(type="str", required=True),
    authentik_token=dict(type="str", required=True, no_log=True),
    state=dict(type="str", required=False, default="present", choices=["present", "absent"]),
    validate_certs=dict(type="bool", required=False, default=True),
    ca_cert_path=dict(type="path", required=False, default=None),
)


def generate_username(full_name: str) -> str:
    """
    Generate an Authentik username from a full name.

    The username is composed of the first letter of the first name(s)
    and the full last name, all in lowercase.

    Examples:
        "Sebastian Freund" -> "sfreund"
        "John Doe"         -> "jdoe"
        "Anna-Maria Müller" -> "amüller"

    Args:
        full_name: The full name of the person.

    Returns:
        A lowercase username string.
    """
    parts = full_name.strip().split()
    if len(parts) < 2:
        return full_name.lower().replace(" ", "")
    first_name = parts[0]
    last_name = parts[-1]
    return (first_name[0] + last_name).lower()


def get_netbox_contact_groups(netbox_url: str, netbox_token: str, module: AnsibleModule) -> list:
    """
    Retrieve all contact groups from NetBox.

    Args:
        netbox_url: The URL of the NetBox instance.
        netbox_token: The NetBox API token.
        module: The AnsibleModule instance for error reporting.

    Returns:
        A list of NetBox contact group objects.
    """
    try:
        nb = pynetbox.api(url=netbox_url, token=netbox_token)
        return list(nb.tenancy.contact_groups.all())
    except Exception:
        module.fail_json(
            msg=f"Failed to retrieve contact groups from NetBox at '{netbox_url}'",
            exception=traceback.format_exc(),
        )


def get_netbox_contacts_for_group(
    netbox_url: str, netbox_token: str, group_id: int, module: AnsibleModule,
) -> list:
    """
    Retrieve all contacts belonging to a specific NetBox contact group.

    Args:
        netbox_url: The URL of the NetBox instance.
        netbox_token: The NetBox API token.
        group_id: The ID of the NetBox contact group.
        module: The AnsibleModule instance for error reporting.

    Returns:
        A list of NetBox contact objects.
    """
    try:
        nb = pynetbox.api(url=netbox_url, token=netbox_token)
        return list(nb.tenancy.contacts.filter(group_id=group_id))
    except Exception:
        module.fail_json(
            msg=f"Failed to retrieve contacts for group ID {group_id} from NetBox at '{netbox_url}'",
            exception=traceback.format_exc(),
        )


def get_authentik_groups(core_api, module: AnsibleModule) -> dict:
    """
    Retrieve all existing Authentik groups as a dict keyed by name.

    Args:
        core_api: An authenticated Authentik CoreApi instance.
        module: The AnsibleModule instance for error reporting.

    Returns:
        A dict mapping group name to group object.
    """
    try:
        groups_by_name: dict = {}
        page = 1
        while True:
            response = core_api.core_groups_list(page=page)
            for group in response.results:
                groups_by_name[group.name] = group
            if response.pagination.next is None or response.pagination.next == 0:
                break
            page += 1
        return groups_by_name
    except ApiException:
        module.fail_json(
            msg="Failed to retrieve groups from Authentik",
            exception=traceback.format_exc(),
        )


def get_authentik_users(core_api, module: AnsibleModule) -> dict:
    """
    Retrieve all existing Authentik users as a dict keyed by username.

    Args:
        core_api: An authenticated Authentik CoreApi instance.
        module: The AnsibleModule instance for error reporting.

    Returns:
        A dict mapping username to user object.
    """
    try:
        users_by_username: dict = {}
        page = 1
        while True:
            response = core_api.core_users_list(page=page)
            for user in response.results:
                users_by_username[user.username] = user
            if response.pagination.next is None or response.pagination.next == 0:
                break
            page += 1
        return users_by_username
    except ApiException:
        module.fail_json(
            msg="Failed to retrieve users from Authentik",
            exception=traceback.format_exc(),
        )


def get_group_members(core_api, group_pk: str, module: AnsibleModule) -> set:
    """
    Retrieve the set of user PKs that are members of the given Authentik group.

    Args:
        core_api: An authenticated Authentik CoreApi instance.
        group_pk: The UUID (pk) of the Authentik group.
        module: The AnsibleModule instance for error reporting.

    Returns:
        A set of integer user PKs.
    """
    try:
        response = core_api.core_groups_retrieve(group_pk)
        member_pks: set = set()
        if response.users_obj:
            for user_obj in response.users_obj:
                member_pks.add(user_obj.pk)
        return member_pks
    except ApiException:
        module.fail_json(
            msg=f"Failed to retrieve members of Authentik group '{group_pk}'",
            exception=traceback.format_exc(),
        )


def ensure_present(
    module: AnsibleModule,
    netbox_url: str,
    netbox_token: str,
    core_api,
) -> dict:
    """
    Ensure that all NetBox contact groups and contacts are present in Authentik.

    Args:
        module: The AnsibleModule instance.
        netbox_url: The URL of the NetBox instance.
        netbox_token: The NetBox API token.
        core_api: An authenticated Authentik CoreApi instance.

    Returns:
        A result dict with counts of created/changed objects and changed flag.
    """
    groups_created: int = 0
    users_created: int = 0
    memberships_created: int = 0

    contact_groups = get_netbox_contact_groups(netbox_url, netbox_token, module)

    existing_groups: dict = get_authentik_groups(core_api, module)
    existing_users: dict = get_authentik_users(core_api, module)

    for nb_group in contact_groups:
        group_name: str = nb_group.name

        # Create Authentik group if it does not exist yet
        if group_name not in existing_groups:
            if not module.check_mode:
                try:
                    new_group = core_api.core_groups_create(
                        authentik_client.GroupRequest(name=group_name),
                    )
                    existing_groups[group_name] = new_group
                except ApiException:
                    module.fail_json(
                        msg=f"Failed to create Authentik group '{group_name}'",
                        exception=traceback.format_exc(),
                    )
            groups_created += 1

        authentik_group = existing_groups.get(group_name)

        # Retrieve contacts for this group
        nb_contacts = get_netbox_contacts_for_group(
            netbox_url, netbox_token, nb_group.id, module,
        )

        # Determine current group members (only when not in check_mode and group exists)
        current_member_pks: set = set()
        if not module.check_mode and authentik_group is not None:
            current_member_pks = get_group_members(core_api, authentik_group.pk, module)

        for nb_contact in nb_contacts:
            full_name: str = nb_contact.name
            username: str = generate_username(full_name)
            email: str = nb_contact.email if nb_contact.email else ""

            # Create Authentik user if it does not exist yet
            if username not in existing_users:
                if not module.check_mode:
                    try:
                        new_user = core_api.core_users_create(
                            authentik_client.UserRequest(
                                username=username,
                                name=full_name,
                                path="netbox",
                                email=email,
                            ),
                        )
                        existing_users[username] = new_user
                    except ApiException:
                        module.fail_json(
                            msg=f"Failed to create Authentik user '{username}'",
                            exception=traceback.format_exc(),
                        )
                users_created += 1

            authentik_user = existing_users.get(username)

            # Assign user to group if not already a member
            if (
                not module.check_mode
                and authentik_group is not None
                and authentik_user is not None
                and authentik_user.pk not in current_member_pks
            ):
                try:
                    core_api.core_groups_add_user_create(
                        authentik_group.pk,
                        authentik_client.UserAccountRequest(pk=authentik_user.pk),
                    )
                    current_member_pks.add(authentik_user.pk)
                    memberships_created += 1
                except ApiException:
                    module.fail_json(
                        msg=(
                            f"Failed to add user '{username}' to Authentik group '{group_name}'"
                        ),
                        exception=traceback.format_exc(),
                    )
            elif module.check_mode and (
                authentik_group is None or authentik_user is None
            ):
                # In check_mode we cannot know membership state when objects do not exist yet
                memberships_created += 1

    changed: bool = (groups_created + users_created + memberships_created) > 0

    return dict(
        changed=changed,
        groups_created=groups_created,
        groups_deleted=0,
        users_created=users_created,
        users_deleted=0,
        memberships_created=memberships_created,
    )


def ensure_absent(
    module: AnsibleModule,
    netbox_url: str,
    netbox_token: str,
    core_api,
) -> dict:
    """
    Ensure that all NetBox contact groups and contacts are absent from Authentik.

    Users are deleted first, then groups.

    Args:
        module: The AnsibleModule instance.
        netbox_url: The URL of the NetBox instance.
        netbox_token: The NetBox API token.
        core_api: An authenticated Authentik CoreApi instance.

    Returns:
        A result dict with counts of deleted objects and changed flag.
    """
    groups_deleted: int = 0
    users_deleted: int = 0

    contact_groups = get_netbox_contact_groups(netbox_url, netbox_token, module)

    existing_groups: dict = get_authentik_groups(core_api, module)
    existing_users: dict = get_authentik_users(core_api, module)

    for nb_group in contact_groups:
        group_name: str = nb_group.name

        nb_contacts = get_netbox_contacts_for_group(
            netbox_url, netbox_token, nb_group.id, module,
        )

        # Delete users first
        for nb_contact in nb_contacts:
            username: str = generate_username(nb_contact.name)

            if username in existing_users:
                if not module.check_mode:
                    try:
                        core_api.core_users_destroy(existing_users[username].pk)
                    except ApiException:
                        module.fail_json(
                            msg=f"Failed to delete Authentik user '{username}'",
                            exception=traceback.format_exc(),
                        )
                    del existing_users[username]
                users_deleted += 1

        # Delete group
        if group_name in existing_groups:
            if not module.check_mode:
                try:
                    core_api.core_groups_destroy(existing_groups[group_name].pk)
                except ApiException:
                    module.fail_json(
                        msg=f"Failed to delete Authentik group '{group_name}'",
                        exception=traceback.format_exc(),
                    )
                del existing_groups[group_name]
            groups_deleted += 1

    changed: bool = (groups_deleted + users_deleted) > 0

    return dict(
        changed=changed,
        groups_created=0,
        groups_deleted=groups_deleted,
        users_created=0,
        users_deleted=users_deleted,
        memberships_created=0,
    )


def run_module() -> None:
    module: AnsibleModule = AnsibleModule(
        argument_spec=ARGSPEC,
        supports_check_mode=True,
    )

    if not HAS_PYNETBOX:
        module.fail_json(
            msg=missing_required_lib("pynetbox"),
            exception=PYNETBOX_IMPORT_ERROR,
        )

    if not HAS_AUTHENTIK_CLIENT:
        module.fail_json(
            msg=missing_required_lib("authentik-client"),
            exception=AUTHENTIK_CLIENT_IMPORT_ERROR,
        )

    netbox_url: str = module.params["netbox_url"]
    netbox_token: str = module.params["netbox_token"]
    authentik_url: str = module.params["authentik_url"].rstrip("/")
    authentik_token: str = module.params["authentik_token"]
    state: str = module.params["state"]
    validate_certs: bool = module.params["validate_certs"]
    ca_cert_path: Optional[str] = module.params["ca_cert_path"]

    # Ensure the URL points to the API root; append /api/v3 when not already present.
    if not authentik_url.endswith("/api/v3"):
        authentik_url = authentik_url + "/api/v3"

    configuration = authentik_client.Configuration(
        host=authentik_url,
        access_token=authentik_token,
        verify_ssl=validate_certs,
        ssl_ca_cert=ca_cert_path,
    )

    with authentik_client.ApiClient(configuration) as api_client:
        core_api = authentik_client.CoreApi(api_client)

        if state == "present":
            result: dict = ensure_present(module, netbox_url, netbox_token, core_api)
        else:
            result: dict = ensure_absent(module, netbox_url, netbox_token, core_api)

    module.exit_json(**result)


def main() -> None:
    run_module()


if __name__ == "__main__":
    main()

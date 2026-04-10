# sflab.homelab.vault_secrets

Ansible role that configures a KV-v2 secrets engine and an AppRole in HashiCorp Vault.

## Overview

This role performs the following actions:

1. Enables a KV-v2 secrets engine at a configurable mount point.
2. Creates a Vault ACL policy granting full access to the secrets engine.
3. Enables the AppRole auth method and creates an AppRole bound to the policy.
4. Reads the Role ID and generates a Secret ID, saving them to a JSON credentials file.

All operations are idempotent: repeated runs produce no changes and no duplicates.

## Requirements

- HashiCorp Vault must be initialized and unsealed (see `sflab.homelab.vault` role).
- The Vault init data file (containing the root token) must exist on the target host.
- The `hvac` Python library must be installed on the Ansible controller.

## Role Variables

| Variable | Default | Description |
|---|---|---|
| `vault_secrets_engine_name` | `secrets_homelab` | Mount point name for the KV-v2 secrets engine |
| `vault_secrets_approle_name` | `approle_secrets_homelab` | Name of the AppRole to create |
| `vault_secrets_policy_name` | `policy_secrets_homelab` | Name of the Vault ACL policy to create |
| `vault_secrets_output_file` | `/etc/vault.d/vault-secrets-approle.json` | Path to write AppRole credentials (Role ID + Secret ID) |
| `vault_secrets_init_data_file` | `/etc/vault.d/vault-init-data.json` | Path to the Vault init data file (contains root token) |
| `vault_secrets_api_protocol` | `https` | Protocol for the Vault API |
| `vault_secrets_api_host` | `{{ ansible_facts['default_ipv4']['address'] }}` | Vault API host |
| `vault_secrets_api_port` | `8200` | Vault API port |
| `vault_secrets_validate_certs` | `false` | Whether to validate TLS certificates |

## Output File Format

The credentials file (`vault_secrets_output_file`) is written with mode `0600` and contains:

```json
{
  "role_id": "...",
  "secret_id": "...",
  "vault_secrets_engine_name": "secrets_homelab",
  "vault_secrets_approle_name": "approle_secrets_homelab"
}
```

The file is only generated once. If the file already exists, the Secret ID generation step is skipped.

## Idempotency

| Component | Strategy |
|---|---|
| KV-v2 engine | `sflab.homelab.vault_kv_secret_engine` with `state: present` |
| Policy | GET check on `/v1/sys/policies/acl/{name}`, write only on 404 |
| AppRole auth method | GET check on `/v1/sys/auth`, enable only if `approle/` absent |
| AppRole role | GET check on `/v1/auth/approle/role/{name}`, write only on 404 |
| Credentials file | `ansible.builtin.stat` check, generate only if file absent |

## Example Playbook

```yaml
- name: Configure Vault secrets engine and AppRole
  hosts: vault_servers
  become: true

  roles:
    - role: sflab.homelab.vault_secrets
      vars:
        vault_secrets_engine_name: "secrets_homelab"
        vault_secrets_approle_name: "approle_secrets_homelab"
        vault_secrets_policy_name: "policy_secrets_homelab"
```

## Using the AppRole Credentials

After the role runs, you can use the credentials with `community.hashi_vault.vault_kv2_write`:

```yaml
- name: Load AppRole credentials
  ansible.builtin.slurp:
    src: /etc/vault.d/vault-secrets-approle.json
  register: _approle_creds_raw

- name: Parse AppRole credentials
  ansible.builtin.set_fact:
    _approle_creds: "{{ _approle_creds_raw.content | b64decode | from_json }}"

- name: Write a secret to Vault
  community.hashi_vault.vault_kv2_write:
    url: "https://vault.home.sflab.io:8200"
    auth_method: approle
    role_id: "{{ _approle_creds.role_id }}"
    secret_id: "{{ _approle_creds.secret_id }}"
    engine_mount_point: "{{ _approle_creds.vault_secrets_engine_name }}"
    path: my-service/config
    data:
      api_key: "my-secret-value"
```

## License

GPL-2.0-or-later

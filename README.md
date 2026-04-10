# Sflab Homelab Collection

[![GitHub Release](https://img.shields.io/github/v/release/sflab-io/ansible-collection-homelab)](https://github.com/sflab-io/ansible-collection-homelab/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains the `sflab.homelab` Ansible Collection for managing homelab infrastructure.

<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against the following Ansible versions: **>=2.15.0**.

Plugins and modules within a collection may be tested with only specific Ansible versions.
A collection may contain metadata that identifies these versions.
PEP440 is the schema used to describe the versions of Ansible.
<!--end requires_ansible-->

## External requirements

### Python packages

The following Python packages are required for the Vault modules:

| Package | Version | Purpose |
| --- | --- | --- |
| [hvac](https://hvac.readthedocs.io/) | `~=2.4.0` | HashiCorp Vault Python client |

Install via:

```bash
pip install -r requirements.txt
```

### Collection dependencies

The following Ansible collections are required and will be installed automatically by `ansible-galaxy`:

| Collection | Purpose |
| --- | --- |
| `ansible.utils` | Core utility plugins |
| `community.crypto` | Cryptography modules (TLS, certificates) |
| `community.general` | General-purpose modules |
| `community.hashi_vault` | HashiCorp Vault integration (base classes) |
| `netbox.netbox` | NetBox IPAM/DCIM integration |

## Included content

<!--start collection content-->
### Modules
Name | Description
--- | ---
[sflab.homelab.vault_init](https://github.com/sflab-io/ansible-collection-homelab/blob/main/docs/sflab.homelab.vault_init_module.rst)|Initializes a HashiCorp Vault instance.
[sflab.homelab.vault_kv_secret_engine](https://github.com/sflab-io/ansible-collection-homelab/blob/main/docs/sflab.homelab.vault_kv_secret_engine_module.rst)|Configures a KV secret engine in HashiCorp Vault
[sflab.homelab.vault_pki_generate_intermediate_csr](https://github.com/sflab-io/ansible-collection-homelab/blob/main/docs/sflab.homelab.vault_pki_generate_intermediate_csr_module.rst)|Generates an certificate signing request (CSR) for a PKI secret engine
[sflab.homelab.vault_pki_role](https://github.com/sflab-io/ansible-collection-homelab/blob/main/docs/sflab.homelab.vault_pki_role_module.rst)|Configures a PKI secret engine role in HashiCorp Vault
[sflab.homelab.vault_pki_root_ca_certificate](https://github.com/sflab-io/ansible-collection-homelab/blob/main/docs/sflab.homelab.vault_pki_root_ca_certificate_module.rst)|Configures a PKI root CA certificate in HashiCorp Vault
[sflab.homelab.vault_pki_secret_engine](https://github.com/sflab-io/ansible-collection-homelab/blob/main/docs/sflab.homelab.vault_pki_secret_engine_module.rst)|Configures a PKI secret engine in HashiCorp Vault
[sflab.homelab.vault_pki_set_signed_intermediate](https://github.com/sflab-io/ansible-collection-homelab/blob/main/docs/sflab.homelab.vault_pki_set_signed_intermediate_module.rst)|Sets a signed intermediate CA certificate for a PKI secret engine
[sflab.homelab.vault_pki_sign_intermediate](https://github.com/sflab-io/ansible-collection-homelab/blob/main/docs/sflab.homelab.vault_pki_sign_intermediate_module.rst)|Signs a certificate signing request as an intermediate CA in HashiCorp Vault
[sflab.homelab.vault_secrets_tune](https://github.com/sflab-io/ansible-collection-homelab/blob/main/docs/sflab.homelab.vault_secrets_tune_module.rst)|Tunes configuration parameters for a HashiCorp Vault secrets engine
[sflab.homelab.vault_unseal](https://github.com/sflab-io/ansible-collection-homelab/blob/main/docs/sflab.homelab.vault_unseal_module.rst)|Unseals a HashiCorp Vault instance
[sflab.homelab.vault_write](https://github.com/sflab-io/ansible-collection-homelab/blob/main/docs/sflab.homelab.vault_write_module.rst)|Execute a write operation in HashiCorp Vault

<!--end collection content-->

### Roles

| Role | Description |
| --- | --- |
| `sflab.homelab.common` | Common infrastructure setup and base configuration |
| `sflab.homelab.docker` | Docker installation with Portainer, Traefik, and Whoami |
| `sflab.homelab.firewall` | OPNsense firewall configuration via JSON criteria files |
| `sflab.homelab.netbox` | NetBox IPAM/DCIM deployment and configuration |
| `sflab.homelab.netbox_init` | NetBox initial data population |
| `sflab.homelab.pki` | PKI infrastructure via HashiCorp Vault (root CA, intermediate CA) |
| `sflab.homelab.self_signed_certificate` | Self-signed TLS certificate generation |
| `sflab.homelab.technitium` | Technitium DNS server (primary/secondary) |
| `sflab.homelab.vault` | HashiCorp Vault installation and initialization |
| `sflab.homelab.vault_secrets` | HashiCorp Vault secrets management |

## Using this collection

### Install from GitHub

Install a specific release directly from GitHub:

```bash
ansible-galaxy collection install \
  git+https://github.com/sflab-io/ansible-collection-homelab.git,v0.1.0
```

Or download and install a release archive:

```bash
ansible-galaxy collection install \
  https://github.com/sflab-io/ansible-collection-homelab/releases/download/v0.1.0/sflab-homelab-0.1.0.tar.gz
```

### Install from Ansible Galaxy

```bash
ansible-galaxy collection install sflab.homelab
```

### Install via requirements.yml

```yaml
collections:
  - name: sflab.homelab
    source: https://github.com/sflab-io/ansible-collection-homelab
    type: git
    version: v0.1.0
```

```bash
ansible-galaxy collection install -r requirements.yml
```

### Upgrade

```bash
ansible-galaxy collection install sflab.homelab --upgrade
```

## Development

### Prerequisites

- [mise](https://mise.jdx.dev) — manages Python, uv, and Dagger versions
- [Dagger](https://dagger.io) v0.20.3 — containerized build and release (installed via mise)
- Python 3.x

### Setup

```bash
# Clone the repository
git clone https://github.com/sflab-io/ansible-collection-homelab.git
cd ansible-collection-homelab

# Install all tools and dependencies (triggered automatically on directory enter)
mise install
```

### Available Tasks

```bash
mise run ansible:build      # Build collection archive via Dagger → ./dist/
mise run ansible:release    # Build and publish a GitHub release
mise run python:install-requirements  # Install Python runtime dependencies
```

### Testing

```bash
# Unit tests
pytest tests/unit/

# Integration tests (requires molecule)
pytest tests/integration/

# Run a specific molecule scenario
molecule test -s integration_hello_world
```

### Code Quality

```bash
pre-commit run --all-files  # Run all pre-commit hooks
black .                     # Format Python code
prettier --write .          # Format YAML/TOML
```

## Release notes

See the [changelog](https://github.com/sflab-io/ansible-collection-homelab/blob/main/CHANGELOG.rst).

Releases are published at [GitHub Releases](https://github.com/sflab-io/ansible-collection-homelab/releases).

## More information

- [Ansible User guide](https://docs.ansible.com/ansible/devel/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/devel/dev_guide/index.html)
- [Ansible Collections documentation](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html)
- [HashiCorp Vault documentation](https://developer.hashicorp.com/vault/docs)
- [Issues](https://github.com/sflab-io/ansible-collection-homelab/issues)

## Licensing

MIT License.

See [LICENSE](LICENSE) to see the full text.

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Collection Overview

This is `sflab.homelab`, an Ansible Collection for managing homelab infrastructure. The collection includes:

- **Roles**: `common`, `docker`, `firewall`, `netbox`, `netbox_init`, `pki`, `self_signed_certificate`, `technitium` (DNS), `vault` (HashiCorp Vault), and `vault_secrets`
- **Plugins**: Action plugins, doc fragments, filters, lookups, modules (Vault PKI), and module utilities
- **Testing**: Unit tests (pytest) and integration tests (molecule)
- **Repository**: [sflab-io/ansible-collection-homelab](https://github.com/sflab-io/ansible-collection-homelab)

## Development Environment Setup

### Prerequisites

- **Python 3.x** - Required for testing and tooling
- **Ansible 2.15+** - Collection minimum version (defined in `meta/runtime.yml`)
- **ansible-galaxy** - For building and installing collections
- **mise** - Tool version manager (manages uv, Python, and Dagger)
- **Dagger v0.20.3** - Used for containerized builds and releases (managed via mise)

### Installing Development Dependencies

The collection uses `mise` with `uv` for Python environment management:

```bash
# Install mise first (https://mise.jdx.dev)
mise install        # Installs tools defined in mise.toml (uv, dagger, etc.)
```

On entering the project directory, mise automatically:

- Installs all tools (`mise i`)
- Installs pre-commit hooks
- Runs `mise run python:install-requirements` (installs `requirements.txt` via uv)

Alternatively, install manually:

```bash
# Runtime dependencies
pip install -r requirements.txt       # hvac~=2.4.0

# Testing dependencies
pip install -r test-requirements.txt  # pytest-ansible, pytest-xdist, molecule

# Install pre-commit
pip install pre-commit
pre-commit install
```

## Development Commands

### Mise Tasks

The project uses mise tasks for all common operations:

```bash
mise run ansible:build      # Build collection archive via Dagger → outputs to ./dist/
mise run ansible:release    # Build + create GitHub release (sflab-io/ansible-collection-homelab)
mise run python:install-requirements  # Install requirements.txt via uv
```

The `ansible:release` task:

- Reads version/namespace/name from `galaxy.yml`
- Builds a clean archive via Dagger (`github.com/stuttgart-things/dagger/ansible@v0.84.0`)
- Creates a GitHub release using `gh auth token` automatically

### Building the Collection (manual)

```bash
ansible-galaxy collection build
```

This creates a tarball `sflab-homelab-<version>.tar.gz` in the current directory.

### Installing Locally

```bash
ansible-galaxy collection install sflab-homelab-*.tar.gz --force
```

Use `--force` to overwrite existing installations during development.

### Testing

**Prerequisites**: Install test dependencies first (from `test-requirements.txt`)

#### Run Unit Tests

```bash
pytest tests/unit/
```

Run with verbose output (already configured in `pyproject.toml`):

```bash
pytest -vvv tests/unit/
```

Run specific test file:

```bash
pytest tests/unit/test_basic.py
```

#### Run Integration Tests

```bash
pytest tests/integration/
```

Integration tests use molecule scenarios located in `extensions/molecule/`.

#### Run Molecule Scenarios Directly

```bash
molecule test -s integration_hello_world
```

Available scenarios:

- `integration_hello_world` - Basic integration test scenario

### Linting and Formatting

Pre-commit hooks are configured. Install them:

```bash
pre-commit install
```

Run all hooks manually:

```bash
pre-commit run --all-files
```

#### Pre-commit Hooks Include:

- **gitleaks** - Secret/credential scanning (v8.30.0)
- **update-docs** - Auto-generate documentation (ansible-network/collection_prep v1.1.2)
- **check-merge-conflict** - Detect merge conflict markers
- **check-symlinks** - Check for broken symlinks
- **debug-statements** - Detect Python debug statements
- **end-of-file-fixer** - Ensure files end with newline
- **trailing-whitespace** - Remove trailing whitespace
- **add-trailing-comma** - Add trailing commas in Python
- **prettier** - Format YAML, TOML, etc.

Note: `no-commit-to-branch` (blocking commits to main) is currently disabled. `isort`, `black`, and `flake8` are not part of the pre-commit hooks — run them manually if needed.

#### Manual Code Quality Commands

- **Black** (line length: 100): `black .`
- **isort**: `isort --filter-files .`
- **Flake8**: `flake8`
- **Prettier** (YAML, TOML, etc.): `prettier --write .`

## Architecture

### Collection Structure

```
sflab.homelab/
├── roles/                    # Ansible roles
│   ├── common/               # Common infrastructure setup
│   ├── docker/               # Docker with Portainer, Traefik, Whoami
│   ├── firewall/             # OPNsense firewall configuration
│   ├── netbox/               # NetBox IPAM/DCIM
│   ├── netbox_init/          # NetBox initialization
│   ├── pki/                  # PKI via HashiCorp Vault
│   ├── self_signed_certificate/ # Self-signed TLS certificates
│   ├── technitium/           # Technitium DNS server (primary/secondary)
│   ├── vault/                # HashiCorp Vault installation
│   └── vault_secrets/        # HashiCorp Vault secrets management
├── plugins/                  # Custom Ansible plugins
│   ├── action/               # Action plugins
│   ├── cache/                # Cache plugins
│   ├── doc_fragments/        # Shared documentation fragments
│   ├── filter/               # Jinja2 filter plugins
│   ├── inventory/            # Inventory plugins
│   ├── lookup/               # Lookup plugins
│   ├── modules/              # Ansible modules (Vault PKI)
│   ├── module_utils/         # Shared utilities for modules
│   ├── plugin_utils/         # Shared utilities for plugins
│   ├── sub_plugins/          # Sub-plugins (nested plugin support)
│   └── test/                 # Test plugins
├── tests/
│   ├── unit/                 # Pytest unit tests
│   └── integration/          # Pytest integration tests
├── extensions/
│   ├── molecule/             # Molecule scenarios for integration testing
│   │   ├── integration_hello_world/  # Example integration test
│   │   └── utils/            # Shared utilities and playbooks
│   └── eda/                  # Event-Driven Ansible rulebooks
├── docs/
│   └── docsite/              # Documentation source files
│       └── links.yml         # Documentation links
├── meta/                     # Collection metadata
├── dist/                     # Built collection archives (generated, not committed)
└── .dagger/                  # Local Dagger module (TypeScript, auto-generated scaffold)
```

### Role Architecture

All roles follow standard Ansible role structure with these common elements:

- `tasks/main.yml` - Entry point orchestrating task execution
- `defaults/main.yml` - Default variables (user-configurable)
- `vars/main.yml` - Role-specific variables (internal)
- `meta/argument_specs.yml` - Role argument specifications (Ansible 2.11+)
- `handlers/main.yml` - Event handlers
- `templates/` - Jinja2 templates
- `files/` - Static files

#### Technitium DNS Role Pattern

**Type**: Implementation role with primary/secondary support

The `technitium` role installs and configures Technitium DNS server:

- **Primary server**: `tasks/init_primary.yml` → `tasks/config_primary.yml`
- **Secondary server**: `tasks/config_secondary.yml`

**Task files**:

- `tasks/main.yml` - Orchestration
- `tasks/install.yml` - Installation
- `tasks/init_primary.yml` - Primary server initialization
- `tasks/config_primary.yml` - Primary server configuration
- `tasks/config_secondary.yml` - Secondary server configuration

#### Vault Role Pattern

**Type**: Implementation role

The Vault role implements HashiCorp Vault installation and configuration directly.

**Task files** (executed via `import_tasks`):

- `tasks/main.yml` - Orchestrates task sequence
- `tasks/validate/main.yml` - Pre-flight validation (listener, raft)
- `tasks/user.yml` - Create vault user
- `tasks/directories.yml` - Create required directories
- `tasks/install.yml` - Install Vault binary
- `tasks/service.yml` - Configure systemd service
- `tasks/init.yml` - Vault initialization
- `tasks/uninit.yml` - Vault uninitialization

**Pattern**: Sequential task execution with validation, following a setup-install-configure workflow.

#### Firewall Role Pattern

**Type**: Implementation role for OPNsense

Manages OPNsense firewall configuration via JSON criteria files.

**Task files**:

- `tasks/main.yml`, `tasks/validate.yml`, `tasks/aliases.yml`, `tasks/dhcp.yml`,
  `tasks/gateways.yml`, `tasks/nat.yml`, `tasks/rules.yml`, `tasks/shaper.yml`,
  `tasks/tls.yml`, `tasks/vlans.yml`

#### PKI Role Pattern

**Type**: Implementation role using HashiCorp Vault PKI secret engine

Configures Vault PKI for root CA, intermediate CA, and certificate issuance.

**Task files**: `tasks/configure_secret_engine_root_ca.yml`, `tasks/configure_secret_engine_intermediate_ca.yml`,
`tasks/generate_root_ca_certificate.yml`, `tasks/generate_intermediate_ca_certificate.yml`,
`tasks/sign_intermediate_csr.yml`, `tasks/create_pki_roles.yml`, `tasks/issue_vault_certificate.yml`,
`tasks/configure_acme_support.yml`, `tasks/load_vault_init_data.yml`

### Plugin Development

All plugins follow standard Ansible plugin interfaces:

- **Action plugins** extend `ActionBase` from `ansible.plugins.action`
- **Filter plugins** return a dict of filter functions
- **Lookup plugins** extend `LookupBase` from `ansible.plugins.lookup`
- **Modules** use `AnsibleModule` with argument specs
- **Test plugins** return a dict of test functions
- **Cache plugins** implement cache interface
- **Inventory plugins** extend inventory base classes

**Plugin Locations**:

- `plugins/action/` - Action plugins
- `plugins/filter/` - Jinja2 filter plugins
- `plugins/lookup/` - Lookup plugins
- `plugins/modules/` - Ansible modules: `vault_init.py`, `vault_unseal.py`, `vault_write.py`, `vault_secrets_tune.py`, `vault_kv_secret_engine.py`, `vault_pki_secret_engine.py`, `vault_pki_root_ca_certificate.py`, `vault_pki_generate_intermediate_csr.py`, `vault_pki_sign_intermediate.py`, `vault_pki_set_signed_intermediate.py`, `vault_pki_role.py`
- `plugins/test/` - Test plugins
- `plugins/cache/` - Cache plugins
- `plugins/inventory/` - Inventory plugins
- `plugins/module_utils/` - Shared utilities (`_vault_module.py`, `_vault_cert.py`, `_vault_module_error.py`, `_vault_secret_engine_module.py`, `_timeparse.py`)
- `plugins/plugin_utils/` - Shared utilities for plugins
- `plugins/sub_plugins/` - Sub-plugins (nested plugin support)
- `plugins/doc_fragments/` - Shared documentation fragments: `auth.py`, `connection.py`, `action_group.py`, `engine_mount.py`, `check_mode.py`, `check_mode_none.py`, `requirements.py`, `secret_engine.py`

### Testing Strategy

**Unit Tests** (`tests/unit/`):

- Framework: pytest
- Configuration: `pyproject.toml`
  - Parallel execution enabled (`-n 2` via pytest-xdist)
  - Verbose output (`-vvv`)
  - Warning filter for AnsibleCollectionFinder
- Test files:
  - `tests/unit/test_basic.py` - Basic unit tests
  - `tests/unit/__init__.py` - Package initialization
- Focus: Test individual functions and classes in isolation

**Integration Tests** (`tests/integration/`):

- Framework: pytest with pytest-ansible and molecule
- Test files:
  - `tests/integration/test_integration.py` - Integration test runner
  - `tests/integration/__init__.py` - Package initialization
  - `tests/integration/targets/hello_world/tasks/main.yml` - Hello world target
- Scenarios: Located in `extensions/molecule/`
- Execution: Tests run molecule scenarios to verify end-to-end functionality

**Molecule Configuration**:

- **Scenarios**: Located in `extensions/molecule/`
  - `integration_hello_world/` - Basic integration test scenario
    - `molecule.yml` - Scenario configuration
  - `utils/` - Shared utilities and playbooks
- **Testing Approach**:
  - Scenarios define test workflows with molecule lifecycle phases
  - Uses `ANSIBLE_COLLECTIONS_PATH` to test the collection in-place
  - Platform `name: na` indicates non-container testing (local execution)

**Test Execution Flow**:

1. Run pytest which discovers integration tests
2. Integration tests invoke molecule scenarios
3. Molecule executes converge playbooks
4. Verify assertions pass

### Collection Dependencies

**Runtime dependencies** (`requirements.txt`):

- `hvac~=2.4.0` - HashiCorp Vault Python client (used by Vault modules)
- `antsibull-changelog~=0.35.0` - Changelog management

**Test dependencies** (`test-requirements.txt`):

- `pytest-ansible`, `pytest-xdist`, `molecule`

**Collection dependencies** (defined in `galaxy.yml`):

- `ansible.utils` - Core utility plugins
- `community.crypto` - Cryptography modules
- `community.general` - General-purpose modules
- `community.hashi_vault` - HashiCorp Vault integration (base classes for modules)
- `netbox.netbox` - NetBox IPAM/DCIM integration

**Dependency management**:

- Runtime dependencies in `requirements.txt`
- Test dependencies in `test-requirements.txt`
- Collection-level dependencies in `galaxy.yml`
- Role-level dependencies in `roles/*/meta/main.yml`

## Documentation Generation

The collection uses `ansible-network/collection_prep` pre-commit hook (v1.1.2) to auto-generate documentation.

**Auto-generated sections in README.md**:

- `<!--start requires_ansible-->...<!--end requires_ansible-->` - Minimum Ansible version
- `<!--start collection content-->...<!--end collection content-->` - Collection content inventory

**Documentation files**:

- `docs/docsite/links.yml` - Documentation links and references
- `README.md` - Main collection documentation (partially auto-generated)
- `roles/*/README.md` - Individual role documentation

**Pre-commit hook**: The `update-docs` hook runs automatically on commit to keep documentation synchronized with code.

## Important Conventions

### Git Workflow

- **Main branch**: Direct commits to `main` are currently allowed (`no-commit-to-branch` hook is disabled)
- **Development workflow**: Feature branches recommended; merge to main
- **Commit requirements**: All pre-commit hooks must pass (gitleaks, update-docs, prettier, etc.)
- **GitHub repository**: [sflab-io/ansible-collection-homelab](https://github.com/sflab-io/ansible-collection-homelab)

### Role Development

- **Variable naming**: Use role-prefixed variable names (e.g., `vault_my_variable`, `technitium_my_variable`)
- **Argument specs**: Define in `meta/argument_specs.yml` for:
  - Automatic validation
  - Auto-generated documentation
  - Type checking
- **Role metadata**: Update `meta/main.yml` with dependencies and galaxy_info

### Python Code Style

- **Line length**: 100 characters (Black configuration in `pyproject.toml`)
- **Type hints**: Required for all functions (example: `def test_basic() -> None`)
- **Import order**: Managed by isort with `--filter-files` flag
- **Formatting**: Enforced by Black formatter
- **Linting**: Checked by Flake8
- **Trailing commas**: Added automatically by add-trailing-comma hook

### YAML/TOML Style

- **Formatter**: Prettier with prettier-plugin-toml
- **Consistency**: Applied automatically via pre-commit
- **File endings**: Newline at end of file (end-of-file-fixer)
- **Trailing whitespace**: Removed automatically

### Testing Requirements

- **Unit tests**: Required for all Python code
- **Integration tests**: Required for roles and modules
- **Test configuration**: Defined in `pyproject.toml`
- **Pytest options**: `-vvv -n 2 --log-level WARNING --color yes`
- **Warning filters**: `AnsibleCollectionFinder has already been configured` is ignored globally

### Dagger Integration

The project uses Dagger for containerized builds and GitHub releases:

- **External module**: `github.com/stuttgart-things/dagger/ansible@v0.84.0`
  - `build` - Builds the collection archive inside a container
  - `github-release` - Creates a GitHub release with the archive
- **Local module**: `.dagger/src/index.ts` - Auto-generated TypeScript scaffold (not actively used)
- **`.daggerignore`** - Excludes `.venv`, `dist`, `.git`, etc. from Dagger file uploads

### Code Quality Gates

Pre-commit hooks enforce:

- No secrets or credentials (gitleaks)
- No merge conflict markers
- No broken symlinks
- No Python debug statements (e.g., `pdb.set_trace()`)
- Proper file endings
- No trailing whitespace
- Formatted YAML/TOML (Prettier)
- Trailing commas in Python (add-trailing-comma)

======================================
Sflab Homelab Collection Release Notes
======================================

.. contents:: Topics

v0.1.0
======

Release Summary
---------------

This is the first release of the Sflab Homelab Collection, a curated set of Ansible roles and playbooks designed to help you manage your homelab infrastructure efficiently.
This release includes a variety of roles for common homelab services, as well as playbooks to get you started quickly.

New Modules
-----------

- vault_init - Initializes a HashiCorp Vault instance.
- vault_kv_secret_engine - Configures a KV secret engine in HashiCorp Vault
- vault_pki_generate_intermediate_csr - Generates an certificate signing request (CSR) for a PKI secret engine
- vault_pki_role - Configures a PKI secret engine role in HashiCorp Vault
- vault_pki_root_ca_certificate - Configures a PKI root CA certificate in HashiCorp Vault
- vault_pki_secret_engine - Configures a PKI secret engine in HashiCorp Vault
- vault_pki_set_signed_intermediate - Sets a signed intermediate CA certificate for a PKI secret engine
- vault_pki_sign_intermediate - Signs a certificate signing request as an intermediate CA in HashiCorp Vault
- vault_secrets_tune - Tunes configuration parameters for a HashiCorp Vault secrets engine
- vault_unseal - Unseals a HashiCorp Vault instance
- vault_write - Execute a write operation in HashiCorp Vault

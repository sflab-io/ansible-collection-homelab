.. _sflab.homelab.vault_pki_generate_intermediate_csr_module:


*************************************************
sflab.homelab.vault_pki_generate_intermediate_csr
*************************************************

**Generates an certificate signing request (CSR) for a PKI secret engine**


Version added: 0.1.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Generates an L(certificate signing request (CSR),https://hvac.readthedocs.io/en/stable/usage/secrets_engines/pki.html#generate-intermediate) for a PKI secret engine.
- This module is not idempotent, as it generates a new CSR (and possibly private key) each time it is run.
- If the CSR is successfully generated, the CSR is returned.



Requirements
------------
The below requirements are needed on the host that executes this module.

- ``hvac`` (`Python library <https://hvac.readthedocs.io/en/stable/overview.html>`_)


Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="2">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>add_basic_constraints</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Whether to include the basic constraints extension in the certificate signing request (CSR).</div>
                        <div>If set to V(true), the CSR will include the basic constraints extension.</div>
                        <div>If not provided, the CSR will not include the basic constraints extension.</div>
                        <div>This option is only needed for compatibility with certain systems, such as Active Directory Certificate Services as the signing CA.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>alt_names</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The list of Subject Alternative Names (SANs) to include in the certificate signing request (CSR).</div>
                        <div>Each element should be a hostname (DNS name) or an email address.</div>
                        <div>If this does not include the common name and O(exclude_cn_from_sans=false), the common name will be added to the list of SANs.</div>
                        <div>If not provided, an empty list will be used.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>auth_method</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>token</b>&nbsp;&larr;</div></li>
                                    <li>userpass</li>
                                    <li>ldap</li>
                                    <li>approle</li>
                                    <li>jwt</li>
                                    <li>cert</li>
                                    <li>none</li>
                        </ul>
                </td>
                <td>
                        <div>Authentication method to be used.</div>
                        <div><code>none</code> auth method was added in collection version <code>0.1.0</code>.</div>
                        <div><code>cert</code> auth method was added in collection version <code>0.1.0</code>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ca_cert</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Path to certificate to use for authentication.</div>
                        <div>If not specified by any other means, the <code>VAULT_CACERT</code> environment variable will be used.</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: cacert</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>cert_auth_private_key</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">path</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 0.1.0</div>
                </td>
                <td>
                </td>
                <td>
                        <div>For <code>cert</code> auth, path to the private key file to authenticate with, in PEM format.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>cert_auth_public_key</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">path</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 0.1.0</div>
                </td>
                <td>
                </td>
                <td>
                        <div>For <code>cert</code> auth, path to the certificate file to authenticate with, in PEM format.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>common_name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The requested common name (CN) attribute for the certificate signing request (CSR).</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>country</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The Country (C) values to include in the CA certificate.</div>
                        <div>If not provided, this defaults to an empty list on new roles.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>engine_mount_point</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The path where the secret backend is mounted.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>exclude_cn_from_sans</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Whether to exclude the common name from the Subject Alternate Names (SANs).</div>
                        <div>If set to V(true), the given O(common_name) will not be added to the list of SANs.</div>
                        <div>If set to V(false), the given O(common_name) will be added to the list of SANs and parsed as a DNS name or email address.</div>
                        <div>If not provided, the common name will not be excluded.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>format</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>pem</li>
                                    <li>der</li>
                                    <li>pem_bundle</li>
                        </ul>
                </td>
                <td>
                        <div>The format of the returned certificate data.</div>
                        <div>If V(pem_bundle), the certificate will contain the private key and certificate concatenated.</div>
                        <div>If not provided, the certificate will be returned in PEM format.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ip_sans</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The list of IP Subject Alternative Names (IP SANs) to include in the certificate signing request (CSR).</div>
                        <div>Each element should be a valid IP address.</div>
                        <div>If not provided, an empty list will be used.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>jwt</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The JSON Web Token (JWT) to use for JWT authentication to Vault.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>key_bits</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>224</li>
                                    <li>256</li>
                                    <li>384</li>
                                    <li>521</li>
                                    <li>2048</li>
                                    <li>3072</li>
                                    <li>4096</li>
                                    <li>8192</li>
                        </ul>
                </td>
                <td>
                        <div>The number of bits to use for generated keys.</div>
                        <div>If O(key_type=rsa), the allowed values are V(2048), V(3072), V(4096), and V(8192).</div>
                        <div>If not provided and O(key_type=rsa), this defaults to V(2048) on new roles.</div>
                        <div>If O(key_type=ec), the allowed values are V(224), V(256), V(384), and V(521).</div>
                        <div>If not provided and O(key_type=ec), this defaults to V(256) on new roles.</div>
                        <div>If O(key_type=ed25519), this should not be provided.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>key_name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The name of the private key to store in the storage backend.</div>
                        <div>Should only be defined if O(type=internal).</div>
                        <div>If set to V(default), the private key will be stored as the default key.</div>
                        <div>If not provided, the private key will not be stored as the default key.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>key_ref</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The identifier of the existing private key to use for generating the certificate signing request (CSR).</div>
                        <div>Should only be provided if O(type=existing).</div>
                        <div>If a private key with this identifier does not exist, the module will fail.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>key_type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>rsa</li>
                                    <li>ed25519</li>
                                    <li>ec</li>
                        </ul>
                </td>
                <td>
                        <div>The type of private key to generate.</div>
                        <div>Should only be defined if O(type=internal).</div>
                        <div>If HashiCorp Vault is running in FIPS mode, using the V(ed25519) value will cause the module to fail, as it is not a certified algorithm.</div>
                        <div>If not provided, the private key will be generated using the RSA algorithm.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>key_usage</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>DigitalSignature</li>
                                    <li>ContentCommitment</li>
                                    <li>KeyEncipherment</li>
                                    <li>DataEncipherment</li>
                                    <li>KeyAgreement</li>
                                    <li><div style="color: blue"><b>CertSign</b>&nbsp;&larr;</div></li>
                                    <li><div style="color: blue"><b>CRLSign</b>&nbsp;&larr;</div></li>
                                    <li>EncipherOnly</li>
                                    <li>DecipherOnly</li>
                        </ul>
                        <b>Default:</b><br/><div style="color: blue">["CertSign", "CRLSign"]</div>
                </td>
                <td>
                        <div>The list of key usage constraints to include in the certificate signing request (CSR).</div>
                        <div>If not provided, no key usage constraints will be included in the CSR.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>locality</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The Locality (L) values to include in the CA certificate.</div>
                        <div>If not provided, this defaults to an empty list on new roles.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>mount_point</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Vault mount point.</div>
                        <div>If not specified, the default mount point for a given auth method is used.</div>
                        <div>Does not apply to token authentication.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>namespace</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Vault namespace where secrets reside. This option requires HVAC 0.7.0+ and Vault 0.11+.</div>
                        <div>Optionally, this may be achieved by prefixing the authentication mount point and/or secret path with the namespace (e.g <code>mynamespace/secret/mysecret</code>).</div>
                        <div>If environment variable <code>VAULT_NAMESPACE</code> is set, its value will be used last among all ways to specify <em>namespace</em>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>organization</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The Organization (O) values to include in the CA certificate.</div>
                        <div>If not provided, this defaults to an empty list on new roles.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>other_sans</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The list of custom OID/UTF8-string SANs.</div>
                        <div>If not provided, an empty list will be used.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>oid</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The OID for the custom SAN.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>utf8</b>&nbsp;&larr;</div></li>
                        </ul>
                </td>
                <td>
                        <div>The type of the custom SAN.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>value</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The value of the custom SAN.</div>
                </td>
            </tr>

            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ou</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The Organizational Unit (OU) values to include in the CA certificate.</div>
                        <div>If not provided, this defaults to an empty list on new roles.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>password</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Authentication password.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>postal_code</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The Postal Code values to include in the CA certificate.</div>
                        <div>If not provided, this defaults to an empty list on new roles.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>private_key_format</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>der</b>&nbsp;&larr;</div></li>
                                    <li>pkcs8</li>
                        </ul>
                </td>
                <td>
                        <div>The format for marshaling the private key.</div>
                        <div>If set to V(der) and O(format=pem) or O(format=pem_bundle), the private key will be returned in PEM-encoded DER format.</div>
                        <div>If set to V(der) and O(format=der), the private key will be returned in base64-encoded DER format.</div>
                        <div>If set to V(pkcs8), the private key will be returned in PEM-encoded PKCS8 format.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>province</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The Province or State (ST) values to include in the CA certificate.</div>
                        <div>If not provided, this defaults to an empty list on new roles.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>proxies</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">raw</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 0.1.0</div>
                </td>
                <td>
                </td>
                <td>
                        <div>URL(s) to the proxies used to access the Vault service.</div>
                        <div>It can be a string or a dict.</div>
                        <div>If it&#x27;s a dict, provide the scheme (eg. <code>http</code> or <code>https</code>) as the key, and the URL as the value.</div>
                        <div>If it&#x27;s a string, provide a single URL that will be used as the proxy for both <code>http</code> and <code>https</code> schemes.</div>
                        <div>A string that can be interpreted as a dictionary will be converted to one (see examples).</div>
                        <div>You can specify a different proxy for HTTP and HTTPS resources.</div>
                        <div>If not specified, <a href='https://requests.readthedocs.io/en/master/user/advanced/#proxies'>environment variables from the Requests library</a> are used.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>retries</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">raw</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 0.1.0</div>
                </td>
                <td>
                </td>
                <td>
                        <div>Allows for retrying on errors, based on the <a href='https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#urllib3.util.Retry'>Retry class in the urllib3 library</a>.</div>
                        <div>This collection defines recommended defaults for retrying connections to Vault.</div>
                        <div>This option can be specified as a positive number (integer) or dictionary.</div>
                        <div>If this option is not specified or the number is <code>0</code>, then retries are disabled.</div>
                        <div>A number sets the total number of retries, and uses collection defaults for the other settings.</div>
                        <div>A dictionary value is used directly to initialize the <code>Retry</code> class, so it can be used to fully customize retries.</div>
                        <div>For detailed information on retries, see the collection User Guide.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>retry_action</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 0.1.0</div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>ignore</li>
                                    <li><div style="color: blue"><b>warn</b>&nbsp;&larr;</div></li>
                        </ul>
                </td>
                <td>
                        <div>Controls whether and how to show messages on <em>retries</em>.</div>
                        <div>This has no effect if a request is not retried.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>role_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Vault Role ID or name. Used in <code>approle</code> and <code>cert</code> auth methods.</div>
                        <div>For <code>cert</code> auth, if no <em>role_id</em> is supplied, the default behavior is to try all certificate roles and return any one that matches.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>secret_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Secret ID to be used for Vault AppRole authentication.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>serial_number</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The serial number of the CA certificate.</div>
                        <div>If you want more than one, specify alternative names in the alt_names map using OID 2.5.4.5.</div>
                        <div>If not provided, HashiCorp Vault will generate a random serial number for the certificate.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>signature_bits</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>256</li>
                                    <li>384</li>
                                    <li>512</li>
                        </ul>
                </td>
                <td>
                        <div>The signature algorithm bit length for the signed certificates.</div>
                        <div>Should only be provided when O(key_type=rsa).</div>
                        <div>If not provided and O(key_type=rsa), this defaults to V(2048).</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>street_address</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The Street Address values to include in the CA certificate.</div>
                        <div>If not provided, this defaults to an empty list on new roles.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>timeout</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 0.1.0</div>
                </td>
                <td>
                </td>
                <td>
                        <div>Sets the connection timeout in seconds.</div>
                        <div>If not set, then the <code>hvac</code> library&#x27;s default is used.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>token</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Vault token. Token may be specified explicitly, through the listed [env] vars, and also through the <code>VAULT_TOKEN</code> env var.</div>
                        <div>If no token is supplied, explicitly or through env, then the plugin will check for a token file, as determined by <em>token_path</em> and <em>token_file</em>.</div>
                        <div>The order of token loading (first found wins) is <code>token param -&gt; ansible var -&gt; ANSIBLE_HASHI_VAULT_TOKEN -&gt; VAULT_TOKEN -&gt; token file</code>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>token_file</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">".vault-token"</div>
                </td>
                <td>
                        <div>If no token is specified, will try to read the token from this file in <em>token_path</em>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>token_path</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>If no token is specified, will try to read the <em>token_file</em> from this path.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>token_validate</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 0.1.0</div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>For token auth, will perform a <code>lookup-self</code> operation to determine the token&#x27;s validity before using it.</div>
                        <div>Disable if your token does not have the <code>lookup-self</code> capability.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>internal</b>&nbsp;&larr;</div></li>
                                    <li>existing</li>
                        </ul>
                </td>
                <td>
                        <div>The private key type to use for generating the certificate signing request (CSR).</div>
                        <div>If set to V(internal), the private key will be generated by HashiCorp Vault and stored.</div>
                        <div>If set to V(existing), the O(key_ref) option is required and the private key with that identifier will be used.</div>
                        <div>KMS-backed keys are not supported with this module.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>uri_sans</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The list of URI Subject Alternative Names (URI SANs) to include in the certificate signing request (CSR).</div>
                        <div>Each element should be a valid URI.</div>
                        <div>If not provided, an empty list will be used.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>url</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>URL to the Vault service.</div>
                        <div>If not specified by any other means, the value of the <code>VAULT_ADDR</code> environment variable will be used.</div>
                        <div>If <code>VAULT_ADDR</code> is also not defined then an error will be raised.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>username</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Authentication user name.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>validate_certs</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Controls verification and validation of SSL certificates, mostly you only want to turn off with self signed ones.</div>
                        <div>Will be populated with the inverse of <code>VAULT_SKIP_VERIFY</code> if that is set and <em>validate_certs</em> is not explicitly provided.</div>
                        <div>Will default to <code>true</code> if neither <em>validate_certs</em> or <code>VAULT_SKIP_VERIFY</code> are set.</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    - name: Generate an intermediate CA CSR
      sflab.homelab.vault_pki_generate_intermediate_csr:
        url: https://vault:8201
        auth_method: userpass
        username: '{{ user }}'
        password: '{{ passwd }}'
        engine_mount_point: pki
        common_name: Intermediate CA



Return Values
-------------
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>csr</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>success</td>
                <td>
                            <div>The certificate signing request (CSR) generated by the module.</div>
                    <br/>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>key_id</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>success</td>
                <td>
                            <div>The identifier of the private key used to generate the certificate signing request (CSR).</div>
                    <br/>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Sebastian Freund (@sflab)

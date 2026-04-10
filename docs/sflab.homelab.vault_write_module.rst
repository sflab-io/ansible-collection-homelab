.. _sflab.homelab.vault_write_module:


*************************
sflab.homelab.vault_write
*************************

**Execute a write operation in HashiCorp Vault**


Version added: 0.1.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- `Writes <https://hvac.readthedocs.io/en/stable/usage/index.html#writing-data>`_ data to a specified path in HashiCorp Vault.
- This module provides a generic interface for executing Vault write operations.
- The module is not idempotent and will always report changed=true when executed.



Requirements
------------
The below requirements are needed on the host that executes this module.

- ``hvac`` (`Python library <https://hvac.readthedocs.io/en/stable/overview.html>`_)


Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="1">
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
                <td colspan="1">
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
                <td colspan="1">
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
                <td colspan="1">
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
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>data</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The data to write to the specified path.</div>
                        <div>Key-value pairs are passed through to the Vault write operation without validation.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
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
                <td colspan="1">
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
                <td colspan="1">
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
                <td colspan="1">
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
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>path</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The Vault path to write data to.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
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
                <td colspan="1">
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
                <td colspan="1">
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
                <td colspan="1">
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
                <td colspan="1">
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
                <td colspan="1">
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
                <td colspan="1">
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
                <td colspan="1">
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
                <td colspan="1">
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
                <td colspan="1">
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
                <td colspan="1">
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
                <td colspan="1">
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
                <td colspan="1">
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
                    <b>response</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>changed
not check_mode</td>
                <td>
                            <div>The response from the Vault write operation.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;request_id&#x27;: &#x27;abc123-def456-ghi789&#x27;, &#x27;lease_id&#x27;: &#x27;&#x27;, &#x27;renewable&#x27;: False, &#x27;lease_duration&#x27;: 0, &#x27;data&#x27;: {}, &#x27;wrap_info&#x27;: None, &#x27;warnings&#x27;: None, &#x27;auth&#x27;: None}</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Sebastian Freund (@sflab)

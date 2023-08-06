[![pipeline status](https://gitdev.digdeo.fr/digdeo-projets-floss1/digdeo-syspass-client/badges/master/pipeline.svg)](https://gitdev.digdeo.fr/digdeo-projets-floss1/digdeo-syspass-client/-/commits/master) [![coverage report](https://gitdev.digdeo.fr/digdeo-projets-floss1/digdeo-syspass-client/badges/master/coverage.svg)](https://gitdev.digdeo.fr/digdeo-projets-floss1/digdeo-syspass-client/-/commits/master)

# digdeo-syspass-client

Python API Client for SysPass server (https://www.syspass.org/en)

### Implemented API
Both 100% Cover and 100% UnitTested
* 3.0: https://syspass-doc.readthedocs.io/en/3.0/
* 3.1: https://syspass-doc.readthedocs.io/en/3.1/

### Cool but what i need to use it ?
The API Client require settings like the server and token ;)
It have many ways to inject that setting, via config file and/or by ENV vars.

### Permanent configuration::

That is suppose to be the default setting , where a file ``config.yml`` is store in user space. 

That standard is describe on FreeDedktop web site. https://specifications.freedesktop.org/basedir-spec/basedir-spec-0.6.html

Then by follow recommendation and standard we use ``$HOME/.config/digdeo-syspass-client/`` as default directory for search ``config.yml`` file.

You can change the ``$XDG_CONFIG_HOME/digdeo-syspass-client/config.yml`` search by set a ENV var **syspass_config_dir** then 
``$HOME/.config/digdeo-syspass-client/config.yml`` will become ``$syspass_config_dir/config.yml``

For more information's  take a look on FreeDesktop XDG recommendation.

### Config file

You can use any type of key here, in our usage that is a Read Only key.

```
syspassclient:
  api_url: 'https://you.server.exemple.com/api.php'
  api_version: '3.1'
  authToken: '######################################################'
  tokenPass: '######################################################'
  verify_ssl: True
  debug: False
  debug_level: 0
  verbose: False
  verbose_level: 0
```

### Variables

* **syspass_config_dir**
* **syspass_auth_token**
* **syspass_token_pass**
* **syspass_verify_ssl**
* **syspass_api_url**
* **syspass_api_version**
* **syspass_debug**
* **syspass_debug_LEVEL**
* **syspass_verbose**
* **syspass_verbose_level**
        
#### syspass_config_dir
Shortcut the ``$HOME/.config/digdeo-syspass-client`` default path by the value of the variable

#### syspass_auth_token
Shortcut the ``authToken`` set inside the ``config.yml``

#### syspass_verify_ssl
If it variable is set then, SSL certificates will be verify.

Note that is Python **Requests** module it deal with SSL certificate , if you take a look of it module documentation, you'll be inform about how deal with self signed certificates.
In summary, Requests module  use **REQUESTS_CA_BUNDLE** env variable, for get the SSL Bundle certificate file path of you system.

Example:
```shell script
export REQUESTS_CA_BUNDLE="/etc/ssl/certs/ca-certificates.crt"
```

The ``ca-certificates.crt`` file is generate by system package call ``ca-certificates`` and must be re-generate each time you add a new self-signed certificate.

Exemple:
```shell script
sudo cp my.cert /usr/local/share/ca-certificates/
sudo update-ca-certificates
```

For many programming language, self signed certificates addition, require to inform the system about that new self-signed certificates existence.

The SSL Bundle Certificates , is common thing for SSL and is not impose by Python it self. If you want more information's, back to you system documentation for know more about SSL bundle cert .

#### syspass_token_pass
Shortcut the ``tokenPass`` set inside the ``config.yml``

#### syspass_api_url
Shortcut the ``api_url`` set inside the ``config.yml``

#### syspass_api_version
Shortcut the ``api_version`` set inside the ``config.yml``

#### syspass_debug
Shortcut the ``debug`` set inside the ``config.yml``

#### syspass_debug_LEVEL
Shortcut the ``debug_level`` set inside the ``config.yml``

#### syspass_verbose
Shortcut the ``verbose`` set inside the ``config.yaml``

#### syspass_verbose_level
Shortcut the ``verbose_level`` set inside the ``config.yml``

### Tips

* If you would like to change token on fly, you'll have to play with **$syspass_config_dir** and a subdirectory structure.
* Syspassclient can start without config.yml file and is suppose to use Variables , that permit to make tests inside a CI.
---
DigDeo FLOSS Team - 2020
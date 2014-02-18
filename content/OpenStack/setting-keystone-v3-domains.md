Title: Setting Keystone v3 domains
Date: 2014-01-18
Tags: OpenStack, Keystone

The [Openstack Identity v3 API][1], provided by Keystone, offers
features that were lacking in the previous version. Among these
features, it introduces the concept of domains, allowing isolation of
projects and users. For instance, an administrator allowed to create
projects and users in a given domain, may not have any right in
another one. While these features look very exciting, some
configuration needs to be done to have a working identity v3 service
with domains properly set.

[Keystone API protection][2] section of the developer's doc provides
hints about how to set-up a multi-domain installation. Starting from
there, I describe the full steps to have a multi-domain setup running,
by using `curl` to send http requests and `jq` to parse the json
answers.


Setting an admin domain and a cloud admin
-----------------------------------------

First, we have to start on a fresh non multi-domain installation with
the [default policy file][3].

* With the `admin` user we can create the `admin_domain`.

        ::::bash
        ADMIN_TOKEN=$(\
        curl http://localhost:5000/v3/auth/tokens \
            -s \
            -i \
            -H "Content-Type: application/json" \
            -d '
        {
            "auth": {
                "identity": {
                    "methods": [
                        "password"
                    ],
                    "password": {
                        "user": {
                            "domain": {
                                "name": "Default"
                            },
                            "name": "admin",
                            "password": "password"
                        }
                    }
                },
                "scope": {
                    "project": {
                        "domain": {
                            "name": "Default"
                        },
                        "name": "admin"
                    }
                }
            }
        }' | grep ^X-Subject-Token: | awk '{print $2}' )

        ID_ADMIN_DOMAIN=$(\
        curl http://localhost:5000/v3/domains \
            -s \
            -H "X-Auth-Token: $ADMIN_TOKEN" \
            -H "Content-Type: application/json" \
            -d '
        {
            "domain": {
            "enabled": true,
            "name": "admin_domain"
            }
        }' | jq .domain.id | tr -d '"' )

        echo "ID of domain cloud: $ID_ADMIN_DOMAIN"

* Then we can create our `cloud_admin` user, within the `admin_domain`
  domain.

        ::::bash
        ID_CLOUD_ADMIN=$(\
        curl http://localhost:5000/v3/users \
            -s \
            -H "X-Auth-Token: $ADMIN_TOKEN" \
            -H "Content-Type: application/json" \
            -d "
        {
            \"user\": {
                \"description\": \"Cloud administrator\",
                \"domain_id\": \"$ID_ADMIN_DOMAIN\",
                \"enabled\": true,
                \"name\": \"cloud_admin\",
                \"password\": \"password\"
            }
        }" | jq .user.id | tr -d '"' )

        echo "ID of user cloud_admin: $ID_CLOUD_ADMIN"

* And we grant to our user `cloud_admin` the `admin` role on domain
  `admin_domain`.

        ::::bash
        ADMIN_ROLE_ID=$(\
        curl http://localhost:5000/v3/roles?name=admin \
            -s \
            -H "X-Auth-Token: $ADMIN_TOKEN" \
        | jq .roles[0].id | tr -d '"' )

        curl -X PUT http://localhost:5000/v3/domains/${ID_ADMIN_DOMAIN}/users/${ID_CLOUD_ADMIN}/roles/${ADMIN_ROLE_ID} \
            -s \
            -i \
            -H "X-Auth-Token: $ADMIN_TOKEN" \
            -H "Content-Type: application/json"

        curl http://localhost:5000/v3/domains/${ID_ADMIN_DOMAIN}/users/${ID_CLOUD_ADMIN}/roles\
            -s \
            -H "X-Auth-Token: $ADMIN_TOKEN" | jq .roles

* Once the `admin_domain` has been created with its `cloud_admin`
  user, we can enforce a domain based policy. In order to do that, we
  have to copy the [policy.v3cloudsample.json][4] file over our former
  `/etc/keystone/policy.json`, while replacing the string
  `admin_domain_id` by the ID of the `admin_domain` we just
  created. Locate the `policy.v3cloudsample.json` file into the `etc`
  directory of Keystone's source.

        ::::bash
        sed s/admin_domain_id/${ID_ADMIN_DOMAIN}/ \
            < policy.v3cloudsample.json \
            > /etc/keystone/policy.json

Warning, current version (commit
19620076f587f925c5d2fa59780c1a80dde15db2) of policy.v3cloudsample.json
doesn't allow `cloud_admin` to manage users in other domains than its
own (see [bug 1267187][5]). Until the patch is merged, I suggest using
this [policy.c3cloudsample.json under review][6].


Creating domains and admins
---------------------------

From now on, the `admin` user can only manage projects and users in
the `Default` domain. To create other domains we will have to
authenticate with the `cloud_admin` user created above.

* Getting a token scoped on the `admin_domain`, for user `cloud_admin`.

        ::::bash
        CLOUD_ADMIN_TOKEN=$(\
        curl http://localhost:5000/v3/auth/tokens \
            -s \
            -i \
            -H "Content-Type: application/json" \
            -d '
        {
            "auth": {
                "identity": {
                    "methods": [
                        "password"
                    ],
                    "password": {
                        "user": {
                            "domain": {
                                "name": "admin_domain"
                            },
                            "name": "cloud_admin",
                            "password": "password"
                        }
                    }
                },
                "scope": {
                    "domain": {
                        "name": "admin_domain"
                    }
                }
            }
        }' | grep ^X-Subject-Token: | awk '{print $2}' )

* Creating domains `dom1` and `dom2`.

        ::::bash
        ID_DOM1=$(\
        curl http://localhost:5000/v3/domains \
            -s \
            -H "X-Auth-Token: $CLOUD_ADMIN_TOKEN" \
            -H "Content-Type: application/json" \
            -d '
        {
            "domain": {
                "enabled": true,
                "name": "dom1"
            }
        }' | jq .domain.id | tr -d '"')

        echo "ID of dom1: $ID_DOM1"

        ID_DOM2=$(\
        curl http://localhost:5000/v3/domains \
            -s \
            -H "X-Auth-Token: $CLOUD_ADMIN_TOKEN" \
            -H "Content-Type: application/json" \
            -d '
        {
            "domain": {
                "enabled": true,
                "name": "dom2"
            }
        }' | jq .domain.id | tr -d '"')

        echo "ID of dom2: $ID_DOM2"

* Now we will create a user `adm1` in domain `dom1`.

        ::::bash
        ID_ADM1=$(\
        curl http://localhost:5000/v3/users \
            -s \
            -H "X-Auth-Token: $CLOUD_ADMIN_TOKEN" \
            -H "Content-Type: application/json" \
            -d "
        {
            \"user\": {
                \"description\": \"Administrator of domain dom1\",
                \"domain_id\": \"$ID_DOM1\",
                \"enabled\": true,
                \"name\": \"adm1\",
                \"password\": \"password\"
            }
        }" | jq .user.id | tr -d '"')

        echo "ID of user adm1: $ID_ADM1"

* We will also grant the `admin` role on domain `dom1` to this `adm1`
  user.

        ::::bash
        curl -X PUT http://localhost:5000/v3/domains/${ID_DOM1}/users/${ID_ADM1}/roles/${ADMIN_ROLE_ID} \
            -s \
            -i \
            -H "X-Auth-Token: $CLOUD_ADMIN_TOKEN" \
            -H "Content-Type: application/json"

        curl http://localhost:5000/v3/domains/${ID_DOM1}/users/${ID_ADM1}/roles \
            -s \
            -H "X-Auth-Token: $CLOUD_ADMIN_TOKEN" | jq .roles


Creating projects and users
---------------------------

The `adm1` user can now fully manage domain `dom1`. He is allowed to
manage as many projects and users as he wishes within `dom1`, while
not being able to access resources of domain `dom2`.

* Now we authenticate as user `adm1` with a scope on `dom1`.

        ::::bash
        ADM1_TOKEN=$(\
        curl http://localhost:5000/v3/auth/tokens \
            -s \
            -i \
            -H "Content-Type: application/json" \
            -d '
        {
            "auth": {
                "identity": {
                    "methods": [
                        "password"
                    ],
                    "password": {
                        "user": {
                            "domain": {
                                "name": "dom1"
                            },
                            "name": "adm1",
                            "password": "password"
                        }
                    }
                },
                "scope": {
                    "domain": {
                        "name": "dom1"
                    }
                }
            }
        }' | grep ^X-Subject-Token: | awk '{print $2}' )

* We create a project `prj1` in domain `dom1`.

        ::::bash
        ID_PRJ1=$(\
        curl http://localhost:5000/v3/projects \
            -s \
            -H "X-Auth-Token: $ADM1_TOKEN" \
            -H "Content-Type: application/json" \
            -d "
        {
            \"project\": {
                \"enabled\": true,
                \"domain_id\": \"$ID_DOM1\",
                \"name\": \"prj1\"
            }\
        }" | jq .project.id | tr -d '"' )

        echo "ID of prj1: $ID_PRJ1"

* When trying and creating a project in domain `dom2`, it fails.

        ::::bash
        curl http://localhost:5000/v3/projects \
            -s \
            -H "X-Auth-Token: $ADM1_TOKEN" \
            -H "Content-Type: application/json" \
            -d "
        {
            \"project\": {
                \"enabled\": true,
                \"domain_id\": \"$ID_DOM2\",
                \"name\": \"prj2\"
            }\
        }" | jq .

* Creating a standard user `usr1` in domain `dom1`, with default project `prj1`.

        ::::bash
        ID_USR1=$(\
        curl http://localhost:5000/v3/users \
            -s \
            -H "X-Auth-Token: $ADM1_TOKEN" \
            -H "Content-Type: application/json" \
            -d "
        {
            \"user\": {
                \"default_project_id\": \"$ID_PRJ1\",
                \"description\": \"Just a user of dom1\",
                \"domain_id\": \"$ID_DOM1\",
                \"enabled\": true,
                \"name\": \"usr1\",
                \"password\": \"password\"
            }
        }" | jq .user.id | tr -d '"' )

        echo "ID of user usr1: $ID_USR1"

* Granting `Member` role to user `usr1` on project `prj1`.

        ::::bash
        MEMBER_ROLE_ID=$(\
        curl http://localhost:5000/v3/roles?name=Member \
            -s \
            -H "X-Auth-Token: $ADM1_TOKEN" \
        | jq .roles[0].id | tr -d '"' )

        curl -X PUT http://localhost:5000/v3/projects/${ID_PRJ1}/users/${ID_USR1}/roles/${MEMBER_ROLE_ID} \
            -s \
            -i \
            -H "X-Auth-Token: $ADM1_TOKEN" \
            -H "Content-Type: application/json"

        curl http://localhost:5000/v3/projects/${ID_PRJ1}/users/${ID_USR1}/roles \
            -s \
            -H "X-Auth-Token: $ADM1_TOKEN" | jq .roles


The domain administrator `adm1` ended up creating a project `prj1` and
a user `usr1` member of the project. `usr1` can now get a token scoped
on `prj1` and manage resources into this project.


[1]: http://api.openstack.org/api-ref-identity.html#identity-v3
[2]: http://docs.openstack.org/developer/keystone/configuration.html#keystone-api-protection-with-role-based-access-control-rbac
[3]: https://github.com/openstack/keystone/blob/master/etc/policy.json
[4]: https://github.com/openstack/keystone/blob/master/etc/policy.v3cloudsample.json
[5]: https://bugs.launchpad.net/keystone/+bug/1267187
[6]: https://review.openstack.org/#/c/65510/
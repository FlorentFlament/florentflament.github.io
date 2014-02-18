Title: Customizing OpenStack RBAC policies
Date: 2014-02-09
Tags: OpenStack, Keystone, Policies

OpenStack uses a [role based access control][2] (RBAC) mechanism to
manage accesses to its resources. With the current architecture,
users' roles granted on each project and domain are stored into
Keystone, and can be updated through [Keystone's API][1]. However,
policy enforcement (actually allowing or not the access to resources
according to a user's roles) is performed independently in each
service, based on the rules defined in each `policy.json` file.

In a default OpenStack setup (like Devstack), two roles are created:

* The `Member` role, which when granted to a user on a project, allows
  him to manage resources (instances, volumes, ...) in this project.

* The `admin` role, which when granted to a user on any project,
  offers to this user a total control over the whole OpenStack
  platform. Although this is the current behavior, it has been [marked
  as a bug][3].

However, the OpenStack policy engine allows operators to specify fine
grained set of rules to control access to resources of each OpenStack
service (Keystone, Nova, Cinder, ...).


Attributes available to build custom policies
---------------------------------------------

Four types of attributes can be used to set policy rules:

* User roles, which can be checked by using the following syntax:

        ::::text
        role:<requires_role>

* Other user related attributes (stored into or obtained through the
  token). The following attributes are available: user_id, domain_id
  or project_id (depending on the scope), and can be checked against
  constants or other attributes:

        ::::text
        project_id:<some_attribute>

* API call attributes are any data sent along with the API call. They
  can be checked against constants or user attributes. For instance,
  the following statement checks that a user being created is in the
  same domain as his creator (note that API call attributes have to be
  on the right side of the expression, while user attributes are on
  the left side):
  
        ::::text
        domain_id:user.domain_id

* The fourth category of attributes are what I'd call contextual
  attributes. These are the attributes of objects referenced (or
  targeted) by an API call; i.e. any object whose id appear somewhere
  in the API call. For instance, when granting a new role on a project
  to a user, all attributes related to the role, the project and the
  user are available to the policy engine, through the `target`
  keyword. The following syntax checks that the role of the context is
  the `Member` role:

        ::::text
        'Member':target.role.name


Depending on the type of API calls, some of the following attributes
will be available, according to the objects impacted by the action:

* domain:
    * target.domain.enabled
    * target.domain.id
    * target.domain.name

* group:
    * target.group.description
    * target.group.domain_id
    * target.group.id
    * target.group.name

* project:
    * target.project.description
    * target.project.domain_id
    * target.project.enabled
    * target.project.id
    * target.project.name

* role:
    * target.role.id
    * target.role.name

* user:
    * target.user.default_project_id
    * target.user.description
    * target.user.domain_id
    * target.user.enabled
    * target.user.id
    * target.user.name


Example: admin and super_admin
------------------------------

The following example is taken from a User Story that we were
considering at [CloudWatt][4]. As a cloud service provider, we wanted
to be able to have 2 different levels of administrator roles:

* An `admin` role, which allows its users to grant the `Member` role
  to any other user.
* While the `super_admin` role allows granting any role.

When added to Keystone's ̀`policy.json` file, the following rules
implements the two roles described previously:

    ::::text
    "admin_grant_member": "role:admin and 'Member':%(target.role.name)s",
    "identity:create_grant": "role:super_admin or rule:admin_grant_member",

The first rule describes a new rule called `admin_grant_member`, which
checks that the user authenticated by the token has the `admin` role
(on its scope), and that the role in the context (the role the admin
is trying to grant) is the `Member` role (we used the `name`
attribute, but could use the role's id instead).

The second rule is checked whenever an API call is made to grant a
role to a user (action `identity:create_grant`). This rule tells the
policy engine that in order for a user to be allowed to grant a role
to another user, the user authenticated by the token must either have
the `super_admin` role, or satisfy the `admin_grant_member` rule.

Put together these two rules actually meet the use case. Any user with
the `admin` role will only be able to grant the `Member` role to other
users, while users with the `super_admin` role will be able to grant
any role.


Notes
-----

One of the most powerful rules that the OpenStack policy engine
allows, are those limiting a user's actions to his own domain or
project. These kind of rules are widely used in [Keystone's
policy.v3cloudsample.json][5].

Also note, that a recent patch merged into oslo-incubator implements
the blueprint allowing the policy engine to [check contextual
attributes against constant values][6]. This patch will have to be
synchronized into the OpenStack projects for them to benefit from this
feature.


[1]: http://api.openstack.org/api-ref-identity.html#identity-v3
[2]: http://docs.openstack.org/developer/keystone/configuration.html#keystone-api-protection-with-role-based-access-control-rbac
[3]: https://bugs.launchpad.net/keystone/+bug/968696
[4]: http://www.cloudwatt.com
[5]: https://github.com/openstack/keystone/blob/master/etc/policy.v3cloudsample.json
[6]: https://blueprints.launchpad.net/oslo/+spec/policy-constant-check

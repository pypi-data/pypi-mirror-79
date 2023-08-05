# Python IAM - Identity Consumer

The `iam.ext.idc` provides a framework to consume identities from an
Identity Provider (IDP) i.e. to act as Service Provider (SP) when using
Security Assertion Markup Language (SAML) or as a Relying Party (RP) when
using OAuth2.

## Preconditions, constraints and assumptions

The following constrains and assumptions apply:

- The deployement consumes identities from a single Identity Provider (IdP) or
  Asserting Party (AP).
- The IdP/AP is fully trusted in the claims that they make regarding the
  Subject i.e. don't use this framework in combination with, for example,
  OAuth2 providers that allow users to specifcy any email address.

## Installation

Install with `pip`:

```
pip install iam.ext.idc
```

## Resources

- [OpenID Connect](https://connect2id.com/learn/openid-connect)

# Loducode utils

Basic components for the development of loducode s.a.s.

### install

`pip install loducode_utils==0.0.7`

## functionalities

- **Admin**
    - ReadOnlyAdmin
    - ReadOnlyStackedInline
    - ReadOnlyTabularInline
- **Models**
    - Audit
    - City  
- **Tasks**
    - send_mail_task(email, subject, message)
- **Urls Api**
    - /api/token/
    - /api/logout/
    - /api/forget/
- **Utils**
    - PaginatedListView
- **Views api**
    - ObtainCustomAuthToken
    - LogoutView
    - ForgetPasswordView

## Commands

- python setup.py sdist bdist_wheel
- twine upload --repository pypi dist/loducode_utils-0.0.7*

####Version 0.0.8
- change translation model payment record
- new view data epayco

####Version 0.0.7
new model payment record

####Version 0.0.6
model city in admin fixxed register

####Version 0.0.5

- model city in admin
- migrations initials city

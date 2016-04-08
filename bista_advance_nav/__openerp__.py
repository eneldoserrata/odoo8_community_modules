{
    'name': 'Advance multi-level navigation',
    'version': '1.1',
    'description': """
        1. Default vertical navigation bar is hidden on installation of module
         and this can be accessed using the left nav menu.
        2. Ease of access to all the Odoo functionality through the
         horizontal navigation bar.
            1. Each menus of the horizontal bar consist
            of sub menus of the particular module.
    """,
    'author': 'Bista Solutions Pvt. Ltd',
    'website': 'http://www.bistasolutions.com',
    'depends': ['web'],
    'category': 'web',
    'data': ['views/webclient_templates.xml'],
    'installable': True,
    'auto_install': False,
    'application': True,
}

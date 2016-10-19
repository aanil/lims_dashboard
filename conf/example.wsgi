import site
site.addsitedir(<site_packages of the python you want to use>)
from lims_dashboard.server import create_app

root_path=<application root path>
application=create_app(root_path, python=<path to the python you want to use>)

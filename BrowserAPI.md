# Browser methods/API

To get full details on the methods below you can use the `xpathshell` command. 

* Once in the shell you can execute `b.<method>?` eg: `b.wait_condition?` (note the `?` question mark).
* IPython will print the corresponding method documentation.

Main methods:

* `set_base_url`
* `get_driver`
* `current_path`
* `current_url`
* `get`
* `get_url`
* `get_page`
* `get_page_once`
* `wait_condition`
* `xpath`
* `select_xpath`
* `select_xsingle`
* `css`
* `select_css`
* `select_css_single`
* `fill`
* `fill_form`
* `fill_form_attr`
* `fill_form_xpath`
* `fill_form_ordered`
* `click`
* `sleep`
* `wipe_alerts`
* `quick_screenshot`
* `save_screenshot`
* `execute_script`

Main attributes:

* `driver`: direct access to the underlying webdriver object.
* `base_url`: current `base_url`
* `current_path`: current path from the driver
* `current_url`: current url from the driver

Other less important methods:

* `build_url`
* `clean_url`
* `get_remote_credentials`


For more details you can open the `xpathwebdriver/xpath_browser.py` code

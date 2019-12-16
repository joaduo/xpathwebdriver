
# Webdriver browser life level constants

# Browser survives across processes
SURVIVE_PROCESS = -5
# Browser is alive as long as the python process is running
PROCESS_LIFE = -4
# Browser is alive as long as the WebdriverManager is not deleted
MANAGER_LIFE = -3
# Browser is alive for a single test round (eg: a unit test class)
TEST_ROUND_LIFE = -2
# Start 1 new browser per test ran
SINGLE_TEST_LIFE = -1

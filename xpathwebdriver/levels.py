
# Webdriver browser life level constants

# Browser survives across processes (INMORTAL_LIFE is deprecated name)
SURVIVE_PROCESS = INMORTAL_LIFE = 5
# Browser is alive as long as the smoothtest process is running
PROCESS_LIFE = 4
# Browser is alive as long as the WebdriverManager is not deleted (TEST_RUNNER_LIFE is deprecated name)
MANAGER_LIFE = TEST_RUNNER_LIFE = 3
# Browser is alive for a single test round (eg: a unit test class)
TEST_ROUND_LIFE = 2
# Start 1 new browser per test ran
SINGLE_TEST_LIFE = 1

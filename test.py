import logging

# from core import DevTrace
#
# dt = DevTrace()
logger = logging.getLogger("inspect_tests")

class Test:

    def __init__(self, fn, ln):
        self.fn = fn
        self.ln = ln

    def deep_call_level_1(self, l_v3):
        logger.error("Test: First Name: {} and Last Name: {}, l_v3: {}".format(self.fn, self.ln, l_v3))

    def hello_world(self):
        l_v1 = "l_v1"
        l_v2 = 1.23
        self.deep_call_level_1("l_v3_1")

num_iterations = 100000
# num_iterations = 10
t = Test('L', 'G')
for i in range(num_iterations):
    t.hello_world()

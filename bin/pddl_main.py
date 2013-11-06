import sys
import pyreform.pddl_merge as main
import config

result = main.run(sys.argv[1], sys.argv[2], local_config=config)


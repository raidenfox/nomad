import sys
sys.path.append("modules")
sys.path.append("modules/core")
sys.path.append("modules/db")
import nomad

nomad.start_nomad("torque02.scope.unina.it",30,"R")
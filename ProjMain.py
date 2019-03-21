import math
import random
from dataclasses import dataclass


# Project 1
# In this project, we are going to build a discrete-time event
# simulator for a number of CPU schedulers on a single CPU system.
# The goal of this project is to compare and assess the impact of
# different schedulers on different performance metrics, and across multiple workloads.
# @authors: John Daloni, Jamal Rasool, Kristof York, Fernando Valdez, Elliot Esponda
# @date: March 21st, 2019


@dataclass  # Struct Creation
class Process:
	service_time: float
	arrival_time: float
	remaining_time: float
	completion_time: float
	id: int


class Event(object):
	pass


class Event:
	time: float
	type: type
	kind: type
	next_event: Event


print("Python 3")
print("Did I do it correctly Jamal?")
print("Yes you did")

class queue_stat:
	
	def statque(ID):
		queues = pbs.pbs_statque(ID, "" , "NULL", "NULL")
		for queue in queues:
			print queue.name,"\n---------------------\n"
			for attrib in queue.attribs:
				print attrib.name," ",attrib.value
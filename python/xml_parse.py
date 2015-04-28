# when level = "IGNORE", we will ignore it, it more than one place set the level
# the priority of level is class > package > layer > log4j
# if all of layer_level, package_level and class_level are "IGNORE",
# it will throw an exception
class myfile:
	def __init__(self):
		self.class_simple = "" # name of the class
		self.package = "" # package of the class
		self.layer = "" # layer of the class
		self.class_level="" # level set by class
		self.package_level="" # level set by package
		self.layer_level="" # level set by layer
		self.level="" # the final level
	def print_it(self):
		print("class_simple:"+self.class_simple)
		print("class_level:"+self.class_level)
		print("package:"+self.package)
		print("package_level:"+self.package_level)
		print("layer:"+self.layer)
		print("layer_level:"+self.layer_level)
		print("level:"+self.level)

# global parameters
log4j_default_level = ""

# parse the myfile according to the log4j.xml
def parse(set_allfile):
	from xml.dom import minidom
	doc = minidom.parse("log4j.xml")

	node_log4j = doc.documentElement
	global log4j_default_level
	log4j_default_level = node_log4j.getAttribute("level")
	print("log4j_default_level:" + str(log4j_default_level))
	list_node_layer = node_log4j.getElementsByTagName("layer")
	# layer
	for node_layer in list_node_layer:
		#print(node_layer.getAttribute('content'))
		#print(node_layer.getAttribute('level'))
		list_node_package = node_layer.getElementsByTagName("package")
		# package
		for node_package in list_node_package:
			list_node_class = node_package.getElementsByTagName("class")
			# class
			for node_class in list_node_class:
				# get node of its package and layer
				cur = myfile()
				node_package_ = node_package
				node_layer_ = node_layer
				# set attributes by nodes
				cur.class_simple = node_class.getAttribute("content")
				cur.class_level = node_class.getAttribute("level")
				cur.package = node_package_.getAttribute("content")
				cur.package_level = node_package_.getAttribute("level")
				cur.layer = node_layer_.getAttribute("content")
				cur.layer_level = node_layer_.getAttribute("level")
				# add cur into set_allfile
				set_allfile.add(cur)
	
	return set_allfile	

# choose the level of the highest priority
def choose_level(set_allfile):
	global log4j_default_level
	#print("choose_level log4j_default_level:" + log4j_default_level)
	for cur in set_allfile:
		# log4j level
		#print("log4j_default_level:" + log4j_default_level)
		if log4j_default_level != "IGNORE":
			#print("###")
			cur.level = log4j_default_level
		# layer level
		#print("cur.layer_level:" + cur.layer_level)
		if cur.layer_level != "IGNORE":
			#print("$$$")
			cur.level = cur.layer_level
		# package level
		if cur.package_level != "IGNORE":
			cur.level = cur.package_level
		# class level
		if cur.class_level != "IGNORE":
			cur.level = cur.class_level
		#print ("cur.class_simple:"+cur.class_simple+",cur.level:"+cur.level)
	return set_allfile

def check_level(set_allfile):
	print("check_level")
	support_level_set = set(['OFF','FATAL','ERROR','WARN','INFO','DEBUG','TRACE','ALL'])
	for cur in set_allfile:
		cur_level_set = set()
		cur_level_set.add(cur.level)
		if not cur_level_set.issubset(support_level_set):
			print ("only OFF,FATAL,ERROR,WARN,INFO,DEBUG,TRACE and ALL are supported")
			print ("level of the class is not support, the details info is as follows:")
			cur.print_it()
			raise

# write the java src in layer(LOG),package(com.espressif.iot.log),class(InitLogger.java)
def write_java_src(set_allfile):
	print("write_java_src")
	file_name = "../java/LOG/com/espressif/iot/log/InitLogger.java"
	file_f = open(file_name,"w")
	file_f.write("package com.espressif.iot.log;\n\n")
	file_f.write("import org.apache.log4j.Level;\n")
	file_f.write("import org.apache.log4j.Logger;\n\n\n")
	file_f.write("// it is generated by python\n")
	file_f.write("public class InitLogger {\n")
	file_f.write("    public static void init(){\n")
	file_f.write("        //######content######\n")
	file_f.write("        ConfigureLog4J.configure();\n")
	for myfile in set_allfile:
			# indent
			file_f.write("        ")
			# Logger.getLogger(
			file_f.write("Logger.getLogger(")
			# com.espressif.iot.oapi.OApiIntermediator.class).setLevel(
			file_f.write(myfile.package + "." + myfile.class_simple + ".class).setLevel(")
			# Level.DEBUG);
			file_f.write("Level." + myfile.level + ");\n")	

	file_f.write("    }\n")
	file_f.write("}")

	file_f.close()


set_allfile = set()
parse(set_allfile)
choose_level(set_allfile)
#for cur in set_allfile:
#	cur.print_it()
check_level(set_allfile)
write_java_src(set_allfile)

# Comment this line to run with default java
# otherwise, set the JAVA_PATH variable to the path of your java installation
#JAVA_PATH=/opt/homebrew/opt/openjdk@11/bin/

JAVAC=javac
JAVA=java
LIB_DIR=lib
OUT_DIR=out

#Modify user according to your username
USER=fran

#Indicate te correct version of the json library you want to use (add it in the lib folder)
JAR=json-20240303.jar

#Directory where spark is installed
SPARK_FOLDER=/home/${USER}/.applications_packages/Java/Spark/spark-3.5.1-bin-hadoop3

#Extra libraries to include, replace with your own .jars
CLASSPATH=$(OUT_DIR):$(LIB_DIR)/$(JAR):$(shell find $(SPARK_FOLDER)/jars -name '*.jar' | tr '\n' ':')
SOURCES=$(shell find src -name "*.java")

#Create a JAR with your application
APP_JAR=feed-reader.jar

all: build run

build:
	$(JAVA_PATH)$(JAVAC) --release 11 -cp $(CLASSPATH) -d out $(SOURCES)
	cd $(OUT_DIR) && jar cvf ../$(APP_JAR) .

run:
	$(JAVA_PATH)$(JAVA) -cp $(CLASSPATH) FeedReaderMain

#New rule to run with spark-submit
spark: build
	$(SPARK_FOLDER)/bin/spark-submit \
		--class FeedReaderMain \
		--master spark://fran-MAX-G0101:7077 \
		--driver-memory 1g \
		--executor-memory 1g \
		--executor-cores 1 \
		--jars $(LIB_DIR)/$(JAR) \
		$(APP_JAR)

#New rule to run with spark-submit and named entities
spark-ne: build
	$(SPARK_FOLDER)/bin/spark-submit \
		--class FeedReaderMain \
		--master spark://fran-MAX-G0101:7077 \
		--driver-memory 1g \
		--executor-memory 1g \
		--executor-cores 1 \
		--jars $(LIB_DIR)/$(JAR) \
		$(APP_JAR) -ne

clean:
	rm -rf $(OUT_DIR)
	rm -f $(APP_JAR)

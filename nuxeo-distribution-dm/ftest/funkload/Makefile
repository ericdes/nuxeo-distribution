CREDCTL := fl-credential-ctl credential.conf
MONCTL := fl-monitor-ctl monitor.conf
LOG_HOME := ../../target/ftest/funkload/log

ifdef URL
	FLOPS = -u $(URL) $(EXT)
else
	FLOPS = $(EXT)
endif

ifdef REPORT_HOME
	REPORT = $(REPORT_HOME)
else
	REPORT = ../../target/ftest/funkload/report
endif


# all test except bench
all: start rest page test-nuxeo webengine stop

start:
	-mkdir -p $(REPORT) $(LOG_HOME)
	-$(MONCTL) restart
	$(CREDCTL) restart
	fl-run-test test_pages.py -v --simple-fetch -e testAvailable $(FLOPS)


stop:
	-$(MONCTL) stop
	-$(CREDCTL) stop

# test rest and pages libs
rest:
	fl-run-test -v --simple-fetch test_rest.py -e testWriter $(FLOPS)
	fl-run-test -v --simple-fetch test_rest.py -e testReader $(FLOPS)

page:
	fl-run-test -v --simple-fetch test_pages.py $(FLOPS)

webengine:
	fl-run-test -v --simple-fetch test_webengine.py $(FLOPS)


# test nuxeo ep
init:
	fl-run-test -v --simple-fetch test_nuxeo.py -e testInit $(FLOPS)

writer:
	fl-run-test -v --simple-fetch test_nuxeo.py -e testWriter $(FLOPS)

reader:
	fl-run-test -v --simple-fetch test_nuxeo.py -e testReader $(FLOPS)

test-nuxeo: init writer reader


# bench nuxeo ep
bench: start test-nuxeo bench-writer bench-reader stop

bench-writer:
	-fl-run-bench --simple-fetch -c 1:2:4:6 -D 60 -m 0.2 -M 1 -s 1 test_nuxeo.py Nuxeo.testWriter $(FLOPS)
	-fl-build-report $(LOG_HOME)/nuxeo-bench.xml --html -o $(REPORT)

warmup:
	fl-run-test -v -m 0 -M 0 test_nuxeo.py -e testReader $(FLOPS)
	-fl-run-bench -c 5 -D 1 -m 0 -M 0 -s 0 test_nuxeo.py Nuxeo.testReader $(FLOPS)

bench-reader: warmup
	-fl-run-bench --simple-fetch -c 1:5:10:15:20:25:30 -D 60 -m 0.1 -M 1 -s 1 test_nuxeo.py Nuxeo.testReader $(FLOPS)
	-fl-build-report $(LOG_HOME)/nuxeo-bench.xml --html -o $(REPORT)


clean:
	-find . "(" -name "*~" -or  -name ".#*" -or  -name "*.pyc" ")" -print0 | xargs -0 rm -f

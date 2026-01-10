# to produce less distraction
RUN_ARGS=--ui_event_filters=-info --noshow_progress --show_result=0 

lock:
	cd rules_dummy && bazelisk run //requirements

run_rules_dummy:
	cd rules_dummy && bazelisk run ${RUN_ARGS} @rules_dummy//tool

run:
	bazelisk run ${RUN_ARGS} @rules_dummy//tool
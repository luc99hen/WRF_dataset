FROM 1813927768/wrf_dataset_compile

WORKDIR /wrf

ADD . /wrf

ENTRYPOINT [ "/wrf/run_case.sh" ]
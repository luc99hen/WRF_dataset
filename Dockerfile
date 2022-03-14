FROM 1813927768/wrf_dataset_compile

WORKDIR /wrf

ADD . /wrf

CMD ["/wrf/run_case.sh"]
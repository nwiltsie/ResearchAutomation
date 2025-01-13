#!/usr/bin/env bash
set -eou pipefail

run_script_in_dir() {
    local dir=$1

    pushd "$dir" > /dev/null

    echo "Bootstrapping renv in $dir..."
    Rscript -e "renv::restore()"

    echo "Generating plot in $dir..."
    Rscript "../do_plot.R"

    popd > /dev/null
}

run_script_in_dir "v3.4"
run_script_in_dir "v3.5"

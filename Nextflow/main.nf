#!/usr/bin/env nextflow

nextflow.enable.dsl=2

// Define parameters
params.csv_file = "${projectDir}/../data/2021-02-18-data.csv"
params.outputDir = 'output'

// Extract racer names from the CSV
process extract_ids {
    input:
    path(csv_file)

    output:
    stdout

    script:
    """
    ${projectDir}/../scripts/print_racer_names.py ${csv_file}
    """
}


// Extract raw racer data
process extract_racer_data {
    input:
    tuple val(racer_name), path(csv_file)
    output:
    tuple val(racer_name), path("raw.json")

    script:
    """
    ${projectDir}/../scripts/extract_racer_data.py ${csv_file} --name ${racer_name} raw.json
    """
}

// Clean racer data
process clean_racer_data {
    input:
    tuple val(racer_name), path(raw_data)
    output:
    tuple val(racer_name), path("clean.json")

    script:
    """
    ${projectDir}/../scripts/clean_racer_data.py ${raw_data} clean.json
    """
}


// Generate lap plots
process plot_data {
    input:
    tuple val(racer_name), path(clean_data), val(plot_type)
    output:
    tuple val(racer_name), path("plot.png"), val(plot_type)

    publishDir path: "${params.outputDir}",
        pattern: "plot.png",
        mode: 'copy',
        saveAs: { "${plot_type}-${racer_name}.png" }

    script:
    """
    ${projectDir}/../scripts/plot_data.py ${clean_data} plot.png --type ${plot_type}
    """
}

/*

// Merge all cleaned racer data
process merge_data {
    input:
    file clean_files from clean_racer_data.collect()
    output:
    file "${params.temp_dir}/merged.json" into merged_data

    script:
    """
    ../scripts/merge_racer_data.py ${params.temp_dir}/merged.json ${clean_files.join(' ')}
    """
}

// Generate plots for merged data
process plot_merged_data {
    input:
    file merged_file from merged_data
    output:
    file "${params.output_dir}/merged-lines.png"
    file "${params.output_dir}/merged-split.png"

    script:
    """
    ../scripts/plot_data.py ${merged_file} ${params.output_dir}/merged-lines.png --type lap
    ../scripts/plot_data.py ${merged_file} ${params.output_dir}/merged-split.png --type split
    """
}
*/

workflow {
    extract_ids(params.csv_file)
        | splitText()
        | map(v -> v.strip())
        | combine(Channel.of(params.csv_file))
        | extract_racer_data
        | clean_racer_data
        | set {clean_data}

    clean_data
        | combine(Channel.of("lap", "split"))
        | plot_data

    // clean_data.view()

    // extract_racer_data(params.csv_file, racer_names)
    //     | clean_racer_data()

    /*
    // Racer-specific processes
    generate_lap_plots()
    generate_split_plots()

    // Merged data and plots
    merge_data()
    plot_merged_data()
    */
}

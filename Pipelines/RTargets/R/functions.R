parse_names <- function(csvfile) {
    parse_script <- "../scripts/print_racer_names.py"
    strsplit(
        system(paste(parse_script, csvfile), intern = TRUE),
        split = "\n"
    )
}

extract_data <- function(csvfile, racer_name, raw_dir) {
    extract_script <- "../scripts/extract_racer_data.py"
    outpath <- file.path(raw_dir, racer_name)

    system(paste(extract_script, csvfile, outpath, "--name", racer_name))
    return (outpath)
}

clean_data <- function(rawfile, clean_dir) {
    clean_script <- "../scripts/clean_racer_data.py"
    outpath <- file.path(clean_dir, basename(rawfile))

    system(paste(clean_script, rawfile, outpath))
    return (outpath)
}

merge_data <- function(datafiles, clean_dir) {
    merge_script <- "../scripts/merge_racer_data.py"
    outpath <- file.path(clean_dir, "merged")

    system(paste(
        merge_script,
        outpath,
        paste(datafiles, collapse = " ")
    ))
    return (outpath)
}

plot_data <- function(datafile, type, outdir) {
    plot_script <- "../scripts/plot_data.py"
    outpath <- file.path(outdir, paste0(basename(datafile), "-", type, ".png"))

    system(paste(
        plot_script,
        datafile,
        outpath,
        "--type",
        type
    ))
    return (outpath)
}


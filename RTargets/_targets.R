# _targets.R file
library(targets)

tar_source()

create_directory_targets <- function(target_name, path) {
    intermediate_name <- paste0(target_name, "_dir")

    list(
        # Target to create the directory and track it
        tar_target_raw(
            name = intermediate_name,
            command = substitute({
                if (!dir.exists(PATH)) dir.create(PATH, recursive = TRUE)
                tracking_file <- file.path(PATH, ".target-tracking")
                if (!file.exists(tracking_file)) file.create(tracking_file)
                tracking_file
            }, list(PATH = path)),  # Substitute the value of path
            format = "file"
        ),
        # Target to compute the directory name
        tar_target_raw(
            name = target_name,
            command = substitute(
                dirname(intermediate),
                list(intermediate = as.name(intermediate_name))
            )
        )
    )
}

list(
    tar_target(
        name = csvfile,
        command = "../data/2021-02-18-data.csv",
        format = "file"
    ),

    create_directory_targets("raw_dir", file.path(tar_path_store(), "user", "raw")),
    create_directory_targets("clean_dir", file.path(tar_path_store(), "user", "clean")),
    create_directory_targets("output_dir", "output"),

    # Extract the racer names
    tar_target(name = racer_names, command = parse_names(csvfile)),
    # Extract the raw racer data
    tar_target(
        name = raw_racer_data,
        command = extract_data(csvfile, racer_names, raw_dir),
        pattern = map(racer_names),
        format = "file"
    ),
    # Clean the racer data
    tar_target(
        name = clean_racer_data,
        command = clean_data(raw_racer_data, clean_dir),
        pattern = map(raw_racer_data),
        format = "file"
    ),

    tar_target(name = plot_types, command = c("lap", "split")),

    # Plot the individual racer data
    tar_target(
        name = racer_plots,
        command = plot_data(clean_racer_data, plot_types, output_dir),
        pattern = cross(clean_racer_data, plot_types),
        format = "file"
    ),

    # Merge the cleaned racer data
    tar_target(
        name = merged_data,
        command = merge_data(clean_racer_data, clean_dir),
        format = "file"
    ),

    tar_target(
        name = merged_plots,
        command = plot_data(merged_data, plot_types, output_dir),
        pattern = map(plot_types),
        format = "file"
    )
)

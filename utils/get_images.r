library(httr2)

file_name <- "adoption.zip"

request("https://www.kaggle.com/api/v1/") |>
    req_url_path_append("/competitions/data/download-all/") |>
    req_url_path_append("petfinder-adoption-prediction") |>
    req_auth_basic(Sys.getenv("KAGGLE_USERNAME"), Sys.getenv("KAGGLE_KEY")) |>
    req_perform(path = file_name)

dir_data <- "./data"
if (!dir.exists(dir_data)) {
  dir.create(dir_data)
}

unzip(file_name, exdir = dir_data)

library(data.table)

test <- fread(paste0(dir_data, "/test/test.csv"))
setnames(test, tolower)
multiple_ids <- test[quantity > 1]$petid

dir_origin <- paste0(dir_data, "/test_images")
dir_save <- Sys.getenv("DIR_SAVE", "./images")

if (!dir.exists(dir_save)) {
  dir.create(dir_save)
}

set.seed(42)
all_pictures <- list.files(dir_origin, pattern = "-1.jpg$", full.names = TRUE)
all_ids <- sub(".*/(.*?)-1.jpg", "\\1", all_pictures)
to_take <- which(!all_ids %in% multiple_ids)
sampled_pictures <- all_pictures[to_take]
sampled_ids <- all_ids[to_take]

for (file_path in sampled_pictures) {
  file_name <- basename(file_path)
  new_file_path <- file.path(dir_save, sub("-1.jpg", ".jpg", file_name))
  file.rename(from = file_path, to = new_file_path)
}

test <- test[petid %in% sampled_ids]

cols <- c("quantity", "state", "rescuerid", "videoamt", "photoamt",
          "breed2", "color2", "color3")
test[, (cols) := NULL]

breed <- fread(paste0(dir_data, "/breed_labels.csv"))
setnames(breed, tolower)

color <- fread(paste0(dir_data, "/color_labels.csv"))
setnames(color, tolower)

test[breed, on = .(breed1 = breedid), breed := i.breedname]
test[color, on = .(color1 = colorid), color := i.colorname]

cols <- c("breed1", "color1")
test[, (cols) := NULL]

test[, type := fifelse(type == 1, "Dog", "Cat")]

test[, gender := fcase(
  gender == 1, "Male",
  gender == 2, "Female",
  gender == 3, "Mixed"
)]

test[, maturitysize := fcase(
  maturitysize == 1, "Small",
  maturitysize == 2, "Medium",
  maturitysize == 3, "Large",
  maturitysize == 4, "Extra Large",
  maturitysize == 0, "Not Specified"
)]

test[, furlength := fcase(
  furlength == 1, "Short",
  furlength == 2, "Medium",
  furlength == 3, "Long",
  furlength == 0, "Not Specified"
)]

test[, vaccinated := fcase(
  vaccinated == 1, "Yes",
  vaccinated == 2, "No",
  vaccinated == 3, "Not Sure"
)]

test[, dewormed := fcase(
  dewormed == 1, "Yes",
  dewormed == 2, "No",
  dewormed == 3, "Not Sure"
)]

test[, sterilized := fcase(
  sterilized == 1, "Yes",
  sterilized == 2, "No",
  sterilized == 3, "Not Sure"
)]

test[, health := fcase(
  health == 1, "Healthy",
  health == 2, "Minor Injury",
  health == 3, "Serious Injury",
  health == 0, "Not Specified"
)]

file_info <- Sys.getenv("FILE_INFO", "/information.csv")
fwrite(test, paste0(dir_save, file_info))

# zip("images.zip", dir_save)

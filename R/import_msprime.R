
## Import simulated haplotypes from other software (i.e., msprime)

read_haplo <- function(haplo_file) {
  haplo <- readr::read_delim(haplo_file,
                             delim = " ",
                             col_names = FALSE)

  haplo
}


read_map <- function(map_file) {
  map <- readr::read_csv(map_file)
  colnames(map) <- c("marker", "bp", "M")
  # map$marker <- paste("site", map$marker, sep = "_")
  # map$chr <- 1
  #
  # map <- map[, c("marker", "chr", "M")]

  map$M

}



import_msprime <- function(founder_dir) {

  genome_table <- readr::read_tsv(paste(founder_dir, "/genome_table.txt", sep = ""))
  haplo_files <- paste(founder_dir, "/", genome_table$chr, ".txt", sep = "")
  map_files <- paste(founder_dir, "/", genome_table$chr, "_pos.txt", sep = "")

  haplo <- purrr::map(haplo_files, read_haplo)
  map <- purrr::map(map_files, read_map)

  ##colnames(haplo) <- map$marker

  AlphaSimR::newMapPop(haplotypes = haplo, genMap = map)

}



#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 3) {
  stop("Usage: independent_validate_v4_s2_avaglio_a2.R <input.tsv> <output_root> <restricted_dir>")
}

input_path <- args[[1]]
output_root <- args[[2]]
restricted_dir <- args[[3]]
dir.create(file.path(output_root, "audit"), recursive = TRUE, showWarnings = FALSE)
dir.create(file.path(output_root, "diagnostics"), recursive = TRUE, showWarnings = FALSE)
dir.create(restricted_dir, recursive = TRUE, showWarnings = FALSE)

suppressPackageStartupMessages(library(survival))

source_covariates <- c(
  "age", "corticosteroids", "surgical_status", "sex", "kps",
  "mgmt_status", "mmse", "rpa_class", "who"
)
specifications <- list(
  list(claim_id = "GBM_01", signature = "Phillips_proneural35", column = "phillips_subtype"),
  list(claim_id = "GBM_02", signature = "Verhaak_proneural", column = "tcga_subtype")
)

d <- read.delim(
  input_path,
  sep = "\t",
  header = TRUE,
  stringsAsFactors = FALSE,
  check.names = FALSE,
  na.strings = character(),
  quote = "",
  comment.char = ""
)
stopifnot(nrow(d) == 349)
literal_na <- apply(d[, source_covariates, drop = FALSE], 1, function(x) any(x == "NA"))
a2 <- d[d$idh1_status == "Wild type" & !literal_na, , drop = FALSE]
stopifnot(nrow(a2) == 333)
a2$duration <- as.numeric(a2[["os_time_to_event_(months)"]])
a2$event <- as.integer(a2[["os_event_type_(0_=_censored)"]])
stopifnot(sum(a2$event) == 260)

result_rows <- list()
ph_rows <- list()
influence_rows <- list()
restricted_rows <- list()
threshold <- 2 / sqrt(nrow(a2))

for (spec in specifications) {
  model_data <- data.frame(
    duration = a2$duration,
    event = a2$event,
    marker = as.integer(tolower(a2[[spec$column]]) == "proneural"),
    treatment_binary = as.integer(a2$treatment == "Bevacizumab")
  )
  model_data$interaction <- model_data$marker * model_data$treatment_binary
  fit <- coxph(
    Surv(duration, event) ~ marker + treatment_binary + interaction,
    data = model_data,
    ties = "efron",
    x = TRUE,
    y = TRUE,
    model = TRUE,
    singular.ok = FALSE
  )
  summary_fit <- summary(fit)
  coef_row <- summary_fit$coefficients["interaction", ]
  ci_row <- summary_fit$conf.int["interaction", ]
  result_rows[[length(result_rows) + 1]] <- data.frame(
    claim_id = spec$claim_id,
    signature = spec$signature,
    implementation = "R_survival_coxph_efron",
    n = fit$n,
    events = fit$nevent,
    interaction_beta = unname(coef_row["coef"]),
    interaction_se = unname(coef_row["se(coef)"]),
    interaction_hr = unname(ci_row["exp(coef)"]),
    ci95_low = unname(ci_row["lower .95"]),
    ci95_high = unname(ci_row["upper .95"]),
    interaction_z = unname(coef_row["z"]),
    interaction_p = unname(coef_row["Pr(>|z|)"]),
    log_likelihood = unname(fit$loglik[2]),
    iterations = fit$iter,
    converged = is.null(fit$fail),
    stringsAsFactors = FALSE
  )

  ph <- cox.zph(fit, transform = "rank", global = TRUE)
  ph_table <- as.data.frame(ph$table)
  ph_table$term <- rownames(ph_table)
  rownames(ph_table) <- NULL
  names(ph_table)[1:3] <- c("chisq", "df", "p")
  ph_table$claim_id <- spec$claim_id
  ph_table$signature <- spec$signature
  ph_table$implementation <- "R_survival_cox_zph_rank"
  ph_rows[[length(ph_rows) + 1]] <- ph_table[, c("claim_id", "signature", "implementation", "term", "chisq", "df", "p")]

  raw <- residuals(fit, type = "dfbeta")
  scaled <- residuals(fit, type = "dfbetas")
  # survival 3.8.6 returns these matrices without column names even though
  # coefficient names are available on the fitted object.  Restore the
  # deterministic coefficient order before term-wise reporting.
  if (is.null(colnames(raw))) {
    colnames(raw) <- names(coef(fit))
  }
  if (is.null(colnames(scaled))) {
    colnames(scaled) <- names(coef(fit))
  }
  for (term in colnames(raw)) {
    influence_rows[[length(influence_rows) + 1]] <- data.frame(
      claim_id = spec$claim_id,
      signature = spec$signature,
      implementation = "R_survival_residuals",
      term = term,
      n = nrow(a2),
      dfbetas_threshold_2_over_sqrt_n = threshold,
      max_abs_dfbeta = max(abs(raw[, term])),
      max_abs_dfbetas = max(abs(scaled[, term])),
      count_abs_dfbetas_above_threshold = sum(abs(scaled[, term]) > threshold),
      stringsAsFactors = FALSE
    )
  }

  top <- order(abs(scaled[, "interaction"]), decreasing = TRUE)[1:5]
  restricted_rows[[length(restricted_rows) + 1]] <- data.frame(
    claim_id = spec$claim_id,
    signature = spec$signature,
    rank_abs_interaction_dfbetas = seq_along(top),
    source_row_1based = as.integer(rownames(a2)[top]),
    geo_accession = a2$geo_accession[top],
    interaction_dfbeta = raw[top, "interaction"],
    interaction_dfbetas = scaled[top, "interaction"],
    stringsAsFactors = FALSE
  )
}

write.table(
  do.call(rbind, result_rows),
  file.path(output_root, "audit", "V4_S2_independent_R_cox_results.tsv"),
  sep = "\t", row.names = FALSE, quote = FALSE, na = ""
)
write.table(
  do.call(rbind, ph_rows),
  file.path(output_root, "diagnostics", "V4_S2_A2_ph_R_cox_zph.tsv"),
  sep = "\t", row.names = FALSE, quote = FALSE, na = ""
)
write.table(
  do.call(rbind, influence_rows),
  file.path(output_root, "diagnostics", "V4_S2_A2_influence_R.tsv"),
  sep = "\t", row.names = FALSE, quote = FALSE, na = ""
)
write.table(
  do.call(rbind, restricted_rows),
  file.path(restricted_dir, "V4_S2_A2_top5_influential_records_R_RESTRICTED.tsv"),
  sep = "\t", row.names = FALSE, quote = FALSE, na = ""
)

software <- data.frame(
  component = c("R", "survival"),
  version = c(as.character(getRversion()), as.character(packageVersion("survival"))),
  stringsAsFactors = FALSE
)
write.table(
  software,
  file.path(output_root, "audit", "V4_S2_independent_R_software.tsv"),
  sep = "\t", row.names = FALSE, quote = FALSE
)

cat("Independent R validation completed for", length(result_rows), "models\n")


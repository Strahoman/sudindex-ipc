# install.packages("fedstatAPIr") # Раскомментируй при первом запуске
library(fedstatAPIr)

# Получаем ИПЦ по коду показателя 31074 (Индекс потребительских цен к предыдущему месяцу)
data <- fedstat_fetch_table(
  table_code = "31074",
  filters = list(territory = "1")  # код 1 — Россия
)

# Преобразуем и оставляем последние 24 месяца
data$Period <- as.Date(paste0(data$Time, "-01"))
data <- data[order(data$Period), ]
data_latest <- tail(data, 24)

# Сохраняем в CSV для Python
write.csv(data_latest[, c("Time", "Value")], "ipc_from_r.csv", row.names = FALSE)
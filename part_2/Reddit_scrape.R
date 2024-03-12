#Scrape comments from r/DataScience and r/DataEngineering
library(RedditExtractoR)
library(dplyr)

start <- Sys.time()

print("Scraping r/datascience posts for URLs...")

ds <- find_thread_urls(subreddit = "datascience", period = "year")
ds_urls <- ds$url

print("\tr/datascience post URLs scraped.")

end_time <- Sys.time()
time_passed_minutes <- as.numeric(
  difftime(end_time, start, units = "mins")
)

cat("\tTime Passed (minutes):", time_passed_minutes, "\n")

start <- Sys.time()

print("Scraping r/datascience threads...")

ds_comments <- get_thread_content(ds_urls)
ds_comments <- as.data.frame(ds_comments$comments)
ds_comments <- ds_comments |>
  mutate(subreddit = "r/datascience")

print("\tr/datascience threads scraped.")

end_time <- Sys.time()
time_passed_minutes <- as.numeric(
  difftime(end_time, start, units = "mins")
)

cat("\tTime Passed (minutes):", time_passed_minutes, "\n")

start <- Sys.time()

print("Scraping r/dataengineering posts for URLs...")

de <- find_thread_urls(subreddit = "dataengineering", period = "year")
de_urls <- de["url"]

print("\tr/dataengineering post URLs scraped.")

end_time <- Sys.time()
time_passed_minutes <- as.numeric(
  difftime(end_time, start, units = "mins")
)

cat("\tTime Passed (minutes):", time_passed_minutes, "\n")

print("Scraping r/dataengineering threads...")

de_comments <- get_thread_content(de_urls)
de_comments <- as.data.frame(de_comments$comments)

print("\tr/dataengineering threads scraped.")

end_time <- Sys.time()
time_passed_minutes <- as.numeric(
  difftime(end_time, start, units = "mins")
)

cat("\tTime Passed (minutes):", time_passed_minutes, "\n")

reddit_scrape <- rbind(ds_comments, de_comments)
write.csv(reddit_scrape, "reddit scrape.csv")
write.table(reddit_scrape, "reddit scrape.txt", sep = "\t", row.names = FALSE)

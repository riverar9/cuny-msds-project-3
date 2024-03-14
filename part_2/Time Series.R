#Time Series Sentiment

library(ggplot2)
library(zoo)
tidy_full_scrape_merged_sentiments = read.csv('/Users/Lucas/Downloads/tidy_full_scrape_merged_sentiments.csv')

#Use code from here----

time_series = tidy_full_scrape_merged_sentiments %>%
  group_by(date) %>%
  summarize(positive = sum(sentiment == "positive", na.rm = TRUE), 
            negative = sum(sentiment == "negative", na.rm = TRUE)) %>%
  mutate(sentiment_value = positive - negative) %>%
  mutate(roll_avg_7 = rollmean(sentiment_value, k = 7, fill = NA)) %>%
  mutate(roll_avg_30 = rollmean(sentiment_value, k = 30, fill = NA)) %>%
  mutate(roll_avg_30_pos = rollmean(positive, k = 30, fill = NA)) %>%
  mutate(roll_avg_30_neg = rollmean(negative, k = 30, fill = NA))


time_series$date = as.Date(time_series$date)

ggplot(aes(x = date, y = roll_avg_30), data = time_series) +
  geom_line() +
  theme_minimal() +
  labs(x = 'Date', y = 'Sentiment Count (Positive - Negative)', title = '30-day Rolling Mean of Sentiment for r/DataScience and r/DataEngineer')

ggplot(aes(x = date, y = roll_avg_7), data = time_series) +
  geom_line() +
  theme_minimal() +
  labs(x = 'Date', y = 'Sentiment Count (Positive - Negative)', title = '7-day Rolling Mean of Sentiment for r/DataScience and r/DataEngineer')

ggplot(aes(x = date, y = sentiment_value), data = time_series) +
  geom_line() +
  theme_minimal() +
  labs(x = 'Date', y = 'Sentiment Count (Positive - Negative)', title = 'Sentiment Value for r/DataScience and r/DataEngineer')

ggplot(time_series, aes(x = date)) +
  geom_line(aes(y = roll_avg_30_pos, color = "Positive")) +
  geom_line(aes(y = roll_avg_30_neg, color = "Negative")) +
  labs(x = "Date", y = " Sentiment Count", title = "30-day Rolling Mean of Sentiment for r/DataScience and r/DataEngineer", color = "Sentiment") +
  scale_color_manual(values = c("Positive" = "#4CCD99", "Negative" = "#EE4266")) +
  theme_minimal()


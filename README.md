# password_hacker.py
This python helps us check our password against pwned password without passing the whole password.
This python reads passwords from a file line by line and sends the first 5 characters of sha1 hashed password to pwned api . Pwned api returns all hashed exploited password. Then we check the sha1 hashed password against hashed exploited password. 

# scraper.py
This python scrape a dynamic website with javascript and sends an email notification once we find the "FAILED" on the website.

# safe.py
This python scrapes all text value by name field and write it to a new file

# Tg_bot.py
> Connect TG bot to ChatGPT and deploy it onto AWS Severless Lamda 
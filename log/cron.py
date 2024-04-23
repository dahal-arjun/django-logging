def my_cron_job():
    print("Hello, World!")
    with open("log.txt", "a") as f:
        f.write("Hello, World!\n")

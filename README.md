# unimelb-badminton-courts-notifier

A bot to crawl the information of the availability of badminton courts at Melbourne uni.

Its task is to notify me by sending an email if there is any available 1-hour slot on this or next weekends

No one can book badminton courts at Melbourne uni earlier than me 😎

### Run the Program
1. Enable the program by setting `RUN_PROGRAM` to `True` in `config.py`

2. Install dependencies if needed
    ```
    pip install -r requirements.txt
    ```

3. Create a file `.env` and set the environment variables following `.env.example`

4. Start crawling 🤠
    ```
    python main.py
    ```
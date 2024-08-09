# Gravity Falls Code Cracker Script

This Python script automates the submission of codes to an API endpoint, handling rate limits by using an adaptive delay mechanism. The script reads a list of codes from a file and attempts to submit them, adjusting the delay between requests based on the server's responses to avoid being rate-limited.

## Features

- **Adaptive Delay:** Dynamically adjusts the delay between requests based on success or failure, reducing the chances of hitting rate limits.
- **Progress Tracking:** Saves progress in a JSON file to allow resumption from where it left off.
- **Code Storage:** Successfully submitted codes and their responses are saved in a JSON file.

## Prerequisites

- Python 3.x
- `requests` library

Install the required library using pip:

```bash
pip install requests
```

## Usage

1. **Prepare Your Word List:** 
   - Create or modify the file `sanitized_wordlist.txt` to contain the codes you want to submit, with one code per line.

2. **Run the Script:**

   ```bash
   python main.py
   ```

3. **Monitor Progress:**
   - The script will output the current word being processed and the current delay between requests.
   - If the script is interrupted, it will save the current progress in `progress.json` and resume from there the next time you run it.

4. **Check Results:**
   - Successfully submitted codes are saved in `successful_codes.json` along with the server's response.

## Configuration

- **File Paths:**
  - Modify the path to your word list in the `main()` function if your file is not named `sanitized_wordlist2.txt`.

- **Adaptive Delay Parameters:**
  - You can tweak the adaptive delay parameters (`initial_delay`, `min_delay`, `max_delay`, etc.) by modifying the `AdaptiveDelay` class in the script.

## Code Explanation

### `AdaptiveDelay` Class

- Manages the delay between requests based on server responses.
- Increases the delay when the request fails (e.g., due to rate limiting) and decreases it after a certain number of successful requests.

### `send_request()` Function

- Sends the code to the API endpoint using a POST request.
- Adjusts the delay based on the success or failure of the request.

### `main()` Function

- Loads the list of codes, tracks progress, and iterates over the codes to send each one using the `send_request()` function.

## License

This project is licensed under the BSD 2-Clause License. See the `LICENSE` file for details.

## Disclaimer

This script is provided "as is", without warranty of any kind. The authors are not responsible for any misuse or damage that may arise from its use.

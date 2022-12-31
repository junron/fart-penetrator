# Fart Penetrator

Burp Intruder but more 💩

## Features

- Send requests concurrently
- Configure anything in the HTTP request
- Sort by content length or response time
- Use payload sets from
    - Portswigger username list
    - Postswigger password list
    - Integer ranges
    - Files

## Installation

1. Clone this repo
2. `pip install -r requirements.txt`
3. Install the [Among Us font](https://www.fontget.com/font/among-us/)
   and [Fira Code](https://github.com/tonsky/FiraCode)
4. Run `penetrator.py`

## Usage

1. Use Burp proxy to capture a HTTP request
2. Copy and paste the HTTP request to the HTTP request tab of Fart Penetrator
3. Replace fields to be fuzzed with FUZZ{n}, where n >= 0
4. Switch to payloads tab and load a payload set from a predefined wordlist, custom file, or integer range
5. Click "Launch Attack!"


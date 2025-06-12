# HMM Shipping Tracking Automation

This project automates the process of retrieving shipping information from HMM (Hyundai Merchant Marine) using browser automation and AI. It can track shipping details including voyage numbers and arrival dates based on booking IDs. Tested on two IDs "HANA98736001" and "SINI25432400"

## Features

- Automated browser navigation to HMM shipping tracking
- AI-powered interaction with web elements
- Support for both initial tracking and replay of successful tracking sequences
- Saves successful tracking sequences for future use
- Handles browser cleanup and resource management
- Anti-detection measures to prevent website blocking
- Automatic retry mechanism for failed attempts
- Human-like behavior simulation with random delays and mouse movements
- Demo Video Link: https://drive.google.com/drive/folders/1pl8zxIaIj1bkdEYiOFtvICldnKVTPYJo?usp=sharing

## Prerequisites

- Python >=3.11 and <3.13
- Google API key for Gemini model
- Chromium browser (installed automatically)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Kjain02/Sidecar_Project.git
cd Sidecar_Project
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Playwright browser:
```bash
playwright install chromium --with-deps --no-shell
```

5. Create a `.env` file in the project root and add your Google API key. Get it from https://aistudio.google.com/apikey
```bash
GOOGLE_API_KEY=your_api_key_here
```

## Usage

### Windows Users
Simply double-click the `run.bat` file or run it from the command prompt:
```bash
.\run.bat
```
The batch file will:
1. Create a virtual environment if it doesn't exist
2. Install/update all required dependencies
3. Set up Playwright browser
4. Run the tracking script
5. Clean up resources when done

### Manual Execution
Run the script with a booking ID:
```bash
python browser_auto.py
```

The script will:
1. Check for existing web interactions
2. If found, replay the stored steps with the new booking ID
3. If not found, perform a new tracking sequence
4. Save successful sequences for future use

## Project Structure

- `browser_auto.py`: Main script for tracking shipping information
- `requirements.txt`: Project dependencies
- `.env`: Environment variables (not tracked in git)
- `agent_action_steps.json`: Stored successful tracking sequences

## Dependencies

- browser-use: Browser automation framework
- langchain: AI agent framework
- google-generativeai: Google's Gemini model integration
- python-dotenv: Environment variable management
- playwright: Browser automation engine

## Error Handling

The script includes comprehensive error handling for:
- Browser automation failures
- API errors
- Resource cleanup
- Website blocking and detection
- Failed tracking attempts

### Anti-Detection Measures
The script implements several anti-detection features:
- Random delays between actions (1-3 seconds)
- Random mouse movements to simulate human behavior
- Natural interaction patterns
- Case-insensitive error detection

### Retry Mechanism
The script includes an intelligent retry system that:
- Detects common error patterns in URLs
- Automatically retries failed attempts
- Monitors for error indicators like "error", "failed", "invalid", etc.
- Adds new tasks when retry is needed
- Limits maximum retry attempts to prevent infinite loops

## Criteria Met

### 1. Natural Language Usage
The agent interprets high-level, human-readable instructions (e.g., "Track shipment for booking ID HANA98736001") and autonomously performs all necessary browser interactions without requiring hardcoded steps.

- Uses a Gemini-powered agent to understand and act on intent
- Prompts are abstracted from implementation, allowing easy customization
- New tasks can be added by simply describing what needs to be done

### 2. Repeatability
The solution records successful sequences of actions (mouse clicks, keystrokes, navigation steps, etc.) in a structured JSON file (agent_action_steps.json). These can be:

- Replayed later with different input values (like booking IDs)
- Improved iteratively by refining action sequences from real-world runs

### 3. Generalization
The pipeline has been designed to generalize across multiple booking IDs without requiring changes to logic or selectors:

- We can change Booking ID in the browser_auto.py
- Verified to work with booking IDs like "HANA98736001" and "SINI25432400"



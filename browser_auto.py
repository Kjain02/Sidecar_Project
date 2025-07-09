"""
HMM Shipping Tracking Automation

This module provides functionality to automate the process of retrieving shipping information
from HMM (Hyundai Merchant Marine) using browser automation and AI. It can track shipping
details including voyage numbers and arrival dates based on booking IDs.

The module uses:
- browser-use for browser automation
- Google's Gemini model for AI-powered interactions
- Playwright for browser control
"""

import os
import asyncio
import sys
import random
import json
from pathlib import Path
from dotenv import load_dotenv
from browser_use import Agent
from browser_use.llm import ChatGoogle
import platform

# Configure event loop policy for Windows
if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy()) # Use ProactorEventLoop for Windows


# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError("Set GOOGLE_API_KEY in .env")





async def anti_detection_hook(agent: Agent):
    """Add human-like delays and behavior. Implements anti-detection
    measures to prevent website blocking and simulate human-like behavior."""
    page = await agent.browser_session.get_current_page()
    
    # Add random delays between actions
    delay = random.uniform(1.0, 3.0)
    await asyncio.sleep(delay)
    # Occasionally move mouse randomly (simulate human behavior)
    if random.random() < 0.3:  # 30% chance
        await page.mouse.move(
            random.randint(100, 800), 
            random.randint(100, 600)
        )


async def retry_hook(agent: Agent):
    """
    Implements an intelligent retry mechanism for failed tracking attempts.
    
    This function is called after each step to:
    1. Check for common error patterns in the current URL
    2. Automatically retry failed attempts
    3. Add new tasks when retry is needed
    
    Args:
        agent (Agent): The browser automation agent instance
    
    If any error is detected:
    - Prints a retry message
    - Adds a new task to retry the operation
    """
    page = await agent.browser_session.get_current_page()
    current_url = page.url
    
    # Custom logic to determine if retry is needed
    error_indicators = ["error", "failed", "invalid", "incorrect", "unable"]
    if any(err in current_url.lower() for err in error_indicators):
        print("Detected failure condition, will retry...")
        # You can pause and modify the task or add additional instructions
        agent.add_new_task("Retry to complete the original task")


def save_actions(stored_actions):
    """
    Convert model_actions() output to initial_actions format and save to JSON file.
    
    This function handles the DOMHistoryElement serialization issue by extracting
    only the necessary action information and storing it in a format that can be
    replayed later.
    
    Args:
        stored_actions (list): List of action dictionaries from model_actions()
    
    The saved format will be a list of dictionaries, each containing a single
    action name as key and its parameters as value.
    """
    initial_actions = []
    
    for action in stored_actions:
        # Extract the action name and parameters
        # Each action is a dict with one key (the action name) and its parameters
        for action_name, parameters in action.items():
            if action_name != 'interacted_element':  # Skip the interacted_element
                # Create the format expected by initial_actions
                action_dict = {action_name: parameters}
                initial_actions.append(action_dict)
                break  # Only process the first non-interacted_element key
    
    with open(f"agent_action_steps.json", "w") as f:
        json.dump(initial_actions, f, indent=2)


async def fetch_hmm(booking_id: str) -> str:
    """
    Fetch shipping information from HMM website for a given booking ID.
    
    This function attempts to retrieve voyage number and arrival date for a shipping
    booking. It first tries to use stored successful sequences if available, otherwise
    performs a new tracking sequence.
    
    Args:
        booking_id (str): The HMM booking ID to track
        
    Returns:
        str: A string containing the voyage number and arrival date in the format
             "Voyage: <voyage_number>, Arrival: <arrival_date>"
             or "No results found" if tracking fails
    """
    

    # Initialize the Gemini model
    llm = ChatGoogle(
        model="gemini-2.0-flash",
        api_key=api_key
        # google_api_key=api_key
    )
       

    steps_file = Path(f"agent_action_steps.json")
    
    try:
        if steps_file.exists(): # Checks if there is any file exists with stored interactions
            # Load and use stored successful sequence
            with open(steps_file) as f:
                initial_actions = json.load(f)
            # Create an agent with stored actions
            agent = Agent(
                task=f'''Given an HMM booking ID "{booking_id}", retrieve voyage and arrival from HMM Shipping line.''',
                message_context=f'''Replaying previous actions with new booking ID "{booking_id}"
                                and return the new voyage number and arrival date in the format 
                                Voyage: <voyage_number>, Arrival: <arrival_date>''',
                initial_actions=initial_actions,
                llm=llm,
            )
            
            result = await agent.run(
                on_step_start=anti_detection_hook,
                on_step_end=retry_hook,
                max_steps=20
            )
            final_result = result.final_result()
            if final_result:
                return final_result
            return "No results found"

        else:
            # Perform new tracking sequence
            task = f"""
            Your task:
            Given an HMM booking ID "{booking_id}", retrieve voyage and arrival from HMM Shipping line.
            First, navigate to exactly website: http://www.seacargotracking.net/
            Scroll down to find and navigate to the link "HYUNDAI Merchant Marine (HMM)" and stay on that link
            Scroll down to find "Track and Trace" and input the booking ID in the box and search.
            Wait for the results to load or try Refreshing the page only if Blocked by the website.
            Scroll down to find the voyage number and arrival date.
            Only return the Final Answer in the format "Voyage: <voyage_number>, Arrival: <arrival_date>"
            """

            agent = Agent(
                task=task,
                llm=llm
            )
            
            result = await agent.run(
                on_step_start=anti_detection_hook,
                on_step_end=retry_hook,
                max_steps=20
            )
            
            # Get the final result and save successful sequence
            final_result = result.final_result()
            if final_result:
                stored_actions = result.model_actions()
                save_actions(stored_actions) # Save agent actions to json file
                return final_result
            return "No results found"
    
    except Exception as e:
        print(f"Error during cleanup: {e}")

async def main():
    """
    Main function to run the HMM tracking automation.
    
    Currently uses a hardcoded booking ID for testing purposes.
    Handles exceptions and ensures proper cleanup of resources.
    """
    # booking_id = input("Enter HMM booking ID: ").strip()
    booking_id = "SINI25432400"
    
    try:
        # Run the async function
        result = await fetch_hmm(booking_id)
        print("Results:", result)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Set up event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\nShutting down...")
   

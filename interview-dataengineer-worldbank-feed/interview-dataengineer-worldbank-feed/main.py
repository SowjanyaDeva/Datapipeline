import argparse
import schedule
import time
import threading
from src.module1 import refresh_main
from reports.report import report_main
from datetime import datetime
from app import create_app

def refresh_data():
    print("Refreshing data...")
    print(datetime.now())
    refresh_main()
    print("Data refresh complete.")

def generate_report():
    print("Generating reports...")
    print(datetime.now())
    report_main()
    print("Reports generated.")

def schedule_tasks():
    # Schedule tasks
    schedule.every(120).minutes.do(refresh_data)  
    schedule.every(120).minutes.do(generate_report)  

    # Start the scheduler in a loop
    while True:
        schedule.run_pending()
        time.sleep(1)

def main(command):
    if command == 'refresh':
        refresh_data()
    elif command == 'report':
        generate_report()

if __name__ == "__main__":
    app = create_app()

    # Start the scheduler in a separate thread
    scheduler_thread = threading.Thread(target=schedule_tasks)
    scheduler_thread.daemon = True 
    scheduler_thread.start()  

    # Set up argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['refresh', 'report'], nargs='?', help="Command to execute")
    args = parser.parse_args()

    # Process command line argument if provided
    if args.command:
        main(args.command)

    # Run the Flask app
    app.run(debug=True, use_reloader=False)  # Prevent reloader from starting multiple instances

    # The main thread will not exit; it will keep the scheduler and app running
    print("Scheduler is running. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")

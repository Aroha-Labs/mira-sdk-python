import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="A simple CLI parameter parsing example")
    
    # Add arguments
    parser.add_argument("-n", "--name", type=str, help="Your name")
    parser.add_argument("-a", "--age", type=int, help="Your age")
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")
    
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    if args.verbose:
        print("Verbose mode is on")
    
    if args.name:
        print(f"Hello, {args.name}!")
    
    if args.age:
        print(f"You are {args.age} years old.")

if __name__ == "__main__":
    main()

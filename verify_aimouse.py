from aimouse.src.inference.llm_interface import llm_interface

def verify():
    print("--- Testing Vision ---")
    res_vision = llm_interface.execute("rect(0, 0, 0, 0)")
    print(f"Vision Status: {res_vision['status']}")
    print(f"Image Resolution: {res_vision['image']['resolution']}")

    print("\n--- Testing Movement ---")
    # Move to a safe area (e.g., top left)
    res_move = llm_interface.execute("rect(100, 100, 50, 50);click")
    print(f"Movement Status: {res_move['status']}")
    print(f"Success: {res_move.get('success')}")

if __name__ == '__main__':
    verify()
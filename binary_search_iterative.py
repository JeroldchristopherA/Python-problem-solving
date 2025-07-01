def binary_search_iterative(arr, target):
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid  
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1  

# Example usage
nums = [1, 3, 5, 7, 9, 11, 13]
target = 7

result = binary_search_iterative(nums, target)
if result != -1:
    print(f"✅ Found at index {result}")
else:
    print("❌ Not found")

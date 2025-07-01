def binary_search_recursive(arr, target, low, high):
    if low > high:
        return -1  # Not found

    mid = (low + high) // 2

    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, high)
    else:
        return binary_search_recursive(arr, target, low, mid - 1)

# Example usage
nums = [1, 3, 5, 7, 9, 11, 13]
target = 11

result = binary_search_recursive(nums, target, 0, len(nums) - 1)
if result != -1:
    print(f"✅ Found at index {result}")
else:
    print("❌ Not found")

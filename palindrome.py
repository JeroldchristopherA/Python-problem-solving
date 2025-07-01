def is_palindrome(text):
    # Remove spaces and convert to lowercase
    cleaned = text.replace(" ", "").lower()
    return cleaned == cleaned[::-1]

# Example usage
word = input("Enter a word or phrase: ")
if is_palindrome(word):
    print("✅ It's a palindrome!")
else:
    print("❌ Not a palindrome.")

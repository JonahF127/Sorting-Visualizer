def partition(lst, low, high, ascending):
    i = low - 1
    pivot = lst[high] 
    for j in range(low, high):
        if (lst[j] <= pivot and ascending) or (lst[j] >= pivot and not ascending) :
            i += 1
            lst[i], lst[j] = lst[j], lst[i]
    lst[i + 1], lst[high] = lst[high], lst[i + 1]
    return i + 1


def quick_sort(lst, low, high, ascending = True):
    if low < high: 
        pi = partition(lst, low, high, ascending)
        quick_sort(lst, low, pi - 1, ascending)
        quick_sort(lst, pi + 1, high, ascending)



arr = [2, 5, 3, 8, 6, 5, 4, 7]
n = len(arr)
print("Contents of the array: ")
for i in range(n):
   print(arr[i], end=" ")
quick_sort(arr, 0, n - 1, False)
print("\nContents of the array after sorting: ")
for i in range(n):
   print(arr[i], end=" ")